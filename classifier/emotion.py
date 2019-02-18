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
emotion_model_path = './models/face_classification/emotion/fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013')
font = cv2.FONT_HERSHEY_SIMPLEX

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []


def classify_emotion(frame):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(face_detection, gray_image)
    emotion_text = "unknown"

    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)

        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, emotion_target_size)
        except:
            continue
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        gray_face = preprocess_input(gray_face, False)

        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

    return emotion_text
