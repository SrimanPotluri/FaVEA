import moviepy.editor as mp
import cv2
import os
import glob


def video(file_path):
    vidcap = cv2.VideoCapture(file_path)
    success, image = vidcap.read()
    count = 0
    num_frame = 0
    filelist = glob.glob('Screenshots/*')
    for f in filelist:
        os.remove(f)
    filelist = glob.glob('ProcessedPhotos/*')
    for f in filelist:
        os.remove(f)
    filelist = glob.glob('Audio/*')
    for f in filelist:
        os.remove(f)

    while success:
        success, image = vidcap.read()
        if num_frame == 10:
            cv2.imwrite("Screenshots/frame%d.jpg" % count, image)     # save frame as JPEG file
        if num_frame == 20:
            num_frame = 0
        count += 1
        num_frame += 1
    clip = mp.VideoFileClip(file_path)
    clip.audio.write_audiofile("Audio/audio.wav")


#video()