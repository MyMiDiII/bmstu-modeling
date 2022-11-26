from distributions import Distribution

class Processor:

    def __init__(self, distribution: Distribution):
        self.distribution = distribution
        self.aviable = True

    def process_time(self):
        return self.distribution.generate()

    def set_aviable(self, state=True):
        self.aviable = state 

    def is_aviable(self) -> bool:
        return self.aviable
