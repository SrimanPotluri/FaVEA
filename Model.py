import cv2
import glob
import numpy as np
# face is a namespace
from cv2 import face


emotions = ["neutral", "happy", "angery",  "fearful",  "sad", "surprised", "contemptuous", "disgusted"]  # Emotion list
fisher_face = face.FisherFaceRecognizer_create()  # Initialize fisher face classifier


def build_model():
    training_data = []
    training_labels = []

    for emotion in emotions:
        files = glob.glob("Dataset/%s/*" % emotion)
        # Append data to training and prediction list, and generate labels 0-7
        for item in files:
            image = cv2.imread(item)  # open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
            training_data.append(gray)  # append image array to training data list
            training_labels.append(emotions.index(emotion))
    print "training fisher face classifier"
    print "size of training set is:", len(training_labels), "images"
    fisher_face.train(training_data, np.asarray(training_labels))
    fisher_face.write('./Face.xml')


# Now run it
build_model()