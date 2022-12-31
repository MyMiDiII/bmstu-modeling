class EventModel:
    def __init__(self, generator: Generator, operators: list[Processor]
                 , computers: list[Processor], requestsNum=1000):
        self.generator = generator
        self.operators = operators
        self.computers = computers
        self.blocks = [self.generator] + self.operators + self.computers
        self.requestsNum = requestsNum

    def run(self):
        self.generator.GenerateNextEvent(0)
        events = [block.NextEvent for block in self.blocks]

        generatedRequests = 1
        denials = 0

        while generatedRequests < self.requestsNum:
            curTime = events[0].Time
            for event in events[1:]:
                if not event.Time < 0 and event.Time < curTime:
                    curTime = event.Time

            for block in self.blocks:
                if abs(block.NextEvent.Time - curTime) < EPS:
                    if not isinstance(block.NextEvent.EventBlock, Processor):
                        generatedRequests += 1
                        if not block.TransmitRequest():
                            denials += 1
                        block.GenerateNextEvent(curTime)
                    else:
                        block.EndProcess(curTime)

        return denials / generatedRequests
