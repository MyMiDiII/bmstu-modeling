class EventModel:
    def __init__(self
                 , generator:TheatergoersGenerator
                 , checkers:  list[ProcessorVIP]
                 , cloakroomAttendant: list[Processor]
                 , theatergoersNum=1000):
        self.generator = generator
        self.checkers  = checkers
        self.attendant = cloakroomAttendant
        self.blocks = [self.generator] + self.checkers + self.attendant
        self.theatergoersNum = theatergoersNum

    def run(self):
        self.generator.GenerateNextEvent(0)
        events = [block.NextEvent for block in self.blocks]

        theatergoersGenerated = self.generator.requestsNum
        theatergoersInTheator = 0

        curTime = 0
        while theatergoersInTheator < self.theatergoersNum:
            curTime = events[0].Time
            for event in events[1:]:
                if not (event.Time < 0) and event.Time < curTime or curTime < 0:
                    curTime = event.Time

            for block in self.blocks:
                if abs(block.NextEvent.Time - curTime) < EPS:
                    if not isinstance(block.NextEvent.EventBlock, Processor):
                        block.TransmitRequest()

                        if theatergoersGenerated < self.theatergoersNum:
                            block.GenerateNextEvent(curTime)
                            theatergoersGenerated += block.requestsNum
                        else:
                            block.NextEvent.time = -1
                    else:
                        block.EndProcess(curTime)
                        if not isinstance(block, ProcessorVIP):
                            theatergoersInTheator += 1

        return curTime
