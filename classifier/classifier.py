from classifier.age_gender import start_classifier_stream
from classifier.emotion import classify_emotion
from classifier.gender import classify_gender


def classify_stream(frames):
    classifications = []
    for frame in frames:
        classification = classify(frame)
        print(classification)
        classifications.append(classification)
    return classifications[len(classifications) - 1]


def classify(frame):
    age_gender_label = start_classifier_stream(frame)

    gender_label = age_gender_label[1]
    emotion_label = classify_emotion(frame)
    age_label = age_gender_label[0]

    new_classification = Classification(gender_label, emotion_label, age_label)
    return new_classification


class Classification:

    def __init__(self, gender, emotion, age):
        self.gender = gender
        self.emotion = emotion
        self.age = age

    def __str__(self):
        return "[" + str(self.gender) + ", " + str(self.emotion) + ", " + str(self.age) + "]"
