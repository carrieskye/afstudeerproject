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

        # check if this face is not already present in encodings
        if name in known_face_names:
            print(f'Encoding for {name} already exists')
            continue
        # full name path
        file_path = join(directory, file)

        # load the first found encoding
        encoding = face_recognition.face_encodings(face_recognition.load_image_file(file_path))[0]
        # if encoding in known_face_encodings:
        #     print(f'Encoding for {name} is already in the list')
        #     continue
        # append to encodings and names
        known_face_encodings.append(encoding)
        known_face_names.append(name)


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


def get_identifications(frame, _faces, new_face_callback=None):
    """Returns array with names of people"""
    # we get all encodings for the faces
    rgb_small_frame = frame[:, :, ::-1]

    # opencv is x y w h
    # dlib   is t r b l
    faces = [(y, x + w, y + h, x) for (x, y, w, h) in _faces]

    face_encodings = face_recognition.face_encodings(rgb_small_frame, faces)
    # we create an array that has as many places as the faces we got
    names = [""] * len(faces)

    # for every encoding of a face
    for index, encoding in enumerate(face_encodings):
        # search it in the known_faces
        has = False
        distances = face_recognition.face_distance(known_face_encodings, encoding)

        for dist in distances:
            if dist < max_face_distance:
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
