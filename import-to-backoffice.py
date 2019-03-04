import requests
import json
import argparse

parser = argparse.ArgumentParser(description="Script to import json dumps to backoffice", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--backoffice_url", type=str, default='http://localhost:8080/api/', help="API url")
parser.add_argument("--file", type=str, default='dump.json', help="File to import")
parser.add_argument("--device_id", type=str, default='1001', help="Device ID to use for import")

args = parser.parse_args()

back_office_api = args.backoffice_url
file = args.file
device_id = args.device_id

with open(file, 'r') as f:
    data = json.load(f)
    requests.post(back_office_api + 'devices/' + device_id + '/export',
                  headers={'Content-Type': 'application/json'},
                  data=json.dumps(data))
