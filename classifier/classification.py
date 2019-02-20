class Classification:

    def __init__(self, timestamp, name, gender, emotion, age):
        self.timestamp = timestamp
        self.name = name
        self.gender = gender
        self.emotion = emotion
        self.age = age

    def __str__(self):
        timestamp = "[" + str(self.timestamp).ljust(18, "0") + "] "
        labels = str(self.name)+ ", "+ str(self.gender) + ", " + str(self.emotion) + ", " + str(self.age)
        return timestamp + labels
