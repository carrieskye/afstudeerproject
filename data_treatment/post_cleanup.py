def cleanup(raw_data):
    unprocessed_data = raw_data
    processed_data = []

    i = 0
    for element in unprocessed_data:
        i += element[0]

    i /= len(unprocessed_data)

    processed_data.append(int(i))

    counter = 0
    for element in unprocessed_data:
        if element[1] == "M":
            counter += 1
        elif element[1] == "F":
            counter -= 1

    if counter >= 0:
        processed_data.append("M")
    elif counter < 0:
        processed_data.append("F")

    return processed_data
