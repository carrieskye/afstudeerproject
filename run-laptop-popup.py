from cameras.laptopcam import stream_video
#from detectors.simple import detect_face
from detectors.rollingcaro import detect_face
from reporting.popup import show_frame
#from reporting.web import show_frame

cascadePath = './models/opencv/haarcascade_frontalface_default.xml'


def every_frame(frame):
    frame_with_face = detect_face(frame, cascadePath)
    show_frame(frame_with_face)


stream_video(every_frame)
