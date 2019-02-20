import cv2


def show_frame(frame):
    """Show a opencv popup with the frame"""
    cv2.imshow('Video', frame)
    # when using imshow, we need waitKey or it doesn't work
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise SystemExit


def show_detected(label):
    """Print the label"""
    print("label detected" + str(label))
