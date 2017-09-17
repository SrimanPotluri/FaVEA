# measure_wav.py
# Paul Boersma 2017-01-03
#
# A sample script that uses the Vokaturi library to extract the emotions from
# a wav file on disk. The file can contain a mono or stereo recording.
#
# Call syntax:
#   python3 measure_wav.py path_to_sound_file.wav

import sys
import scipy.io.wavfile
sys.path.append("OpenVokaturi-2-1d/api")
import Vokaturi


def voice_predict():
    file_name = "Audio/audio.wav"
    print("Loading library...")
    Vokaturi.load("OpenVokaturi-2-1d/lib/Vokaturi_mac64.so")

    print("Analyzed by: %s" % Vokaturi.versionAndLicense())

    print("Reading sound file...")
    (sample_rate, samples) = scipy.io.wavfile.read(file_name)
    print("   sample rate %.3f Hz" % sample_rate)

    print("Allocating Vokaturi sample array...")
    buffer_length = len(samples)
    print("   %d samples, %d channels" % (buffer_length, samples.ndim))
    c_buffer = Vokaturi.SampleArrayC(buffer_length)
    if samples.ndim == 1:
        c_buffer[:] = samples[:] / 32768.0  # mono
    else:
        c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0  # stereo

    print("Creating VokaturiVoice...")
    voice = Vokaturi.Voice (sample_rate, buffer_length)

    print("Filling VokaturiVoice with samples...")
    voice.fill(buffer_length, c_buffer)

    print("Extracting emotions from VokaturiVoice...")
    quality = Vokaturi.Quality()
    emotionProbabilities = Vokaturi.EmotionProbabilities()
    voice.extract(quality, emotionProbabilities)

    fh = open("output.txt", 'a')
    fh.write("Based on your voice, your emotion is ")
    if not quality.valid:
        fh.write("beyond my understanding.\n")
        exit(1)

    print_result = [(round(emotionProbabilities.neutrality*100), "neutral"), \
                   (round(emotionProbabilities.happiness*100), "happy"), \
                   (round(emotionProbabilities.anger*100), "angry"), \
                   (round(emotionProbabilities.fear*100),"fearful"), \
                   (round(emotionProbabilities.sadness*100), "sad")]
    print_result = [tup for tup in print_result if tup[0] != 0]
    print_result.sort(key=lambda tup: tup[0])
    if len(print_result) == 0:
        fh.write("beyond my understanding.\n")
    elif len(print_result) == 1:
        fh.write("dominantly %d percent %s.\n" % (print_result[0][0], print_result[0][1]))
    else:
        for i in range(len(print_result) - 1, 0, -1):
            fh.write("%d percent %s, " % (print_result[i][0], print_result[i][1]))
        fh.write("and %d percent %s.\n" % (print_result[0][0], print_result[0][1]))
    fh.close()

    with open("output.txt") as f1:
        with open("templates.yaml", "w") as f2:
            f2.write("welcome: Ready to hear your comments?\n\nround: ")
            for line in f1:
                f2.write(line.strip("\n"))
                f2.write(" ")

    voice.destroy()


#voice_predict(sys.argv[1])
