class Generator:
    def __init__(self, distribution, receivers):
        self.distribution = distribution
        self.receivers = receivers
        self.nextEvent = Event(-1, self)

    def GenerateNextEvent(self, curTime):
        self.nextEvent.Time = curTime + self.distribution.Generate()

    def TransmitRequest(self):
        for receiver in self.receivers:
            if receiver.TakeRequest(self.nextEvent.time):
                return True
        return False
