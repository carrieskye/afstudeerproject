import argparse
import importlib

import cv2
import time

from annotate.simple import annotate_frame
from cameras.laptop_cam import stream_video
from classifier.classifier import classify
from data_treatment.post_processor import get_overall_classification
from detectors.simple import detect_face
from recognition.identify import get_identifications

# Reporting is loaded based on arguments, see main()
# TODO: this is not ideal since IDE's cannot work with this
reporting = None

# cascade to use with opencv to identify faces
cascadePath = './models/opencv/haarcascade_frontalface_default.xml'

# dictionary with person -> classifications
people = {}


def opencv_format_to_css(opencv_format):
    # css format is: top, right, bottom, left and used by face_recognition
    (x, y, w, h) = opencv_format
    return x, y, x+w, y+h


def every_frame(frame, timestamp):
    # get faces from detector
    faces = detect_face(frame, cascadePath)

    # convert opencv coordinates to css format
    faces_css = [opencv_format_to_css(face) for face in faces]

    # get identifications for the faces
    people_in_frame = get_identifications(frame, faces_css)

    # labels for each person in the frame
    labels = []

    # here we want the iterate over the identified persons and classify them
    for index, face in enumerate(faces):
        # get the name of the current face
        name = people_in_frame[index]

        # get classification for this face
        classification = classify(frame, face, timestamp)

        # if this is the first time initialise in the people dictionary
        if name not in people:
            people[name] = []

        # append this classification
        people[name].append(classification)

        # get average age, most common gender and last emotion
        average_age, most_common_gender, last_emotion = get_overall_classification(people[name])

        label = f'{name} ({average_age}/{most_common_gender}/{last_emotion})'
        labels.append(label)

    # TODO: determine when to send the labels with label_action

    # annotate the frame
    annotate_frame(frame, faces_css, labels)

    # show the person we detected
    reporting.show_frame(frame)


def label_action(labels):
    reporting.show_detected(labels)


def main():
    global reporting
    args = get_args()
    # load either web or pop-up reporting based on args
    reporting_module = 'reporting.' + ('web' if args.web else 'popup')
    print("Loading " + reporting_module)
    reporting = importlib.import_module(reporting_module)

    if args.file is not None:
        frame = cv2.imread(args.file)
        every_frame(frame, time.time())
        if cv2.waitKey() & 0xFF == ord('q'):
            raise SystemExit
        return

    # on every frame from the stream run stuff
    stream_video(every_frame)


def get_args():
    parser = argparse.ArgumentParser(description="This script will launch the project",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--web", type=bool, default=False,
                        help="Serve web-page instead of showing pop-up")
    parser.add_argument("--file", type=str, default=None,
                        help="Run on image instead of webcam")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
