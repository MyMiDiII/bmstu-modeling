from dataclasses import dataclass

from typing import Union

@dataclass
class Event:
    def __init__(self, time: float, eventBlock: Union['Generator', 'Processor']):
        self.time = time
        self.eventBlock = eventBlock

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
        return f"time: {self.time}, type: {self.eventBlock}"

    @property
    def Time(self):
        return self.time

    @Time.setter
    def Time(self, value):
        self.time = value

    @property
    def EventBlock(self):
        return self.eventBlock
