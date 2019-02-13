import cv2
import time
import math

cascadaPath = './models/opencv/haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascadaPath)


def get_hit_ratio():
    if face_hits + no_face_hits == 0:
        return 0
    return math.floor(10000 * face_hits / (face_hits + no_face_hits)) / 100


# global face and no face hits
face_hits = 0
no_face_hits = 0
hit_streak = 0
hit_streak_ongoing = False
fail_streak = 0

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

    # we keep track of the number of hits and fails in a row
    if len(faces) > 0:
        hit_streak += 1
        fail_streak = 0
    else:
        hit_streak = 0
        fail_streak += 1

    # if there's five hits in a row, we assume there's someone behind the camera
    if hit_streak >= 10:
        hit_streak_ongoing = True

    # if there's a person behind the camera, we keep track of the hit ratio to see if the person is still there
    if hit_streak_ongoing:
        if len(faces) > 0:
            face_hits += 1
        else:
            no_face_hits += 1

    if get_hit_ratio() < 50 or fail_streak > 10:
        hit_streak_ongoing = False
        face_hits = 0
        no_face_hits = 0

    print(face_hits, "-", no_face_hits, " -> ", get_hit_ratio(), "% | streak=", hit_streak, "| ongoing =",
          hit_streak_ongoing)

    # calculating fps and displaying
    fps = round(capturedFrames / (time.time() - start))
    cv2.putText(frame, "fps:" + str(fps), (0, 25), 2, 1, (255, 255, 255))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if hit_streak_ongoing:
        cv2.putText(frame, "Detected", (25, 100), 2, 1, (0, 0, 0), 2)  # Draw the text

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # press q to stop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
