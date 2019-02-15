import numpy
from datetime import datetime

from cameras.laptopcam import stream_video
from detectors.simple import detect_face
from reporting.popup import show_frame, show_detected
from classifier.random import classify

# cascada to use with opencv to identify faces
cascadePath = './models/opencv/haarcascade_frontalface_default.xml'

# cooldown time in seconds, the time to wait before a new detection is used
cooldown_time = 5

cooldown_start_time = None
last_label = None


def every_frame(frame):
    global cooldown_start_time, last_label

    # detector
    person_detected, frame_with_face = detect_face(numpy.copy(frame), cascadePath)

    # if we haven't detected a person don't do anything
    if not person_detected:
        show_frame(frame)
        return

    # show the person we detected
    show_frame(frame_with_face)

    if cooldown_start_time is not None:
        since_detected = (datetime.now() - cooldown_start_time).total_seconds()

        # we detected a person a while ago and are still in cooldown
        if since_detected < cooldown_time:
            pass
        if since_detected > cooldown_time:
            cooldown_start_time = None

    # no cooldown
    if cooldown_start_time is None:
        cooldown_start_time = datetime.now()
        label = classify(frame)
        if last_label is not label:
            last_label = label
            label_action(label)


def label_action(label: str):
    show_detected(label)


stream_video(every_frame)
