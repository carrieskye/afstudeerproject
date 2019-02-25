# from classifier.age_gender import classify as classify_age_gender
from classifier.insightface_gender_age.classify import classify as classify_insightface
from classifier.emotion import classify as classify_emotion
from utils import TimeBlock
from .classification import Classification


def classify(frame, face, timestamp, name, position):
    """Will return a classification for the supplied coordinates of the face in the supplied frame"""
    # age and gender
    # with TimeBlock('age_gender'):
    #     age_label, gender_label, _ = classify_age_gender(frame, face)

    # age and gender
    with TimeBlock('insightface'):
        age_label, gender_label, _ = classify_insightface(frame, face)
        # print(age_label, age_label2, gender_label, gender_label2)

    # emotion
    with TimeBlock('emotion'):
        emotion_label = classify_emotion(frame, face)

    return Classification(timestamp, name, position, gender_label, emotion_label, age_label)
