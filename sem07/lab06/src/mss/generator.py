import random

from mss.distributions import Distribution
from mss.event import Event

class Generator:

    def __init__(self, distribution: Distribution, receivers: list['Processor']):
        self.distribution = distribution
        self.receivers = receivers
        self.nextEvent = Event(-1, self)
        self.addParams = []

    def GenerateNextEvent(self, curTime):
        self.nextEvent.Time = curTime + self.distribution.Generate()

    def TransmitRequest(self):
        for receiver in self.receivers:
            if receiver.TakeRequest(self.nextEvent.time, *self.addParams):
                return True

        return False

    @property
    def NextEvent(self):
        return self.nextEvent


class TheatergoersGenerator(Generator):

    def __init__(self, distribution: Distribution
                     , receivers: list['Processor']
                     , probabilityVIP: float):
        super().__init__(distribution, receivers)
        self.isNextVIP = False
        self.requestsNum = 1
        self.probabilityVIP = probabilityVIP
        self.addParams = [self.isNextVIP, self.requestsNum]

    def GenerateNextEvent(self, curTime):
        super().GenerateNextEvent(curTime)
        self.isNextVIP = random.random() < self.probabilityVIP


class GroupTheatergoersGenerator(TheatergoersGenerator):

    def __init__(self, timeDistribution: Distribution
                     , numDistribution:  Distribution
                     , receivers: list['Processor']
                     , probabilityVIP: float):
        super().__init__(timeDistribution, receivers, probabilityVIP)
        self.numDistribution = numDistribution

    def GenerateNextEvent(self, curTime):
        super().GenerateNextEvent(curTime)
        self.requestsNum = self.numDistribution.Generate()
