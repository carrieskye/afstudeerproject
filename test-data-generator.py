from json import dumps
from time import time
from random import random
from export.export_periodically import save_to_file, log
from classifier.classification import Classification

classifications = 0
males = 0
females = 0


def result(personId, gender, emotion, age, timestamp):
    global classifications
    classifications += 1
    log(Classification(timestamp, personId, None, gender, emotion, age))


gender = 'M'
age = 20
people = 1
timestamp = time() - 60 * 60 * 8 * 100
while timestamp < time():
    # increase with 1 second
    timestamp += 60 * 10

    age = int(random()*100)
    for i in range(0, 15):
        result(str(people), gender, 'HAPPY', age, timestamp + (0.06 * i))
        pass
    if random() > 0.7:
        gender = 'F' if random() > .5 else 'M'
        if gender == 'MALE': males += 1
        if gender == 'FEMALE': females += 1
        people += 1

print(f"done, generated {classifications} classifications, {people} different people")
print(f"{males} males, {females} females")
save_to_file()

