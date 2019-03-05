from json import dumps
from classifier.classification import Classification
from positioning.simple import Position
import random

data = []

timestamps = []

males = [6, 8, 10, 11, 13, 14, 16, 18, 19, 21,
         18, 17, 15, 16, 14, 16, 17, 19, 23, 25,
         27, 29, 31, 32, 34, 32, 36, 38, 32, 29,
         30, 27, 26, 27, 25, 24, 20, 19, 17, 14]

females = [3, 5, 6, 8, 9, 11, 13, 14, 16, 17,
           19, 20, 19, 18, 18, 17, 20, 21, 25, 27,
           28, 32, 34, 36, 38, 40, 38, 39, 40, 41,
           42, 43, 41, 40, 39, 37, 32, 30, 29, 24]

emotions = ['ANGRY', 'DISGUST', 'FEAR', 'HAPPY', 'SAD', 'SURPRISE', 'NEUTRAL']


def export_for_back_office():
    return [{
        'personId': classification.name,
        'gender': 'MALE' if classification.gender == 'M' else 'FEMALE',
        'emotion': classification.emotion.upper(),
        'age': classification.age,
        'timestamp': classification.timestamp,
    } for classification in data]


def generate_timestamps():
    initial = 1551773100.000000
    while initial < 1551808500.000000:
        timestamps.append(initial)
        initial += 900


def random_emotion():
    emotion_index = random.randint(0, 5)
    return emotions[emotion_index]


def random_age():
    dice = random.randint(0, 5)
    return random.randint(1, 100) if dice < 1 else random.randint(5, 60) if dice < 4 else random.randint(15, 35)


def save_to_file(path='./dump.json'):
    def obj_dict(obj):
        return obj.__dict__

    with open(path, 'w') as f:
        f.write(dumps(export_for_back_office(), default=obj_dict))

    print(f'Saved {len(data)} classifications to {path}')


generate_timestamps()

random_position = Position(0, 0)
random_name = 10000

for index, value in enumerate(timestamps):
    for i in range(0, males[index]):
        data.append(Classification(value, random_name, random_position, 'M', random_emotion(), random_age()))
        random_name += 1
    for i in range(0, females[index]):
        data.append(Classification(value, random_name, random_position, 'F', random_emotion(), random_age()))
        random_name += 1

save_to_file()
