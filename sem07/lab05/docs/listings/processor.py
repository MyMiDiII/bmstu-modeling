class Processor(Generator):
    def __init__(self, generator: Generator, memory: Memory):
        super().__init__(generator.distribution, generator.receivers)
        self.nextEvent.eventBlock = self
        self.memory = memory
        self.aviable = True

    def TakeRequest(self, curTime) -> bool:
        if self.aviable:
            self.aviable = False
            self.GenerateNextEvent(curTime)
            return True
        return self.memory.InsertRequest()

    def EndProcess(self, curTime):
        self.TransmitRequest()
        if not self.memory.IsEmpty():
            self.memory.RemoveRequest()
            self.GenerateNextEvent(curTime)
        else:
            self.aviable = True
            self.NextEvent.Time = -1
