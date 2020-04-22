import argparse
import matplotlib.pyplot as plt
import os

parser = argparse.ArgumentParser()
parser.add_argument('--replay_file', type=str, required=True)
locals().update(vars(parser.parse_args()))

mat_trace = []
with open(replay_file, 'r') as f:
    for line in f:
        if 'MATERIAL' not in line: continue
        mat_trace.append(int(line.split(' ')[-2]))
dirname = os.path.dirname(replay_file)
prefix = os.path.splitext(os.path.basename(replay_file))[0]
plt.plot(mat_trace, marker='o')
plt.ylabel('Material')
plt.xlabel('Round')
fname = f'{dirname}/{prefix}_material.png'
print(f'Saving to {fname}')
plt.gcf().savefig(fname, format='png')
plt.show()
