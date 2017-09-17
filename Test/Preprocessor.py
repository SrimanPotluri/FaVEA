import glob
import os

from shutil import copyfile

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]  # Define emotion order
participants = glob.glob("/Users/sriman/Documents/source_emotion/*")  # Returns a list of all folders with participant numbers

for x in participants:
    part = "%s" % x[-4:]  # store current participant number
    for sessions in glob.glob("%s/*" % x):  # Store list of sessions for current participant
        for files in glob.glob("%s/*" % sessions):
            current_session = files[44:-30]
            file = open(files, 'r')

            emotion = int(float(file.readline()))  # emotions are encoded as a float, readline as float, then convert to integer.
            sourcefile_emotion = glob.glob("/Users/sriman/Documents/source_images/%s/%s/*" % (part, current_session))[-1]  # get path for last image in sequence, which contains the emotion
            sourcefile_neutral = glob.glob("/Users/sriman/Documents/source_images/%s/%s/*" % (part, current_session))[0]  # do same for neutral image
            print sourcefile_neutral[47:]
            dest_neut = "/Users/sriman/Documents/sorted_set/neutral/%s" % sourcefile_neutral[47:]  # Generate path to put neutral image
            dest_emot = "/Users/sriman/Documents/sorted_set/%s/%s" % (emotions[emotion], sourcefile_emotion[47:])  # Do same for emotion containing image


            copyfile(sourcefile_neutral, dest_neut)  # Copy file
            copyfile(sourcefile_emotion, dest_emot)  # Copy file