from datetime import datetime
import argparse
import importlib

import numpy

from cameras.laptop_cam import stream_video
from classifier.classifier import Classification
from classifier.classifier import start_classify_stream
from detectors.rolling_caro import detect_face, get_detected_frames
from data_treatment.post_processor import cleanup

# Reporting is loaded based on arguments, see main()
reporting = None

# cascade to use with opencv to identify faces
cascadePath = './models/opencv/haarcascade_frontalface_default.xml'

# cooldown time in seconds, the time to wait before a new detection is used
cooldown_time = 3
cooldown_start_time = None

last_labels = Classification('unknown', 'unknown', -1)


def every_frame(frame):
    global cooldown_start_time, last_labels

    # detector
    person_detected, frame_with_face = detect_face(numpy.copy(frame), cascadePath)

    # if we haven't detected a person don't do anything
    if not person_detected:
        reporting.show_frame(frame)
        return

    # show the person we detected
    reporting.show_frame(frame_with_face)

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
        detected_frames = get_detected_frames(cooldown_start_time.timestamp() - 1)

        start_classify_stream(detected_frames, classification_done)


def classification_done(classification_results):
    classification = cleanup(classification_results)
    label_action(classification)


def label_action(labels):
    reporting.show_detected(labels)


def main():
    global reporting
    args = get_args()
    # load either web or pop-up reporting based on args
    reporting_module = 'reporting.' + ('web' if args.web else 'popup')
    print("Loading " + reporting_module)
    reporting = importlib.import_module(reporting_module)
    stream_video(every_frame)


def get_args():
    parser = argparse.ArgumentParser(description="This script will launch the project",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--web", type=bool, default=False,
                        help="Serve web-page instead of showing pop-up")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
