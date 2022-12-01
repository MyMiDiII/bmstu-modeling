from mss.distributions import Distribution

class Generator:

    def __init__(self, distribution: Distribution):
        self.distribution = distribution

    def next_time(self):
        return self.distribution.generate()
