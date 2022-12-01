import random
import bisect

from mss.event import Event, EventType
from mss.generator import Generator
from mss.memory import Memory
from mss.processor import Processor

from mss.distributions import Uniform, Normal

class FutureEvents:

    def __init__(self):
        self.events = list()

    def all_events(self):
        return self.events

    def add(self, event: Event):
        bisect.insort(self.events, event)

    def next(self) -> Event:
        return self.events.pop(0)


class EventModel:

    def __init__(self
                 , generator
                 , memory
                 , processor
                 , requests_num=1000
                 , repeat_percent=0):
        self.generator = generator
        self.memory = memory
        self.processor = processor
        self.requests_num = requests_num
        self.repeat_percent= repeat_percent


    def run(self):
        self.processor.set_aviable(True)
        #print(self.memory.cur_len)

        processed_requests = 0
        total_requests = self.requests_num
        events = FutureEvents()

        events.add(Event(self.generator.next_time(), EventType.GENERATOR))

        gen_num = 0
        proc_num = 0

        while processed_requests < total_requests:
            #print("NEW EVENT")
            cur_event = events.next()
            #print(cur_event)

            if cur_event.event_type == EventType.GENERATOR:
                #print(f"GENERATE {gen_num + 1} {cur_event.time}")
                self.memory.insert_request()
                events.add(Event(cur_event.time + self.generator.next_time(),
                                 EventType.GENERATOR))
                gen_num += 1

            if cur_event.event_type == EventType.PROCESSOR:
                #print(f"{proc_num + 1} end process time {cur_event.time}")
                #print("End process")
                processed_requests += 1
                if random.randint(0, 100) < self.repeat_percent:
                    #print("Repeat!!!")
                    self.memory.insert_request()
                    #total_requests += 1
                self.processor.set_aviable(True)

            if self.processor.is_aviable():
                #print(self.memory.is_empty())
                if not self.memory.is_empty():
                    #print(f"Begin process {proc_num + 1}")
                    self.memory.remove_request()
                    self.processor.set_aviable(False)
                    #print(self.processor.is_aviable())
                    events.add(Event(cur_event.time +
                                     self.processor.process_time(),
                                     EventType.PROCESSOR))
            #print(f"Memory size: {self.memory.cur_len}")
            #print(f"Events: {[str(x) for x in events.all_events()]}")
            #print()

        print("\nEVENT MODEL")
        print(f"Repeat: {self.repeat_percent}")
        print(f"Requests: {total_requests}")
        print(f"Repeats: {total_requests - self.requests_num}")
        print(f"Time: {cur_event.time}")
        print(f"Max len: {self.memory.max_len}")

        return self.memory.max_len


if __name__ == "__main__":
    model = EventModel(
            Generator(Uniform(2, 4)),
            Memory(),
            Processor(Normal(100, 1)),
            10,
            0
            )
    model.run()

