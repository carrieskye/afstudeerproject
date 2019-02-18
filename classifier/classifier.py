from classifier.gender import classify_gender
from classifier.emotion import classify_emotion
from classifier.age_gender import start_classifier_stream


def classify_stream(frames):
    classifications = []
    for frame in frames:
        classification = classify(frame)
        print(classification)
        classifications.append(classification)
    return classifications[len(classifications) - 1]


def classify(frame):
    gender_label = classify_gender(frame)
    emotion_label = classify_emotion(frame)

    age_gender_label = start_classifier_stream(frame)
    gender2_label = age_gender_label[0]
    age_label = age_gender_label[1]

    new_classification = Classification(gender_label, gender2_label, emotion_label, age_label)
    return new_classification


class Classification:

    def __init__(self, gender, gender2, emotion, age):
        self.gender = gender
        self.gender2 = gender2
        self.emotion = emotion
        self.age = age

    def __str__(self):
        return "[" + str(self.gender) + ", " + str(self.gender2) + ", " + str(self.emotion) + ", " + str(self.age) + "]"
