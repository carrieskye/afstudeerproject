import cv2
import numpy

blue = (225, 105, 65)
green = (87, 139, 46)
red = (60, 20, 220)
yellow = (32, 165, 218)
white = (255, 255, 255)
font = cv2.FONT_HERSHEY_DUPLEX


def annotate_frame(original_frame, faces, labels, copy=False):
    """Put labels for each face on the frame"""
    # if we want to keep the original frame fresh
    frame = numpy.copy(original_frame) if copy else original_frame

    for index, (x, y, w, h) in enumerate(faces):
        xw, yh = x + w, y + h
        label = f'{labels[index].name} ({labels[index].age} {labels[index].gender} {labels[index].emotion})'
        colour = get_colour(labels[index])

        # draw rectangles around the face
        cv2.rectangle(frame, (x, y), (xw, yh), colour, 2)
        # add filled box
        cv2.rectangle(frame, (x - 1, y), (xw + 1, y - 20), colour, cv2.FILLED)
        # put label in the filled box
        cv2.putText(frame, label, (x + 1, y - 4), font, .6, white, 1)

    return frame


def get_colour(label):
    if label.gender == 'F':
        return red if label.age > 12 else yellow
    else:
        return blue if label.age > 12 else green
