from flask import Flask, render_template, Response
import cv2
import threading
import time

app = Flask(__name__)

current_frame = None
changed = False


def show_frame(frame):
    global current_frame
    global changed
    current_frame = frame
    changed = True


def get_latest_frame():
    global current_frame
    global changed
    while True:
        if changed:
            changed = False
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', current_frame)[1].tobytes() + b'\r\n\r\n')
        time.sleep(0.1)


@app.route('/')
def index():
    return render_template('web_app_flask.html')


@app.route('/video_viewer')
def video_viewer():
    return Response(get_latest_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


threading.Thread(target=app.run).start()
