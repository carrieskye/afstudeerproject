from classifier.gender import classify_gender
from classifier.emotion import classify_emotion


def classify(frame):
    gender_label = classify_gender(frame)
    emotion_label = classify_emotion(frame)
    print("GENERAL CLASSIFIER", gender_label, " ", emotion_label)
    new_classification = Classification(gender_label, emotion_label)
    return new_classification


class Classification:

    def __init__(self, gender, emotion):
        self.gender = gender
        self.emotion = emotion

    def __str__(self):
        return "[" + self.gender + ", " + self.emotion
