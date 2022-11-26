import random
import bisect

from queuing_system.event import Event, EventType
from queuing_system.generator import Generator
from queuing_system.memory import Memory
from queuing_system.processor import Processor

from queuing_system.distributions import Uniform, Normal

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

        processed_requests = 0
        total_requests = self.requests_num
        events = FutureEvents()

        events.add(Event(self.generator.next_time(), EventType.GENERATOR))

        while processed_requests < total_requests:
            print("NEW EVENT")
            cur_event = events.next()
            print(cur_event)

            if cur_event.event_type == EventType.GENERATOR:
                print("Generate")
                self.memory.insert_request()
                events.add(Event(cur_event.time + self.generator.next_time(),
                                 EventType.GENERATOR))

            if cur_event.event_type == EventType.PROCESSOR:
                print("End process")
                processed_requests += 1
                if random.randint(0, 100) <= self.repeat_percent:
                    print("Repeat!!!")
                    self.memory.insert_request()
                    total_requests += 1
                self.processor.set_aviable(True)

            if self.processor.is_aviable():
                print(self.memory.is_empty())
                if not self.memory.is_empty():
                    print("Begin process")
                    self.memory.remove_request()
                    self.processor.set_aviable(False)
                    print(self.processor.is_aviable())
                    events.add(Event(cur_event.time +
                                     self.processor.process_time(),
                                     EventType.PROCESSOR))
            print(f"Memory size: {self.memory.cur_len}")
            print(f"Events: {[str(x) for x in events.all_events()]}")
            print()

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

