from typing import Callable

import cv2


def stream_video(result_callback: Callable):
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        img = cv2.resize(frame, None, fx=0.5, fy=0.5)
        result_callback(img)
    video_capture.release()
    cv2.destroyAllWindows()
