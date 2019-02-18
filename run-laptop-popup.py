import numpy
from datetime import datetime
from classifier.all_classifiers import Classification

from cameras.laptopcam import stream_video
# from detectors.simple import detect_face
from detectors.rollingcaro import detect_face
# from reporting.popup import show_frame, show_detected
from reporting.web import show_frame, show_detected
from classifier.all_classifiers import classify

# cascada to use with opencv to identify faces
cascadePath = './models/opencv/haarcascade_frontalface_default.xml'

# cooldown time in seconds, the time to wait before a new detection is used
cooldown_time = 5

cooldown_start_time = None

last_labels = Classification("unknown", "unknown")


def every_frame(frame):
    global cooldown_start_time, last_labels

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

        classification = classify(frame)

        if last_labels is not classification:
            last_labels = classification

        label_action(last_labels)


def label_action(labels):
    show_detected(labels)


stream_video(every_frame)
