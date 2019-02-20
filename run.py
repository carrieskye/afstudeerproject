import argparse
import importlib
import numpy as np
from collections import Counter

from cameras.laptop_cam import stream_video
from classifier.classifier import classify
from detectors.simple import detect_face
from recognition.identify import get_identifications
from annotate.simple import annotate_frame

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


def every_frame(frame):
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
        classification = classify(frame, face)
        # get the name of the current face
        name_of_person = people_in_frame[index]
        # if this is the first time initialise in the people dictionary
        if name_of_person not in people:
            people[name_of_person] = []
        # append this classification
        people[name_of_person].append(classification)
        # append the name
        label = name_of_person
        # get average age over all ages predications
        label += " age:" + str(int(np.average(list(map(lambda c: c.age, people[name_of_person])))))
        # get most common gender label
        label += " " + Counter(list(map(lambda c: c.gender, people[name_of_person]))).most_common(1)[0][0]
        labels.append(label)

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

    # on every frame from the stream run stuff
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
