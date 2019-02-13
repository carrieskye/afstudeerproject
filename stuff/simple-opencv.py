import cv2
import time

cascadaPath = './models/opencv/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadaPath)

video_capture = cv2.VideoCapture(0)
capturedFrames = 0
start = time.time()
while True:
    ret, frame = video_capture.read()
    capturedFrames += 1

    # to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(200, 200)
    )

    # calculating fps and displaying
    fps = round(capturedFrames / (time.time() - start))
    cv2.putText(frame, "fps:" + str(fps), (0, 25), 2, 1, (255, 255, 255))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # press q to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
