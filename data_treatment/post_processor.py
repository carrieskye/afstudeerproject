from classifier.classifier import *


def cleanup(unprocessed_data):
    classification = Classification('U', 'unknown', -1)

    if len(unprocessed_data) > 0:
        gender_count = {'M': 0, 'F': 0}
        emotion_count = {'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0}
        age_count = {age: 0 for age in list(range(120))}

        # iterate over classifications
        for classification in unprocessed_data:
            if classification.gender != 'U':
                gender_count[classification.gender] += 1

            if classification.emotion != 'unknown':
                emotion_count[classification.emotion] += 1

            if classification.age >= 0:
                age_count[classification.age] += 1

        # determine most frequent value for gender and emotion and average for age
        classification.gender = max(gender_count, key=gender_count.get)
        classification.emotion = max(emotion_count, key=emotion_count.get)
        classification.age = max(age_count, key=age_count.get)

    return classification
