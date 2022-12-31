import random
import bisect

from typing import Union

from mss.event import Event
from mss.generator import Generator
from mss.memory import Memory
from mss.processor import Processor

from mss.distributions import Uniform, Normal

EPS = 1e-4

class EventModel:

    def __init__(self
                 , generator: Generator
                 , operators: list[Processor]
                 , computers: list[Processor]
                 , requestsNum=1000):
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

        curTime = 0
        while generatedRequests < self.requestsNum:
            print("NEW EVENT")
            for ev in events:
                print(ev)

            curTime = events[0].Time
            for event in events[1:]:
                if not event.Time < 0 and event.Time < curTime:
                    curTime = event.Time

            for block in self.blocks:
                if abs(block.NextEvent.Time - curTime) < EPS:
                    if not isinstance(block.NextEvent.EventBlock, Processor):
                        print("Gen")
                        generatedRequests += 1
                        if not block.TransmitRequest():
                            denials += 1
                        block.GenerateNextEvent(curTime)
                    else:
                        print("Proc")
                        block.EndProcess(curTime)

        print(curTime)
        return denials / generatedRequests


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

