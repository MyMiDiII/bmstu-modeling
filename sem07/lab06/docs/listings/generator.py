class Generator:

    def __init__(self, distribution: Distribution, receivers: list['Processor']):
        self.distribution = distribution
        self.receivers = receivers
        self.nextEvent = Event(-1, self)
        self.requestsNum = 1

    def GenerateNextEvent(self, curTime):
        self.nextEvent.Time = curTime + self.distribution.Generate()

    def TransmitRequest(self):
        if not self.receivers:
            return

        receiver = min(self.receivers, key=lambda rec: rec.GetQueueLength())
        return receiver.TakeRequest(self.nextEvent.time, self.requestsNum)

    @property
    def NextEvent(self):
        return self.nextEvent


class TheatergoersGenerator(Generator):

    def __init__(self, distribution: Distribution
                     , numDistribution:  Distribution
                     , receivers: list['ProcessorVIP']
                     , probabilityVIP: float):
        super().__init__(distribution, receivers)
        self.numDistribution = numDistribution
        self.isNextVIP = False
        self.probabilityVIP = probabilityVIP
        self.addParams = [self.isNextVIP, self.requestsNum]

    def GenerateNextEvent(self, curTime):
        super().GenerateNextEvent(curTime)
        self.isNextVIP = random.random() < self.probabilityVIP
        self.requestsNum = self.numDistribution.Generate()

    def TransmitRequest(self):
        if not self.receivers:
            return

        neededRecievers = [rec for rec in self.receivers
                               if rec.isVIP == self.isNextVIP]
        receiver = min(neededRecievers, key=lambda rec: rec.GetQueueLength())

        return receiver.TakeRequest(self.nextEvent.time, self.requestsNum)
