from mss.generator import Generator
from mss.memory import Memory

class Processor(Generator):

    def __init__(self, generator: Generator, memory: Memory):
        super().__init__(generator.distribution, generator.receivers)
        self.nextEvent.eventBlock = self
        self.memory = memory
        self.aviable = True

    def ProcessTime(self):
        return self.GenerateNextEvent()

    def SetAviable(self, state=True):
        self.aviable = state

    def IsAviable(self) -> bool:
        return self.aviable

    def TakeRequest(self, curTime) -> bool:
        if self.aviable:
            self.SetAviable(False)
            self.GenerateNextEvent(curTime)
            return True

        return self.memory.InsertRequest()

    def EndProcess(self, curTime):
        self.TransmitRequest()

        if not self.memory.IsEmpty():
            self.memory.RemoveRequest()
            self.GenerateNextEvent(curTime)
        else:
            self.SetAviable(True)
            self.NextEvent.Time = -1


