import time
from typing import Callable

from picamera import PiCamera
from picamera.array import PiRGBArray


def stream_video(result_callback: Callable):
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    raw_capture = PiRGBArray(camera, size=(640, 480))

    # allow the camera to warm up
    time.sleep(0.1)

    for raw_frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        frame = raw_frame.array
        result_callback(frame)
        raw_capture.truncate(0)
