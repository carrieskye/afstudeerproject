import cv2
import numpy as np

from keras.models import load_model

from .utils.datasets import get_labels
from .utils.inference import detect_faces
from .utils.inference import draw_text
from .utils.inference import draw_bounding_box
from .utils.inference import apply_offsets
from .utils.inference import load_detection_model
from .utils.preprocessor import preprocess_input

# parameters for loading data and images
detection_model_path = './models/face_classification/detection/haarcascade_frontalface_default.xml'
gender_model_path = './models/face_classification/gender/simple_CNN.81-0.96.hdf5'
gender_labels = get_labels('imdb')
font = cv2.FONT_HERSHEY_SIMPLEX

# hyper-parameters for bounding boxes shape
frame_window = 10
gender_offsets = (30, 60)

# loading models
face_detection = load_detection_model(detection_model_path)
gender_classifier = load_model(gender_model_path, compile=False)

# getting input model shapes for inference
gender_target_size = gender_classifier.input_shape[1:3]

# starting lists for calculating modes
gender_window = []


def classify_gender(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detect_faces(face_detection, gray_image)
    gender_text = 'unknown'

    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, gender_offsets)

        rgb_face = rgb_image[y1:y2, x1:x2]
        try:
            rgb_face = cv2.resize(rgb_face, gender_target_size)
        except:
            continue
        rgb_face = np.expand_dims(rgb_face, 0)
        rgb_face = preprocess_input(rgb_face, False)

        gender_prediction = gender_classifier.predict(rgb_face)
        gender_label_arg = np.argmax(gender_prediction)
        gender_text = gender_labels[gender_label_arg]
        gender_window.append(gender_text)

    return 'M' if gender_text == 'man' else 'F' if gender_text == 'woman' else 'unknown'
