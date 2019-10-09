from enum import Enum
import argparse
import classes

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="Filepath to PIN log file.")
args = parser.parse_args()

cache = classes.Hierarchy([ (0, 0, 0) ])

class AccessType(Enum):
    READ = "R"
    WRITE = "W"

def memaccess(ip, is_read, addr, size, mem_at, line):
    if is_read:
        cache.read(addr, size)
     else:
        cache.write(addr, size)

with open(args.filepath) as f:
    line = f.readline()
    linenum = 0
    while line:
        if "#" not in line:
            comps = line.split()
            ip = int(comps[0][:-1], 16)
            is_read = comps[1] == "R"
            addr = int(comps[2], 16)
            size = int(comps[3])
            mem_at = int(comps[4], 16)
            memaccess(ip, is_read, addr, size, mem_at, linenum)
        line = f.readline()
        linenum += 1
    print(cache.getMetrics())
