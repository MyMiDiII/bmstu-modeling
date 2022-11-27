class StepModel:

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
                saved_time = generator_time
                generator_time = saved_time + self.generator.next_time()

            if 0 < processor_time < current_time:
                processed_requests += 1
                if random.randint(0, 100) < self.repeat_percent:
                    self.memory.insert_request()
                self.processor.set_aviable(True)

            if self.processor.is_aviable():
                if not self.memory.is_empty():
                    self.memory.remove_request()
                    self.processor.set_aviable(False)
                    processor_time = ((saved_time if empty_generated
                                       else processor_time)
                                         + self.processor.process_time())
                else:
                    processor_time = -1

            empty_generated = False
            current_time += self.step

        return self.memory.max_len
