import VideoSegmentation
import PredictTestData
import Voice


def main(file_path):
    VideoSegmentation.video(file_path)
    PredictTestData.detect_faces()
    PredictTestData.face_predict()
    Voice.voice_predict()

#main("Videos/Speech1.mp4")
