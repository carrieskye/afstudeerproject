from cameras.laptopcam import stream_video
from reporting.popup import show_frame
#from detectors.simple import detect_face
from detectors.rollingcaro import detect_face

cascadePath = './models/opencv/haarcascade_frontalface_default.xml'


def every_frame(frame):
    frame_with_face = detect_face(frame, cascadePath)
    show_frame(frame_with_face)


stream_video(every_frame)
