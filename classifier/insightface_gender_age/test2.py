import cv2
from classify import classify


img = cv2.imread('Tom_Hanks_54745.png')
x2, y2, _ = img.shape
print(classify(img, [0, x2, 0, y2]))

