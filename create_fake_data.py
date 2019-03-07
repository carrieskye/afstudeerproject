import argparse
import random
from datetime import datetime
from json import dumps

from classifier.classification import Classification
from positioning.simple import Position

today = datetime.today().replace(hour=9,
                                 minute=5,
                                 second=0,
                                 microsecond=0)

parser = argparse.ArgumentParser(description="Script to create random classifications in dump.json",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--date",
                    type=lambda d: datetime.strptime(d, '%Y%m%d').replace(hour=9, minute=5),
                    default=today,
                    help="Date for which data will be generated")

parser.add_argument("--busy_rating",
                    type=int,
                    default=5,
                    help="Rating for how busy the store is from 0 to 10")

args = parser.parse_args()
data_date = args.date
busy_rating = args.busy_rating

data = []
timestamps = [x for x in range(int(datetime.timestamp(data_date)), int(datetime.timestamp(data_date)) + 39000, 900)]
emotions = ['ANGRY', 'DISGUST', 'FEAR', 'HAPPY', 'SAD', 'SURPRISE', 'NEUTRAL']

males = [1, 2, 2, 3, 4, 4, 5, 5,
         6, 6, 7, 6, 5, 5, 4, 4,
         4, 5, 5, 6, 6, 7, 7, 7,
         7, 7, 7, 7, 8, 9, 9, 10,
         10, 11, 12, 12, 11, 10, 9, 9,
         8, 6, 5, 6]

females = [0, 1, 1, 2, 2, 3, 3, 4,
           4, 5, 5, 5, 4, 4, 4, 4,
           5, 6, 7, 7, 8, 8, 8, 8,
           9, 9, 9, 9, 10, 10, 10, 11,
           11, 10, 11, 10, 9, 9, 8, 8,
           7, 5, 5, 6]


def export_for_back_office():
    return [{
        'personId': classification.name,
        'gender': 'MALE' if classification.gender == 'M' else 'FEMALE',
        'emotion': classification.emotion.upper(),
        'age': classification.age,
        'timestamp': classification.timestamp,
    } for classification in data]


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


random_position = Position(0, 0)
random_name = 10000

for index, value in enumerate(timestamps):
    random_extras = random.randint(0, busy_rating)
    for i in range(0, males[index] * busy_rating + random_extras):
        data.append(Classification(value, random_name, random_position, 'M', random_emotion(), random_age()))
        random_name += 1

    random_extras = random.randint(0, busy_rating)
    for i in range(0, females[index] * busy_rating + random_extras):
        data.append(Classification(value, random_name, random_position, 'F', random_emotion(), random_age()))
        random_name += 1

save_to_file()
