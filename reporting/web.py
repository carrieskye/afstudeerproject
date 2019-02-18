import threading
import time
import json

import cv2
from flask import Flask, render_template, Response, send_from_directory
from simple_websocket_server import WebSocketServer, WebSocket

from classifier.classifier import Classification

app = Flask(__name__, static_url_path='')

current_frame = None
changed = False

last_labels = Classification('unknown', 'unknown', 'unknown', -1)


def show_detected(labels):
    global last_labels

    last_labels = labels

    for connection in connections:
        connection.send_message(json.dumps(labels.emotion + ' ' + labels.gender))


def show_frame(frame):
    global current_frame
    global changed
    current_frame = frame

    if last_labels.gender != 'unknown' or last_labels.gender2 != 'unknown' or \
            last_labels.emotion != 'unknown' or last_labels.age != -1:
        cv2.putText(frame, str(last_labels), (15, 120), 2, 1, (0, 0, 0))

    changed = True


def get_latest_frame():
    global current_frame
    global changed
    while True:
        if changed:
            changed = False
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', current_frame)[
                1].tobytes() + b'\r\n\r\n')
        time.sleep(0.1)


@app.route('/')
def index():
    return render_template('web_app_flask.html')


@app.route('/video_viewer')
def video_viewer():
    return Response(get_latest_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


connections = []


class SimpleEcho(WebSocket):
    def handle(self):
        # echo message back to client
        self.send_message(self.data)

    def connected(self):
        connections.append(self)

    def handle_close(self):
        connections.remove(self)


server = WebSocketServer('', 5001, SimpleEcho)
# start websocket server
threading.Thread(target=server.serve_forever).start()

# start flask server
threading.Thread(target=app.run).start()
