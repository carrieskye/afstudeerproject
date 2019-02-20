import cv2
import numpy

blue = (255, 0, 0)
white = (255, 255, 255)
font = cv2.FONT_HERSHEY_DUPLEX


def annotate_frame(original_frame, faces, labels, copy=False):
    """Put labels for each face on the frame"""
    # if we want to keep the original frame fresh
    frame = numpy.copy(original_frame) if copy else original_frame

    for index, (x, y, xw, yh) in enumerate(faces):
        # draw rectangles around the face
        cv2.rectangle(frame, (x, y), (xw, yh), blue, 2)
        # add filled box
        cv2.rectangle(frame, (x-1, y), (xw+1, y-15), blue, cv2.FILLED)
        # put label in the filled box
        cv2.putText(frame, labels[index], (x + 1, y - 3), font, .5, white, 1)

    return frame

