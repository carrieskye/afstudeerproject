from typing import Callable

import cv2


def stream_video(result_callback: Callable):
    video_capture = cv2.VideoCapture(0)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    while True:
        ret, frame = video_capture.read()
        result_callback(frame)
    video_capture.release()
    cv2.destroyAllWindows()
