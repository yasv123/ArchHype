from enum import Enum
import argparse
import classes

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="Filepath to PIN log file.")
args = parser.parse_args()

mainmem = classes.Memory()

class AccessType(Enum):
    READ = "R"
    WRITE = "W"

mismatch = {'g': 0, 'f': 0, 'l': 0}
unmatch = {'g': 0, 'f': 0, 'l': 0}

def memaccess(ip, access_type, addr, size, mem_at, line):
    global mismatch
    global unmatch
    # print(str(size) + " byte " + str(AccessType.value) + " at "+str(addr))
    # fill out simulation here using size, AccessType and addr
    if access_type is AccessType.READ:
        read, un = mainmem.read(addr, size)
        if read != mem_at and not un:
            mismatch['g'] += 1
            if line < 37000:
                mismatch['f'] += 1
            else:
                mismatch['l'] += 1
        elif read != mem_at and un:
            print('actual', mem_at, 'simulated', read)
            unmatch['g'] += 1
            if line < 37000:
                unmatch['f'] += 1
            else:
                unmatch['l'] += 1
    else:
        mainmem.write(addr, size, mem_at)

with open(args.filepath) as f:
    line = f.readline()
    linenum = 0
    while line:
        if "#" not in line:
            comps = line.split()
            ip = int(comps[0][:-1], 16)
            access_type = AccessType(comps[1])
            addr = int(comps[2], 16)
            size = int(comps[3])
            mem_at = int(comps[4], 16)
            memaccess(ip, access_type, addr, size, mem_at, linenum)
        line = f.readline()
        linenum += 1
print(mismatch, unmatch)
