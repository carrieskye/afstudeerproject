import numpy


from cameras.laptopcam import stream_video
#from detectors.simple import detect_face
from detectors.rollingcaro import detect_face
from reporting.popup import show_frame
#from reporting.web import show_frame

cascadePath = './models/opencv/haarcascade_frontalface_default.xml'


def every_frame(frame):
    person_detected, frame_with_face = detect_face(numpy.copy(frame), cascadePath)
    if person_detected:
        show_frame(frame_with_face)
    else:
        show_frame(frame)


stream_video(every_frame)
