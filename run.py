import argparse
import importlib
import signal
import time
import json

import cv2

from activation.simple import is_activated
from annotate.simple import annotate_frame
from cameras.laptop_cam import stream_video
from classifier.classifier import Classifier
from data_treatment.post_processor import get_overall_classification
from detectors.simple import detect_face
from person_selector.simple import select_person
from positioning.simple import get_position
from recognition.identify import get_identifications, persist
from utils import TimeBlock, timeblock_stats

# Reporting is loaded based on arguments, see main()
reporting = None

# Classifier loaded in main
classifier = None

# cascade to use with opencv to identify faces
cascadePath = './models/opencv/haarcascade_frontalface_default.xml'

# dictionary with person -> classifications
people = {}

# list with all classifications for daily exports
export = []

# keep track of activation, so the home page only changes if no one was before the camera in the previous frame
was_activated = False

# Print classifications as we get them
print_classification = False

# keep recent classifications to use for person selector
recent_classifications = {}


def every_frame(frame, timestamp):
    global was_activated, recent_classifications

    # get faces from detector
    with TimeBlock('detection'):
        faces = detect_face(frame, cascadePath)

    with TimeBlock('identification'):
        # get identifications for the faces
        people_in_frame = get_identifications(frame, faces)

    # labels for each person in the frame
    labels = []

    # here we want the iterate over the identified persons and classify them
    for index, face in enumerate(faces):
        # get the positioning of the person
        position = get_position(frame, face)

        # get the name of the current face
        name = people_in_frame[index]

        # get classification for this face
        classification = classifier.classify(frame, face, timestamp, name, position)

        # if we want to debug we can print the classification
        if print_classification:
            print(classification)

        # if this is the first time initialise in the people dictionary
        if name not in people:
            people[name] = []

        # append this classification
        people[name].append(classification)

        # append to export
        export.append(classification)

        # get average age, most common gender and last emotion
        with TimeBlock('overall'):
            overall_classification = get_overall_classification(people[name])

        labels.append(overall_classification)

    # add new classifications to recent classifications
    for classification in labels:
        recent_classifications[classification] = 5

    # lower time to live by one and remove expired classifications
    for key, value in recent_classifications.items():
        recent_classifications[key] = value - 1
    recent_classifications = {k: v for k, v in recent_classifications.items() if v > 0}

    # if activated, we determine the most important person and send advertisements for this person
    activated = is_activated(timestamp, people_in_frame)
    if activated and len(labels) > 0:
        selected_labels = select_person(recent_classifications.keys())
        reporting.show_detected(selected_labels, was_activated)
    was_activated = activated

    # annotate the frame
    annotate_frame(frame, faces, labels)

    # show the person we detected
    reporting.show_frame(frame)


def sigint_handler(*_):  # https://stackoverflow.com/a/36120113
    timeblock_stats()
    persist()

    # save to json file
    path = './dump.json'

    def obj_dict(obj):
        return obj.__dict__

    with open(path, 'w') as f:
        f.write(json.dumps(export, default=obj_dict))
    print(f'Saved {len(export)} classifications to {path}')

    raise SystemExit


def main():
    global reporting, print_classification, classifier
    args = get_args()
    # load either web or pop-up reporting based on args
    reporting_module = 'reporting.' + ('web' if args.web else 'popup')
    print("Loading " + reporting_module)
    reporting = importlib.import_module(reporting_module)

    classifier = Classifier(args.age_gender)

    # if process is killed with ctrl+c display stats
    signal.signal(signal.SIGINT, sigint_handler)

    if args.video is not None:
        cap = cv2.VideoCapture(args.video)
        frame_nr = 0
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.resize(frame, None, fx=0.25, fy=0.25)
            if frame_nr % 4 == 0:
                every_frame(frame, time.time())
            frame_nr += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                raise SystemExit
        return

    if args.file is not None:
        frame = cv2.imread(args.file)
        every_frame(frame, time.time())
        if cv2.waitKey() & 0xFF == ord('q'):
            raise SystemExit
        return

    if args.print_classification:
        print_classification = True

    # on every frame from the stream run stuff
    stream_video(every_frame)


def get_args():
    parser = argparse.ArgumentParser(description="This script will launch the project",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--web", type=bool, default=False,
                        help="Serve web-page instead of showing pop-up")
    parser.add_argument("--file", type=str, default=None,
                        help="Run on image instead of webcam")
    parser.add_argument("--age_gender", type=str, default='yu4u_age_gender.age_gender',
                        help="Classifier to use for age and gender, options are: yu4u_age_gender.age_gender or insightface_gender_age.classify")
    parser.add_argument("--video", type=str, default=None,
                        help="Run on video instead of webcam")
    parser.add_argument("--print_classification", type=bool, default=False,
                        help="Print classification as we get them")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
