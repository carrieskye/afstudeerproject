class Classification:

    def __init__(self, timestamp, name, position, gender, emotion, age):
        self.timestamp = timestamp
        self.name = name
        self.position = position
        self.gender = gender
        self.emotion = emotion
        self.age = age

    def __str__(self):
        timestamp = "[" + str(self.timestamp).ljust(18, "0") + "] "
        labels = str(self.gender) + ", " + str(self.age) + ", " + str(self.emotion)
        return timestamp + str(self.name) + ", " + str(self.position) + ", " + labels
