import time

import cv2

from utils import print_row, format_percentage


class Capture:

    def __init__(self, absolute_start, timestamp, frame, hit):
        self.timestamp = timestamp
        self.timestamp_relative = timestamp - absolute_start
        self.hit = hit

        if hit:
            self.frame = frame
        else:
            self.frame = None

    def __str__(self):
        return ("HIT" if self.hit else "FAIL") + " [" + str(format(self.timestamp_relative, '.2f')) + "s] "


start = time.time()
captured_frames = 0
# print_header(19, ["FIRST", "LAST", "DIFF", "FULL-RATIO", "RECENT-RATIO", "DETECTED"])

# Collection of all captures of
#   * the captures of the [detection_duration] last milliseconds if no one is detected
#   * all captures of a person if detected
all_captures = []

# Whether a person has been detected.
detected = False

# We check for [detection_duration] milliseconds if a person is standing before the camera. This means that if in the
# last [detection_duration] milliseconds we get a hit ratio of [detection_ratio_min], a person has been detected. If the
# ratio drops below [overall_ratio_min], the person is no longer considered detected and we again keep track of the
# last [detection_duration] milliseconds.
detection_duration = 4000
detection_ratio_min = 90
overall_ratio_min = 30

# We also check the last [leaving_duration] milliseconds when someone is detected. If the ratio of this duration drops
# below the [leaving_ratio_min], we consider the person as no longer detected.
leaving_duration = 10000
leaving_ratio_min = 5

# Minimum size of a face before we let the algorithm detect it: surface = min_face_size ^ 2.
min_face_size = 100


def get_detection_hit_ratio(captures):
    # If we don't have frames, we cannot return the ratio.
    if len(captures) == 0:
        return 0

    # We iterate over the captures to count the hits and fails.
    hits = 0
    fails = 0
    for capture in captures:
        if capture.hit:
            hits += 1
        else:
            fails += 1

    # We return the percentage of hits.
    return 100 * hits / (hits + fails)


def recent_hits_ratio(now):
    # When someone is detected, [all_captures] contains all frames since the beginning. We only want to check for
    # the last [leaving_duration] milliseconds, to see if the person has moved away.
    capture_index = len(all_captures) - 1
    while all_captures[capture_index].timestamp * 1000 > (now * 1000) - leaving_duration and capture_index > 0:
        capture_index -= 1
    recent_captures = all_captures[capture_index:]

    # We then check the hit ratio of these recent captures.
    return get_detection_hit_ratio(recent_captures)


def update_captures(new_faces, frame, now):
    global detected

    # Add the new capture to the list of captures.
    new_capture = Capture(start, time.time(), frame, len(new_faces) > 0)
    all_captures.append(new_capture)

    if len(all_captures) > 0:
        # If no one is detected, we remove all capture that are older than the [detection_duration].
        while (all_captures[0].timestamp * 1000) < (now * 1000) - detection_duration and not detected:
            all_captures.pop(0)

        # If we have been saving captures for at least [detection_duration] milliseconds, we check if a person is
        # still detected.
        if (now - start) > detection_duration / 1000:
            # The person becomes detected if the ratio becomes greater than the [detection_ratio_min].
            if get_detection_hit_ratio(all_captures) > detection_ratio_min:
                detected = True
            # The person is no longer detected if the ratio becomes lower than the [overall_ratio_min] or has a
            # recent hit ratio that's lower than the [leaving_ratio_min].
            if get_detection_hit_ratio(all_captures) < overall_ratio_min \
                    or recent_hits_ratio(now) < leaving_ratio_min:
                detected = False

        # print_capture_row(now)


def print_capture_row(now):
    first = all_captures[0]
    last = all_captures[len(all_captures) - 1]
    difference = format(last.timestamp - first.timestamp, '.2f')
    full_ratio = format_percentage(get_detection_hit_ratio(all_captures))
    recent_ratio = format_percentage(recent_hits_ratio(now))
    is_detected = "YES" if detected else "NO"

    print_row(19, [str(first), str(last), difference, full_ratio, recent_ratio, is_detected])


def detect_face(frame, cascade_path):
    global captured_frames
    face_cascade = cv2.CascadeClassifier(cascade_path)
    # Take current time at beginning of every iteration
    current_time = time.time()

    captured_frames += 1

    # to greyscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(min_face_size, min_face_size)
    )

    update_captures(faces, frame, current_time)

    # Show FPS on frame
    fps = round(captured_frames / (current_time - start))
    cv2.putText(frame, "FPS: " + str(fps), (15, 30), 2, 1, (255, 255, 255))

    # Show time running on frame
    time_running = str(format(current_time - start, '.3f')) + "s"
    cv2.putText(frame, "TIME: " + time_running, (15, 60), 2, 1, (255, 255, 255))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (87, 37, 168), 2)

    # Show on frame whether a person is detected
    if detected:
        cv2.putText(frame, "DETECTED", (15, 90), 2, 1, (87, 37, 168), 2)  # Draw the text

    return detected, frame
