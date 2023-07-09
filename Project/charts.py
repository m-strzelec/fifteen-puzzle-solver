import os
import pandas as pd
import matplotlib.pyplot as plt

# Read data from file into a pandas DataFrame
data = pd.read_csv('DATA2.txt', header=None, delimiter=' ', names=['solution_depth', 'index', 'strategy',
                                                                   'param', 'solution length',
                                                                   'number of states visited',
                                                                   'number of states processed',
                                                                   'max depth',
                                                                   'elapsed time'])

# Calculate arithmetic means for each criterion and strategy or parameter
criteria = ['solution length', 'number of states visited',
            'number of states processed', 'max depth',
            'elapsed time']
strategies = ['bfs', 'dfs', 'astr']
parameters = ['drlu', 'drul', 'ludr', 'lurd', 'rdlu', 'rdul', 'uldr', 'ulrd']
heuristics = ['hamm', 'manh']

# Means for BFS strategy
bfs_means = {}
for criterion in criteria:
    bfs_means[criterion] = data[data['strategy'] == 'bfs'][criterion].groupby([data['solution_depth'],
                                                                               data['param']]).mean()

# Means for DFS strategy
dfs_means = {}
for criterion in criteria:
    dfs_means[criterion] = data[data['strategy'] == 'dfs'][criterion].groupby([data['solution_depth'],
                                                                               data['param']]).mean()

# Means for A* strategy
astr_means = {}
for criterion in criteria:
    astr_means[criterion] = data[data['strategy'] == 'astr'][criterion].groupby([data['solution_depth'],
                                                                                 data['param']]).mean()

all_means = {}
for criterion in criteria:
    all_means[criterion] = data[criterion].groupby([data['solution_depth'], data['strategy']]).mean()

new_path = r'plots'
if not os.path.exists(new_path):
    os.makedirs(new_path)

# Plot the bar charts
for criterion in criteria:
    # Means for combined
    plt.figure()
    all_means[criterion].unstack().plot(kind='bar', legend=True).set_yscale('log')
    plt.title('Ogółem')
    plt.xlabel('Głębokość')
    plt.ylabel(criterion.capitalize())
    plt.legend(['A*', 'BFS', 'DFS'], title=None)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(fname=f'plots\\Wspólny - {criterion}', dpi=300)

    # Means for BFS strategy
    plt.figure()
    bfs_means[criterion].unstack().plot(kind='bar', legend=True)
    plt.title('BFS')
    plt.xlabel('Głębokość')
    plt.ylabel(criterion.capitalize())
    plt.legend(['DRLU', 'DRUL', 'LUDR', 'LURD', 'RDLU', 'RDUL', 'ULDR', 'ULRD'], title=None, ncol=2)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(fname=f'plots\\BFS - {criterion}', dpi=300)

    # Means for DFS strategy
    plt.figure()
    dfs_means[criterion].unstack().plot(kind='bar', legend=False)
    plt.title('DFS')
    plt.xlabel('Głębokość')
    plt.ylabel(criterion.capitalize())
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(fname=f'plots\\DFS - {criterion}', dpi=300)

    # Means for A* strategy
    plt.figure()
    astr_means[criterion].unstack().plot(kind='bar', legend=True)
    plt.title('A*')
    plt.xlabel('Głębokość')
    plt.ylabel(criterion.capitalize())
    plt.legend(['Hamming', 'Manhattan'], title=None)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(fname=f'plots\\ASTR - {criterion}', dpi=300)
