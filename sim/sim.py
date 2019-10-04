from enum import Enum
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="Filepath to PIN log file.")
args = parser.parse_args()

class AccessType(Enum):
	READ = "R"
	WRITE = "W"

def memaccess(ip, AccessType, addr, size, mem_at):
	print(str(size) + " byte " + str(AccessType.value) + " at 0x{:x}".format(addr))
	# fill out simulation here using size, AccessType and addr

with open(args.filepath) as f:
	line = f.readline()
	while line:
		if "#" not in line:
			comps = line.split()
			ip = int(comps[0][:-1], 16)
			access_type = AccessType(comps[1])
			addr = int(comps[2], 16)
			size = int(comps[3])
			mem_at = int(comps[4], 16)
			memaccess(ip, access_type, addr, size, mem_at)
		line = f.readline()
