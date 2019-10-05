from collections import defaultdict

class Address:
    def __init__(self, address):
        self.address = address

class Memory:
    def __init__(self):
        self.mem = defaultdict(int)

    def read(self, address, size):
        result = 0
        origSize = size
        while size > 0:
            subaddress = address + (origSize - size)
            value = self.mem[subaddress]
            value = value << ((size - 1) * 8)
            result += value
            size -= 1
        return result

    def write(self, address, size, data):
        origSize = size
        while size > 0:
            subaddress = address + (origSize - size)
            value = data >> (size - 1) * 8
            value &= 255
            self.mem[subaddress] = value
            size -= 1
