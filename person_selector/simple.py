import operator


def select_person(classifications):
    categories = {'girl': [], 'boy': [], 'woman': [], 'man': []}

    for classification in classifications:
        categories[map_to_category(classification.gender, classification.age)].append(classification)

    max_count_category = max(map(lambda val: len(val), categories.values()))

    relevant_categories = {k: v for k, v in categories.items() if len(v) == max_count_category}

    if len(relevant_categories) == 1:
        return list(relevant_categories.values())[0][0]

    biggest_classifications = get_biggest_person(relevant_categories)
    return get_most_central_person(biggest_classifications)


def map_to_category(gender, age):
    if gender == 'M':
        return 'man' if age > 12 else 'boy'
    else:
        return 'woman' if age > 12 else 'girl'


# TODO: rewrite this ugly speed solution
def get_biggest_person(relevant_categories):
    max_surface = 0
    for key, value in relevant_categories.items():
        for classification in value:
            if classification.position.surface > max_surface:
                max_surface = classification.position.surface

    min_surface = max_surface * 0.8

    biggest_classifications = []
    for key, value in relevant_categories.items():
        for classification in value:
            if classification.position.surface >= min_surface:
                biggest_classifications.append(classification)

    return biggest_classifications


# TODO: rewrite this ugly speed solution
def get_most_central_person(biggest_classifications):
    smallest_distance = biggest_classifications[0].position.distance
    most_central_person = biggest_classifications[0]

    for classification in biggest_classifications:
        if classification.position.distance < smallest_distance:
            smallest_distance = classification.position.distance
            most_central_person = classification

    return most_central_person
