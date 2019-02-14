from random import random


def classify(face):
    return 'MALE' if random() * 2 > 1 else 'FEMALE'
