import argparse
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

parser = argparse.ArgumentParser()
parser.add_argument("filepath", help="Filepath to PIN log file.")
args = parser.parse_args()

base_linenums = []
# this is hard coded careful
hitrates = [[] for i in range(3)]
missrates = [[] for i in range(3)]
rate_idx = 0

with open(args.filepath) as f:
    line = f.readline()
    while line:
        line = line[:-1] # remove \n
        if 'f' in line[0]:
            base_linenum = line.split(' ')[2]
            base_linenums.append(int(base_linenum))
        else:
            data = list(filter(None, line.split('\t')))

            # get hit rate
            hitrate = list(filter(None, data[0].split(' ')))[-1]
            hitrates[rate_idx % 3].append(float(hitrate))

            # get miss rate
            # missrate = list(filter(None, data[2].split(' ')))[-1]
            # missrates[rate_idx % 3].append(float(missrate))

            # rate index to roll over
            rate_idx += 1
        line = f.readline()

for idx in range(3):
    lbl = 'G' if idx is 0 else 'L' + str(idx)
    ax.scatter(base_linenums, hitrates[idx], label=lbl + 'hit%', s=1)
    ax.scatter(base_linenums, missrates[idx], label=lbl + 'miss%', s=1)

ax.legend()
ax.grid(True)

plt.show()
