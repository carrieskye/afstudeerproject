import cv2
import sys
import time
from picamera.array import PiRGBArray
from picamera import PiCamera


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

# Use flask for web app
from flask import Flask, render_template, Response
app = Flask(__name__)

#cascPath = sys.argv[1]
#cascPath = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
#cascPath = '../opencv-haarcascades/haarcascade_eye.xml'
#cascPath = '../opencv-haarcascades/haarcascade_fullbody.xml'
#cascPath = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
cascadaPath = './models/opencv/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadaPath)

def process_facerecognition():
    video_capture = cv2.VideoCapture(0)
    capturedFrames = 0
    start = time.time()
    #while True:
    for rawframe in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Capture frame-by-frame
        #ret, frame = video_capture.read()
        frame = rawframe.array
        capturedFrames += 1

        # to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        fps = round(capturedFrames / (time.time() - start))
        cv2.putText(frame, "fps:"+ str(fps), (0, 25), 2, 1, (255, 255, 255))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        #cv2.imshow('Video', gray)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cv2.imencode(".jpg", frame)[1].tobytes() + b'\r\n\r\n')
        rawCapture.truncate(0)
        

        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break

    # When everything is done, release the capture
    video_capture.release()
    #cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('web_app_flask.html')

# Entry point for web app
@app.route('/video_viewer')
def video_viewer():
    return Response(process_facerecognition(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    print("\n\nNote: Open browser and type http://127.0.0.1:5000/ or http://ip_address:5000/ \n\n")
    # Run flask for web app
    app.run(host='0.0.0.0', threaded=False, debug=False)
