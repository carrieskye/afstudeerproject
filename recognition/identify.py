from os import listdir
from os.path import isfile, join, splitext, dirname, realpath
import pickle

import face_recognition
import numpy as np

# here we store 128 point encodings
known_face_encodings = []

# here we store the matching names
known_face_names = []

# path for database to store face_encodings
database_path = './recognition/database/database.dat'

# max distance when comparing faces
max_face_distance = 0.6


def load_faces_from_directory(directory):
    """Loads people from supplied directory as known people based on filename"""
    # get all files (not directories)
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    # for every file
    for file in files:
        # split of name
        name, ext = splitext(file)

        # full name path
        file_path = join(directory, file)

        # load the first found encoding
        encoding = face_recognition.face_encodings(face_recognition.load_image_file(file_path))[0]

        add_encoding(name, encoding)


def add_encoding(name, encoding, check_for_existing=True):
    """Add encoding and matching name to current known encodings"""
    # check if this face is not already present in encodings
    if name in known_face_names:
        print(f'Encoding for {name} already exists')
        return False

    # check if there are encodings that already match
    if check_for_existing and len(known_face_encodings) > 0:
        distances = face_recognition.face_distance(known_face_encodings, encoding)
        closest_match_index = np.argmin(distances)
        if distances[closest_match_index] < max_face_distance:
            print(f'Encoding for {name} already matches {known_face_names[closest_match_index]}')
            return False

    # add encoding and name to encodings
    known_face_encodings.append(encoding)
    known_face_names.append(name)

    return True


def load_encodings_from_database(path=database_path):
    """Load encodings from pickle file"""
    try:
        with open(path, 'rb') as f:
            for key, value in pickle.load(f).items():
                known_face_names.append(key)
                known_face_encodings.append(value)
            print(f'Loaded {len(known_face_names)} encodings from {path}')
    except FileNotFoundError:
        print(f'Database {path} not found, will be created at script end (ctrl+c)')
    except EOFError:
        raise Exception(f'Cannot load data from {path}')


def persist(path=database_path):
    """Save encodings to pickle file"""
    all_data = {}

    # Create dictionary with name -> encoding
    for index, encoding in enumerate(known_face_encodings):
        name = known_face_names[index]
        all_data[name] = encoding

    # save to pickle!
    with open(path, 'wb') as f:
        pickle.dump(all_data, f)
    print(f'Saved {len(all_data)} encodings to {path}')


# load faces from ./people directory
load_faces_from_directory(join(dirname(realpath(__file__)), './people'))


# load faces from ./people directory
load_faces_from_directory(join(dirname(realpath(__file__)), './people'))


def get_identifications(frame, _faces):
    """Returns array with names of people"""
    # we get all encodings for the faces
    rgb_small_frame = frame[:, :, ::-1]

    # opencv is x y w h
    # dlib   is t r b l
    faces = [(y, x + w, y + h, x) for (x, y, w, h) in _faces]

    # we create an array that has as many places as the faces we got
    names = [""] * len(faces)

    # for every face create an encoding
    face_encodings = face_recognition.face_encodings(rgb_small_frame, faces)

    # for every encoding of a face
    for index, encoding in enumerate(face_encodings):
        # search it in the known_faces
        distances = face_recognition.face_distance(known_face_encodings, encoding)

        # check if this face is known
        if len(distances) > 0:
            best_match_index = np.argmin(distances)
            distance = distances[best_match_index]
            if distance < max_face_distance:
                # we found a match
                name = known_face_names[best_match_index]
                names[index] = name
                continue

        # if none are found we save this one too
        name = len(known_face_names)
        add_encoding(name, encoding, check_for_existing=False)
        names[index] = name

    return names
