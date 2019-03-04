import sys
import requests
from easygui import msgbox, choicebox, ccbox, indexbox

r = requests.get('http://localhost:8080/api/devices')
devices = r.json()
devices_list = ['{} {}'.format(device['name'], device['postalCode']) for device in devices]
choice = choicebox("Which device is this?", "Device selection", devices_list)
try:
    if choice is None:
        raise ValueError
    index = devices_list.index(choice)
    device = devices[index]
except ValueError:
    print("Invalid choice")
    pass
