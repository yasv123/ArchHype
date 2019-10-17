import argparse
import classes

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="Filepath to PIN log file.")
parser.add_argument("--window_size", type=int, help="For a sliding window anaylsis, the number of accesses to include in the window.")
parser.add_argument("--increment_size", type=int, help="For a sliding window analysis, the number of accesses to increment between window analyses.")
args = parser.parse_args()

# set up windowing
if args.window_size is not None or args.increment_size is not None:
    if args.window_size is None or args.increment_size is None:
        print('Window and increment size must be set.')
        exit()
    window_size = args.window_size
    increment_size = args.increment_size
    window = []

cache_metadata = [ (1, 8, 256), (2, 16, 512) ]

def memaccess(ip, is_read, addr, size, mem_at, line):
    # why the hell do we need this
    if is_read:
        cache.read(addr, size)
    else:
        cache.write(addr, size)

with open(args.filepath) as f:
    cache = classes.Memory(cache_metadata)
    line = f.readline()
    linenum = 0
    while line:
        # skip comment lines, don't increment linenum
        if "#" in line:
            line = f.readline()
            continue

        # parse
        comps = line.split()
        ip = int(comps[0][:-1], 16)
        is_read = comps[1] == "R"
        addr = int(comps[2], 16)
        size = int(comps[3])
        mem_at = int(comps[4], 16)

        # check if windowing
        if window is not None:
            if len(window) < window_size:
                # filling the current window
                window.append((ip, is_read, addr, size, mem_at, linenum))
                memaccess(ip, is_read, addr, size, mem_at, linenum)
            else:
                # window size met, time to reset and slide
                print('finishing window', linenum - window_size, linenum - 1)
                cache.printMetrics()
                cache = classes.Memory(cache_metadata)

                # slice off first increment_size elements
                window = window[increment_size:]
                window.append((ip, is_read, addr, size, mem_at, linenum))

                # reprocess remaining elements
                for access in window:
                    memaccess(access[0], access[1], access[2], access[3], access[4], access[5])
        else:
            memaccess(ip, is_read, addr, size, mem_at, linenum)

        line = f.readline()
        linenum += 1

# make sure to always print final window size, should always be at least 1
print('final window size', len(window))
cache.printMetrics()
