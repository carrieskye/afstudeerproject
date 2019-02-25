from classifier.emotion.emotion import classify as classify_emotion
from utils import TimeBlock
from .classification import Classification
from importlib import import_module


class Classifier:
    """Load classifiers"""
    def __init__(self, age_gender_classifier):
        module = 'classifier.' + age_gender_classifier
        print("Loading " + module)
        self.age_gender = import_module(module)

    def classify(self, frame, face, timestamp, name, position):
        """Will return a classification for the supplied coordinates of the face in the supplied frame"""

        # age and gender
        with TimeBlock('age_gender'):
            age_label, gender_label, _ = self.age_gender.classify(frame, face)

        # emotion
        with TimeBlock('emotion'):
            emotion_label = classify_emotion(frame, face)

        return Classification(timestamp, name, position, gender_label, emotion_label, age_label)
