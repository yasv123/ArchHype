from collections import defaultdict

class Address:
    def __init__(self, address):
        self.address = address

class Memory:
    def __init__(self):
        self.mem = defaultdict(int)
        self.writes = set()

    def read(self, address, size):
        result = 0
        origSize = size
        flag = False
        while size > 0:
            subaddress = address + (origSize - size)
            if not subaddress in self.writes:
                flag = True
                break
            value = self.mem[subaddress]
            value = value << ((size - 1) * 8)
            result += value
            size -= 1
        return (result, flag)

    def write(self, address, size, data):
        origSize = size
        while size > 0:
            subaddress = address + (origSize - size)
            self.writes.add(subaddress)
            value = data >> (size - 1) * 8
            value &= 255
            self.mem[subaddress] = value
            size -= 1
