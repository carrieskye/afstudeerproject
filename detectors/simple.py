import cv2


def detect_face(frame, cascade_path):
    """Detects all faces on frame and returns list of (x,y,w,h) for each face"""
    face_cascade = cv2.CascadeClassifier(cascade_path)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces
