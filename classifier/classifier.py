from classifier.age_gender import start_classifier_stream
from classifier.emotion import classify_emotion

classifications = {}


def start_classify_stream(person_id, frames, callback_when_done):
    if person_id not in classifications.keys():
        classifications[person_id] = []

    callback_when_done(classify_stream(person_id, frames))


def classify_stream(person_id, frames):
    """Will start classifying all frames and run the callback"""
    for frame in frames:
        classification = classify(frame)
        classifications[person_id].append(classification)
    return classifications[person_id]


def classify(frame):
    age_gender_label = start_classifier_stream(frame)

    gender_label = age_gender_label[1]
    emotion_label = classify_emotion(frame)
    age_label = age_gender_label[0]

    new_classification = Classification(gender_label, emotion_label, age_label)
    return new_classification


def get_classifications():
    return classifications


def get_classifications_of_person(person_id):
    return classifications[person_id]


class Classification:

    def __init__(self, gender, emotion, age):
        self.gender = gender
        self.emotion = emotion
        self.age = age

    def __str__(self):
        return "[" + str(self.gender) + ", " + str(self.emotion) + ", " + str(self.age) + "]"
