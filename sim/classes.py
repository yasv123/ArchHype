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
        flag = False
        while size > 0:
            subaddress = address + size - 1
            if not subaddress in self.writes:
                flag = True
                break
            value = self.mem[subaddress]
            value = value << ((size - 1) * 8)
            result += value
            size -= 1
        return (result, flag)

    def write(self, address, size, data, line):
        while size > 0:
            subaddress = address + size - 1
            self.writes.add(subaddress)
            value = data >> (size - 1) * 8
            value &= 255
            self.mem[subaddress] = value
            size -= 1
            if line > 3535 and line < 4187 and subaddress < 0x00007f6d6ce94bb8 and subaddress > 0x00007f6d6ce94ba8:
                print(line, 'addr', hex(address), size, 'data', hex(data))
