from collections import Counter
from functools import reduce

import numpy as np


def get_overall_classification(classifications):
    # get average age over all ages classifications
    average_age = int(reduce(np.add, (c.age for c in classifications)) / len(classifications))

    # get most common gender label
    most_common_gender = Counter(c.gender for c in classifications).most_common(1)[0][0]

    # get last emotion
    last_emotion = classifications[-1].emotion

    return average_age, most_common_gender, last_emotion
