from classifier.classifier import *


def cleanup(raw_data):
    unprocessed_data = raw_data
    processed_data = []

    if len(unprocessed_data) <= 0:
        return Classification('unknown', 'unknown', -1)

    counter_gender = 0
    for element in unprocessed_data:
        if element.gender == "M":
            counter_gender += 1
        elif element.gender == "F":
            counter_gender -= 1

    if counter_gender >= 0:
        processed_data.append("M")
    elif counter_gender < 0:
        processed_data.append("F")

    processed_data.append(unprocessed_data[0].emotion)

    i = 0
    for element in unprocessed_data:
        i += element.age

    i /= len(unprocessed_data)

    processed_data.append(int(i))

    return Classification(processed_data[0], processed_data[1], processed_data[2])
