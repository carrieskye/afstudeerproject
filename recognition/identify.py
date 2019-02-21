from os import listdir
from os.path import isfile, join, realpath, dirname, splitext

import face_recognition
import numpy as np

# here we store 128 point encodings
known_face_encodings = []

# here we store the matching names
known_face_names = []


def load_faces_from_directory(directory):
    """Loads people from supplied directory as known people based on filename"""
    # get all files (not directories)
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    for file in files:
        name, ext = splitext(file)
        file_path = join(directory, file)
        # load the first found encoding in encodings
        known_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(file_path))[0])
        known_face_names.append(name)


# load faces from ./people directory
load_faces_from_directory(join(dirname(realpath(__file__)), './people'))


def get_identifications(frame, _faces, new_face_callback=None):
    """Returns array with names of people"""
    # we get all encodings for the faces
    rgb_small_frame = frame[:, :, ::-1]

    # opencv is x y w h
    # dlib   is t r b l
    faces = [(face[1], face[2], face[3], face[0]) for face in _faces]

    face_encodings = face_recognition.face_encodings(rgb_small_frame, faces)
    # we create an array that has as many places as the faces we got
    names = [""] * len(faces)

    # for every encoding of a face
    for index, encoding in enumerate(face_encodings):
        # search it in the known_faces
        has = False
        distances = face_recognition.face_distance(known_face_encodings, encoding)

        for dist in distances:
            if dist < 0.6:
                best_match_index = np.argmin(distances)
                name = known_face_names[best_match_index]
                names[index] = name
                has = True
        if has:
            continue

        # if none are found we save this one too
        known_face_encodings.append(encoding)
        # and name him the current length of faces
        name = str(len(known_face_encodings))
        known_face_names.append(name)

        names[index] = name

        # we can also notify anyone that there's a new guy
        if new_face_callback is not None:
            # we found a new face in:
            # - frame,
            # - at these coordinates,
            # - with this encoding and
            # - we call him name
            new_face_callback(frame, faces[index], encoding, name)

    return names
