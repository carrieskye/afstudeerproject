import cv2
import numpy as np
from keras.models import load_model

from .utils.datasets import get_labels
from .utils.inference import load_detection_model

# parameters for loading data and images
detection_model_path = './models/face_classification/detection/haarcascade_frontalface_default.xml'
emotion_model_path = './models/face_classification/emotion/fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013')

# hyper-parameters for bounding boxes shape
emotion_offsets = (20, 40)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]


def apply_offsets(face_coordinates, offsets):
    x, y, width, height = face_coordinates
    x_off, y_off = offsets
    return x - x_off, x + width + x_off, y - y_off, y + height + y_off


# TODO: what the heck does this do
def preprocess_input(x, v2=True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x


def classify(frame, face):
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    x1, x2, y1, y2 = apply_offsets(face, emotion_offsets)

    # cut out the face
    gray_face = gray_image[y1:y2, x1:x2]

    try:
        # resize
        gray_face = cv2.resize(gray_face, emotion_target_size)
    except:
        return "neutral"
    # cv2.imshow("face0", gray_face)

    gray_face = np.expand_dims(gray_face, 0)
    gray_face = np.expand_dims(gray_face, -1)
    gray_face = preprocess_input(gray_face, False)

    emotion_prediction = emotion_classifier.predict(gray_face)
    emotion_label_arg = np.argmax(emotion_prediction)
    emotion_text = emotion_labels[emotion_label_arg]

    return emotion_text
