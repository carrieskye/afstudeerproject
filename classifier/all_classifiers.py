from classifier.gender import classify_gender
from classifier.emotion import classify_emotion
from classifier.age_gender import startClassifierStream


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

    age_gender_label = startClassifierStream(frame)
    gender2_label = age_gender_label[0]
    age_label = age_gender_label[1]

    new_classification = Classification(gender_label, emotion_label, gender2_label, age_label)
    return new_classification


class Classification:

    def __init__(self, gender, emotion, gender2, age):
        self.age = age
        self.gender = gender
        self.gender2 = gender2
        self.emotion = emotion

    def __str__(self):
        return "[" + self.gender + ", " + self.emotion
