#from Camera import Camera
#from Detector import Detector
from classifier.Classifier import startClassifier
from data_treatment.Post_Cleanup import cleanup

camera = 0
detector = 0
dataLabel = []

def main():

    rawData = startClassifier()

    dataLabel = cleanup(rawData)
    print(dataLabel)
    #camera = Camera()
    #detector = Detector(camera)



    #while(True):
    #    if not detector.inCooldown:
    #       frames = detector.detect()
    #       detector.cooldown()
    #
    #   if not len(frames) == 0:
    #       Classifier.classify(frames)






main()