import operator
import itertools
import numpy as np


def select_person(classifications):
    categories = {'girl': [], 'boy': [], 'woman': [], 'man': []}

    for classification in classifications:
        categories[map_to_category(classification.gender, classification.age)].append(classification)

    max_count_category = max(map(lambda val: len(val), categories.values()))

    relevant_categories = {k: v for k, v in categories.items() if len(v) == max_count_category}

    if len(relevant_categories) == 1:
        return list(relevant_categories.values())[0][0]

    # TODO: better way to get list of all classifications?
    relevant_classifications = []
    for key, value in relevant_categories.items():
        relevant_classifications += value

    biggest_classifications = get_biggest_people(relevant_classifications)
    return get_most_central_person(biggest_classifications)


def map_to_category(gender, age):
    if gender == 'M':
        return 'man' if age > 12 else 'boy'
    else:
        return 'woman' if age > 12 else 'girl'


def get_biggest_people(classifications):
    max_surface = max(map(lambda value: value.position.surface, classifications))
    min_surface = max_surface * 0.5

    return list(filter(lambda value: value.position.surface >= min_surface, classifications))


# TODO: rewrite this ugly speed solution
def get_most_central_person(classifications):
    # index_min = np.argmin(c.position.distance for c in classifications)
    smallest_distance = min(map(lambda value: value.position.distance, classifications))

    most_central_person = classifications[0]

    for classification in classifications:
        if classification.position.distance < smallest_distance:
            most_central_person = classification

    return most_central_person
