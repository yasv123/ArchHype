from collections import defaultdict
import math
import random
import pprint

pp = pprint.PrettyPrinter(indent=4)

class Address:
    def __init__(self, address):
        self.address = address

class OldMemory:
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
            #if line > 3535 and line < 4187 and
            #subaddress < 0x00007f6d6ce94bb8 and subaddress > 0x00007f6d6ce94ba8:
            #    print(line, 'addr', hex(address), size, 'data', hex(data))


class Cache:
    def __init__(self, A, B, C, allocate):
        self.hits = 0
        self.misses = 0

        self.ways = A
        self.blocksize = B
        self.capacity = C
        self.sets = C // (A * B)
        self.allocate = allocate

        self.offsetbits = int(math.log2(self.blocksize))
        self.indexbits = int(math.log2(self.sets))

        self.cache = [ [ (0, False, False) for j in range(self.ways) ] for i in range(self.sets)]

    def getOffset(self, addr):
        return addr & (self.blocksize - 1)

    def getIndex(self, addr):
        return (addr >> self.offsetbits) & (self.sets - 1)

    def getTag(self, addr):
        return addr >> (self.offsetbits + self.indexbits)

    def read(self, addr):
        ways = self.cache[self.getIndex(addr)]
        taglist = list(filter(lambda item: item[0] == self.getTag(addr) and item[1] == True, ways))
        assert len(taglist) <= 1, "More than one instance of same tag in set"
        block = taglist[0] if len(taglist) == 1 else (0, False, False)
        hit = block[1]
        if not hit:
            self.load(addr)
        self.use(addr)
        return hit

    def write(self, addr):
        return read(addr)
        """
        TODO: DO THIS
        """

    def load(self, addr):
        ways = self.cache[self.getIndex(addr)]
        # unused = list(filter(lambda item: ways[item][2] == False, range(self.ways)))
        numused = len(list(filter(lambda item: item[1], ways)))
        if numused == self.ways:
            # evict logic
            indices = list(filter(lambda item: ways[item][2] == False, range(self.ways)))
            evict = random.sample(indices, 1)[0]
            ways[evict] = (self.getTag(addr), True, True)
        else:
            unused = list(filter(lambda item: ways[item][1] == False, range(self.ways)))[0]
            ways[unused] = (self.getTag(addr), True, True)


    def use(self, addr):
        ways = self.cache[self.getIndex(addr)]
        blockindex = list(filter(lambda item: ways[item][0] == self.getTag(addr) and ways[item][1] == True, range(self.ways)))[0]
        ways[blockindex] = (self.getTag(addr), True, True)
        lrucount = len(list(filter(lambda item: item[1] == True and item[2] == True, ways)))
        if lrucount == self.ways:
            for index in range(self.ways):
                if not index == blockindex:
                    ways[index] = (ways[index][0], True, False)



class Memory:
    def __init__(self, caches):
        self.caches = [Cache(A, B, C, True) for A, B, C in caches]
        self.hits = 0
        self.misses = 0

    def read(self, addr, size):
        for offset in range(size):
            subaddress = addr + offset
            globalHit = False
            for level in range(len(self.caches)):
                hit = self.caches[level].read(subaddress)
                if hit:
                    globalHit = True
                    self.caches[level].hits += 1
                    break
                else:
                    self.caches[level].misses += 1
            if globalHit:
                self.hits += 1
            else:
                self.misses += 1


    def write(self, addr, size):
        self.read(addr, size)

    def printMetrics(self):
        gtotal = self.hits + self.misses
        ghits = (self.hits / gtotal) * 100
        gmisses = (self.misses / gtotal) * 100
        print('G  hit rate: %10.2f\t\tG  hit count: %10d\t\tG  miss rate: %10.2f\t\tG  miss count: %10d'% (ghits, self.hits, gmisses, self.misses))
        for level in range(len(self.caches)):
            cache = self.caches[level]
            ltotal = cache.hits + cache.misses
            lhits = (cache.hits / ltotal) * 100
            lmisses = (cache.misses / ltotal) * 100
            print('L%d hit rate: %10.2f\t\tL%d hit count: %10d\t\tL%d miss rate: %10.2f\t\tL%d miss count: %10d'% (level, lhits, level, cache.hits, level, lmisses, level, cache.misses))


