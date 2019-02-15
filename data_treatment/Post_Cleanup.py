

def cleanup(rawData):

    unprocessedData = rawData
    processedData = []

    i = 0
    for element in unprocessedData:
        i += element[0]

    i /= len(unprocessedData)

    processedData.append(int(i))

    counter = 0
    for element in unprocessedData:
        if(element[1] == "M"):
            counter += 1
        elif(element[1] == "F"):
            counter -= 1

    if(counter >=0):
        processedData.append("M")
    elif(counter < 0):
        processedData.append("F")

    print(processedData)
