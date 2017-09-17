import cv2
import glob
# face is a namespace
from cv2 import face

faceDet = cv2.CascadeClassifier("/Users/sriman/Documents/OpenCV_FaceCascade/haarcascade_frontalface_default.xml")
faceDet_two = cv2.CascadeClassifier("/Users/sriman/Documents/OpenCV_FaceCascade/haarcascade_frontalface_alt2.xml")
faceDet_three = cv2.CascadeClassifier("/Users/sriman/Documents/OpenCV_FaceCascade/haarcascade_frontalface_alt.xml")
faceDet_four = cv2.CascadeClassifier("/Users/sriman/Documents/OpenCV_FaceCascade/haarcascade_frontalface_alt_tree.xml")

emotions = ["neutral", "happy", "angry",  "fearful",  "sad", "surprised", "contemptuous", "disgusted"]  # Emotion list
fishface = face.FisherFaceRecognizer_create()  # Initialize fisher face classifier
fishface.read("./Face.xml")


def face_predict():  # Define function to get file list, randomly shuffle it and split 80/20
    prediction_data=[]
    files = glob.glob("ProcessedPhotos/*")
    for item in files:
            image = cv2.imread(item)  # open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
            prediction_data.append(gray)  # append image array to training data list

    result = [0.0] * 8
    print "predicting classification set"
    for image in prediction_data:
        pred, conf = fishface.predict(image)
        result[pred] += 1

    su = sum(result)
    print_result = []
    for i in range(len(result)):
        temp = round(result[i]/su * 100)
        if temp != 0:
            print_result.append((temp, emotions[i]))

    print_result.sort(key=lambda tup: tup[0])
    fh = open("output.txt", 'w')
    fh.write("Based on your facial expression, your emotion is ")
    if len(print_result) == 0:
        fh.write("beyond my understanding.\n")
    elif len(print_result) == 1:
        fh.write("dominantly %d percent %s.\n" % (print_result[0][0], print_result[0][1]))
    else:
        for i in range(len(print_result)-1, 0, -1):
            fh.write("%d percent %s, " % (print_result[i][0], print_result[i][1]))
        fh.write("and %d percent %s.\n" % (print_result[0][0], print_result[0][1]))
    fh.close()


def detect_faces():
    files = glob.glob("Screenshots/*")  # Get list of all images with emotion

    filenumber = 0
    for f in files:
        frame = cv2.imread(f)  # Open image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale

        # Detect face using 4 different classifiers
        face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                        flags=cv2.CASCADE_SCALE_IMAGE)
        face_two = faceDet_two.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
        face_three = faceDet_three.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                                    flags=cv2.CASCADE_SCALE_IMAGE)
        face_four = faceDet_four.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
                                                  flags=cv2.CASCADE_SCALE_IMAGE)

        # Go over detected faces, stop at first detected face, return empty if no face.
        if len(face) == 1:
            facefeatures = face
        elif len(face_two) == 1:
            facefeatures = face_two
        elif len(face_three) == 1:
            facefeatures = face_three
        elif len(face_four) == 1:
            facefeatures = face_four
        else:
            facefeatures = ""

        # Cut and save face
        for (x, y, w, h) in facefeatures:  # get coordinates and size of rectangle containing face
            print "face found in file: %s" % f
            gray = gray[y:y + h, x:x + w]  # Cut the frame to size

            try:
                out = cv2.resize(gray, (350, 350))  # Resize face so all images have same size
                cv2.imwrite("ProcessedPhotos/%s.jpg" % filenumber, out)  # Write image
            except:
                pass  # If error, pass file
        filenumber += 1  # Increment image number


# Now run it
#detect_faces()  # Call functiona
#face_predict()