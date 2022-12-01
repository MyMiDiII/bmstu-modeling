from enum import Enum
from dataclasses import dataclass


class EventType(Enum):
    GENERATOR = 1
    PROCESSOR = 2

@dataclass
class Event:
    def __init__(self, time: float, event_type: EventType):
        self.time = time
        self.event_type = event_type

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return self.time != other.time

    def __gt__(self, other):
        return self.time > other.time

    def __ge__(self, other):
        return self.time >= other.time

    def __str__(self):
        return f"time: {self.time}, type: {self.event_type}"
