from collections import Counter
from functools import reduce
from classifier.classification import Classification

import numpy as np


def get_overall_classification(classifications):
    # if we want to use average instead:
    # average_age = int(reduce(np.add, (c.age for c in classifications)) / len(classifications))
    # get median age over all ages classifications
    median_age = int(np.median(list(c.age for c in classifications)))

    # get most common gender label
    most_common_gender = Counter(c.gender for c in classifications).most_common(1)[0][0]

    # get last timestamp, name and emotion
    last_timestamp = classifications[-1].timestamp
    last_name = classifications[-1].name
    last_position = classifications[-1].position
    last_emotion = classifications[-1].emotion

    return Classification(last_timestamp, last_name, last_position, most_common_gender, last_emotion, median_age)
