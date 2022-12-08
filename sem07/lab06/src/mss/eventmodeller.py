import random
import bisect
import time

from typing import Union

from mss.event import Event
from mss.generator import TheatergoersGenerator
from mss.memory import Memory
from mss.processor import Processor, ProcessorVIP

from mss.distributions import Uniform, Normal

EPS = 1e-4

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

            print("NEW EVENT")
            print("time", curTime)
            print("in", theatergoersInTheator)
            print("gen", theatergoersGenerated)
            for i, ev in enumerate(events):
                #print(ev)
                if isinstance(ev.eventBlock, Processor):
                    print(f"Канал {i} {ev.eventBlock}")
                    print(ev.eventBlock.GetQueueLength())

            for block in self.blocks:
                if abs(block.NextEvent.Time - curTime) < EPS:
                    if not isinstance(block.NextEvent.EventBlock, Processor):
                        print("Gen")
                        block.TransmitRequest()

                        #print(block.NextEvent.EventBlock)
                        if theatergoersGenerated < self.theatergoersNum:
                            block.GenerateNextEvent(curTime)
                            print(block.requestsNum)
                            theatergoersGenerated += block.requestsNum
                        else:
                            block.NextEvent.time = -1
                    else:
                        print("Proc")
                        block.EndProcess(curTime)
                        if not isinstance(block, ProcessorVIP):
                            theatergoersInTheator += 1


        print(curTime)
        return curTime


if __name__ == "__main__":
    gen = Generator(Uniform(1, 2), None)
    proc = Processor(gen, Memory())

    print(type(gen.NextEvent.eventBlock))
    print(type(proc.NextEvent.eventBlock))

    #model = EventModel(
    #        Generator(Uniform(2, 4)),
    #        Memory(),
    #        Processor(Normal(100, 1)),
    #        10,
    #        0
    #        )
    #model.run()

