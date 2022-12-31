import random
import bisect

from time import sleep

from queuing_system.event import Event, EventType
from queuing_system.generator import Generator
from queuing_system.memory import Memory
from queuing_system.processor import Processor

from queuing_system.distributions import Uniform, Normal

class StepModel:

    def __init__(self, generator, memory, processor
                 , requests_num=1000, repeat_percent=0, step=0.01):
        self.generator = generator
        self.memory = memory
        self.processor = processor
        self.requests_num = requests_num
        self.repeat_percent = repeat_percent
        self.step = step


    def run(self):
        self.processor.set_aviable(True)

        processed_requests = 0
        total_requests = self.requests_num

        generator_time = self.generator.next_time()
        processor_time = -1

        empty_generated = None

        current_time = self.step
        while processed_requests < total_requests:
            if generator_time < current_time:
                if self.processor.is_aviable() and self.memory.is_empty():
                    empty_generated = True
                self.memory.insert_request()
                prev_gen_time = generator_time
                generator_time = prev_gen_time + self.generator.next_time()

            if 0 < processor_time < current_time:
                processed_requests += 1
                if random.randint(0, 100) < self.repeat_percent:
                    self.memory.insert_request()
                    #total_requests += 1
                self.processor.set_aviable(True)

            if self.processor.is_aviable():
                if not self.memory.is_empty():
                    self.memory.remove_request()
                    self.processor.set_aviable(False)
                    processor_time = ((prev_gen_time if empty_generated
                                       else processor_time)
                                         + self.processor.process_time())
                else:
                    processor_time = -1

            empty_generated = False
            current_time += self.step

        print("\nSTEP MODEL")
        print(f"Repeat: {self.repeat_percent}")
        print(f"Requests: {total_requests}")
        print(f"Repeats: {total_requests - self.requests_num}")
        print(f"Time: {current_time - self.step}")
        print(f"Max len: {self.memory.max_len}")

        return self.memory.max_len


if __name__ == "__main__":
    model = StepModel(
            Generator(Uniform(2, 4)),
            Memory(),
            Processor(Normal(100, 1)),
            10,
            0
            )
    model.run()

