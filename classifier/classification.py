class Classification:

    def __init__(self, gender, emotion, age):
        self.gender = gender
        self.emotion = emotion
        self.age = age

    def __str__(self):
        return "[" + str(self.gender) + ", " + str(self.emotion) + ", " + str(self.age) + "]"
