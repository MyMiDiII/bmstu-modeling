class Memory:

    def __init__(self):
        self.cur_len = 0
        self.max_len = 0

    def insert_request(self):
        self.cur_len += 1
        self.max_len = max(self.max_len, self.cur_len)

    def remove_request(self):
        self.cur_len -= 1
        self.cur_len = 0 if self.cur_len < 0 else self.cur_len

    def is_empty(self) -> bool:
        return self.cur_len == 0


if __name__ == "__main__":
    mem = Memory()
    mem.insert_request()
    print(mem.cur_len, mem.max_len)
    mem.insert_request()
    print(mem.cur_len, mem.max_len)
    mem.remove_request()
    print(mem.cur_len, mem.max_len)
    mem.remove_request()
    print(mem.cur_len, mem.max_len)
    mem.remove_request()
    print(mem.cur_len, mem.max_len)

