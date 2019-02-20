import math


class Position:

    def __init__(self, surface, distance):
        self.surface = surface
        self.distance = distance

    def __str__(self):
        return "(" + str(self.surface) + ", " + str(int(self.distance)) + ")"


def get_position(frame, face):
    x, y, w, h = face

    # calculate the surface of the face
    surface = int(w * h / 1000)

    # get frame dimensions
    screen_height, screen_width, _ = frame.shape
    screen_middle = [screen_width / 2, screen_height / 2]

    # find the middle point of the face
    face_middle = [x + (w / 2), y + (h / 2)]

    # calculate distance from middle point of face to the center of the screen
    dist = math.hypot(screen_middle[0] - face_middle[0], screen_middle[1] - face_middle[1])

    return Position(surface, dist)
