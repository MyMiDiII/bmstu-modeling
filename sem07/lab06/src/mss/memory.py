class Memory:

    def __init__(self, capacity: int = None):
        self.curLen = 0
        self.capacity = capacity

    def InsertRequest(self) -> bool:
        if self.curLen != self.capacity:
            self.curLen += 1
            return True

        return False

    def RemoveRequest(self) -> bool:
        self.curLen = max(self.curLen - 1, 0)

        return self.curLen

    def IsEmpty(self) -> bool:
        return self.curLen == 0

    @property
    def CurLen(self):
        return self.curLen


if __name__ == "__main__":
    mem = Memory()
    mem.InsertRequest()
    print(mem.curLen)
    mem.InsertRequest()
    print(mem.curLen)
    mem.RemoveRequest()
    print(mem.curLen)
    mem.RemoveRequest()
    print(mem.curLen)
    mem.RemoveRequest()
    print(mem.curLen)

