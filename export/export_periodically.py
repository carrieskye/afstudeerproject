from json import dumps

import requests
from apscheduler.schedulers.background import BackgroundScheduler

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
    def obj_dict(obj):
        return obj.__dict__

    # authentication
    login = {'username': 'admin', 'rememberMe': True, 'password': 'admin'}
    login_json = dumps(login, default=obj_dict)

    r = requests.post(back_office_api + 'authenticate',
                      headers={'Content-Type': 'application/json'},
                      data=login_json)

    token = str(r.json()['id_token'])

    # export data
    data_json = dumps(export_for_back_office(), default=obj_dict)
    store_id = '1001'

    requests.post(back_office_api + 'devices/' + store_id + '/export/',
                  headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
                  data=data_json)

    print(f'Saved {len(data)} classifications to Back Office')
