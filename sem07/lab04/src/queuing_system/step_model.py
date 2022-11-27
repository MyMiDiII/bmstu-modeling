import random
import bisect

from time import sleep

from queuing_system.event import Event, EventType
from queuing_system.generator import Generator
from queuing_system.memory import Memory
from queuing_system.processor import Processor

from queuing_system.distributions import Uniform, Normal

class StepModel:

    def __init__(self
                 , generator
                 , memory
                 , processor
                 , requests_num=1000
                 , repeat_percent=0
                 , step=0.01):
        self.generator = generator
        self.memory = memory
        self.processor = processor
        self.requests_num = requests_num
        self.repeat_percent = repeat_percent
        self.step = step


    def run(self):
        #print(f"a {self.generator.distribution.a} b {self.generator.distribution.b}")
        #print(f"cur {self.memory.cur_len} max {self.memory.max_len}")
        #print(f"m {self.processor.distribution.m} sigma {self.processor.distribution.sigma}")
        #print(f"req_num {self.requests_num}")
        #print(f"rep {self.repeat_percent}")
        #print(f"step {self.step}")
        self.processor.set_aviable(True)

        processed_requests = 0
        total_requests = self.requests_num

        gen_time = self.generator.next_time()
        proc_time = -1

        generator_event = Event(gen_time, EventType.GENERATOR)
        processor_event = Event(proc_time, EventType.PROCESSOR)

        generate_num = 1
        processe_num = 1

        empty_generated = None

        current_time = self.step
        while processed_requests < total_requests:
            if (generator_event.time < current_time - self.step
                and processor_event.time < current_time - self.step):
                return -1;

            #print()
            #print(f"current_time {current_time}")
            #print(f"gen time {generator_event.time}")
            #print(f"proc time {processor_event.time}")
            if generator_event.time < current_time:
                #print(f"GENERATE {generate_num}")
                if self.processor.is_aviable() and self.memory.is_empty():
                    empty_generated = True
                self.memory.insert_request()
                gen_time = generator_event.time
                generator_event = Event(gen_time + self.generator.next_time(),
                                        EventType.GENERATOR)
                generate_num += 1


            if 0 < processor_event.time < current_time:
                #print(f"END PROCESS {processe_num}")
                processed_requests += 1
                if random.randint(0, 100) < self.repeat_percent:
                    self.memory.insert_request()
                    total_requests += 1
                self.processor.set_aviable(True)

                processe_num += 1

            if self.processor.is_aviable():
                if not self.memory.is_empty():
                    #print(f"BEGIN PROCESS {processe_num}")
                    self.memory.remove_request()
                    self.processor.set_aviable(False)
                    #print(f"gen time {gen_time}")
                    #print(f"proc time {processor_event.time}")
                    #print(f"empty gen? {empty_generated}")
                    ##print(((gen_time
                    #        if empty_generated
                    #        else processor_event.time)
                    #         + self.processor.process_time()))
                    processor_event = Event(((gen_time
                                            if empty_generated
                                            else processor_event.time)
                                             + self.processor.process_time()),
                                             EventType.PROCESSOR)
                    self.processor.set_aviable(False)
                else:
                    processor_event.time = -1

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

