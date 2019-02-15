from flask import Flask, render_template, Response
import cv2
import threading
import time
from simple_websocket_server import WebSocketServer, WebSocket


app = Flask(__name__)

current_frame = None
changed = False


def show_detected(label):
    for connection in connections:
        connection.send_message('label:' + label)


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
