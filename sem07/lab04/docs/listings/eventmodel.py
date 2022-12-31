class EventModel:

    def run(self):
        self.processor.set_aviable(True)

        processed_requests = 0
        total_requests = self.requests_num
        events = FutureEvents()

        events.add(Event(self.generator.next_time(), EventType.GENERATOR))

        while processed_requests < total_requests:
            cur_event = events.next()

            if cur_event.event_type == EventType.GENERATOR:
                self.memory.insert_request()
                events.add(Event(cur_event.time + self.generator.next_time(),
                                 EventType.GENERATOR))

            if cur_event.event_type == EventType.PROCESSOR:
                processed_requests += 1
                if random.randint(0, 100) < self.repeat_percent:
                    self.memory.insert_request()
                self.processor.set_aviable(True)

            if self.processor.is_aviable():
                if not self.memory.is_empty():
                    self.memory.remove_request()
                    self.processor.set_aviable(False)
                    events.add(Event(cur_event.time +
                                     self.processor.process_time(),
                                     EventType.PROCESSOR))

        return self.memory.max_len
