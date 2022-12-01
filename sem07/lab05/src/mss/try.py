class Field:
    def __init__(self):
        self._a = 1


class Check:
    def __init__(self):
        self._field = Field()

    def change(self):
        self.field._a = 4

    @property
    def field(self):
        return self._field

c = Check()
l = [c.field]
print([x._a for x in l])
c.field._a = 5
print([x._a for x in l])
