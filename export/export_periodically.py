from apscheduler.schedulers.background import BackgroundScheduler
from json import dumps

# data to export
data = []

scheduler = BackgroundScheduler()

back_office_api = 'http://localhost:8080/api/'


def log(item):
    data.append(item)


def export_for_back_office():
    return [{
        'personId': classification.name,
        'gender': 'MALE' if classification.gender == 'M' else 'FEMALE',
        'emotion': classification.emotion.upper(),
        'age': classification.age,
        'timestamp': classification.timestamp,
    } for classification in data]


def save_to_file(path='./dump.json'):
    def obj_dict(obj):
        return obj.__dict__

    with open(path, 'w') as f:
        f.write(dumps(export_for_back_office(), default=obj_dict))

    print(f'Saved {len(data)} classifications to {path}')


def send_to_back_office():
    pass
