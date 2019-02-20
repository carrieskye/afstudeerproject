from .classification import Classification
from classifier.age_gender import classify as classify_age_gender
from classifier.emotion import classify as classify_emotion


def classify(frame, face):
    """Will return a classification for the supplied coordinates of the face in the supplied frame"""
    # age and gender
    age_label, gender_label, _ = classify_age_gender(frame, face)
    # emotion
    emotion_label = classify_emotion(frame, face)

    return Classification(gender_label, emotion_label, age_label)
