class Capture:

    def __init__(self, start, timestamp, hit):
        self.timestamp = timestamp
        self.timestamp_relative = timestamp - start
        self.hit = hit

    def __str__(self):
        return ("HIT" if self.hit else "FAIL") + " [" + str(format(self.timestamp_relative, '.2f')) + "s] "
