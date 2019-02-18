from classifier.classifier import *

def cleanup(raw_data):
    unprocessed_data = raw_data
    processed_data = []

    counter_gender1 = 0
    for element in unprocessed_data:
        if element.gender == "M":
            counter_gender1 += 1
        elif element.gender == "F":
            counter_gender1 -= 1

    if counter_gender1 >= 0:
        processed_data.append("M")
    elif counter_gender1 < 0:
        processed_data.append("F")

    counter_gender2 = 0
    for element in unprocessed_data:
        if element.gender2 == "M":
            counter_gender2 += 1
        elif element.gender2 == "F":
            counter_gender2 -= 1

    if counter_gender2 >= 0:
        processed_data.append("M")
    elif counter_gender2 < 0:
        processed_data.append("F")

    processed_data.append(unprocessed_data[0].emotion)

    i = 0
    for element in unprocessed_data:
        i += element.age

    i /= len(unprocessed_data)

    processed_data.append(int(i))

    return Classification(processed_data[0], processed_data[1], processed_data[2], processed_data[3])
