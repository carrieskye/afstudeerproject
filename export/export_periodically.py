import json
from os.path import isfile
from easygui import choicebox
import time
import requests
from apscheduler.schedulers.background import BackgroundScheduler

# data to export
data = []
scheduler = BackgroundScheduler()
back_office_api = 'http://localhost:8080/api/'
device_file = 'device.json'
last_send_timestamp = time.time()


def ask_user_for_device_selection():
    r = requests.get(f'{back_office_api}devices')
    devices = r.json()
    devices_list = ['{} {}'.format(d['name'], d['postalCode']) for d in devices]
    choice = choicebox("Which device is this?", "Device selection", devices_list)
    if choice is None:
        raise ValueError
    index = devices_list.index(choice)
    return devices[index]


def log(item):
    data.append(item)
    if time.time() - last_send_timestamp > 2:
        send_to_back_office()


def export_for_back_office():
    return [{
        'personId': classification.name,
        'gender': 'MALE' if classification.gender == 'M' else 'FEMALE',
        'emotion': classification.emotion.upper(),
        'age': classification.age,
        'timestamp': classification.timestamp,
    } for classification in data]


def obj_dict(obj):
    return obj.__dict__


def save_to_file(path='./dump.json'):

    with open(path, 'w') as f:
        f.write(json.dumps(export_for_back_office(), default=obj_dict))

    print(f'Saved {len(data)} classifications to {path}')


def send_to_back_office():
    global last_send_timestamp, data
    # export data
    data_json = json.dumps(export_for_back_office(), default=obj_dict)
    requests.post(
        url=back_office_api + 'devices/' + device_id + '/export',
        data=data_json,
        headers={'Content-Type': 'application/json'}
    )
    print(f'Saved {len(data)} classifications to Back Office')
    last_send_timestamp = time.time()
    data = []


try:
    if isfile(device_file):
        with open(device_file, 'r') as f:
            device = json.load(f)
    else:
        device = ask_user_for_device_selection()
        with open(device_file, 'w') as f:
            f.write(json.dumps(device, default=obj_dict))
except FileNotFoundError:
    print("File not found, weird")
    raise SystemExit
except EOFError:
    print("EOFERROR WHAA?")
    raise SystemExit
except requests.exceptions.ConnectionError:
    print(f"Cannot connect to '{back_office_api}devices', are you sure we have internet?")
    raise SystemExit
except ValueError:
    print(f"Please select a device!")
    raise SystemExit
except Exception as e:
    print(f"For whatever reason cannot use this device:" + str(type(e)))
    raise SystemExit


device_id = str(device['id'])
device_name = 'id={}, name={}, postalCode={}'.format(device_id, device['name'], device['postalCode'])
print("This is device:" + device_name)
