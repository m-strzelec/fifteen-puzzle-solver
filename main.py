import argparse
import time
from Project.algorithms import Algorithms
from Project.board import Board


# Define the maximum recursion depth for DFS
MAX_DFS_DEPTH = 20

# Define the valid strategies and their corresponding parameters
VALID_STRATEGIES = {
    "bfs": ["neighborhood_order"],
    "dfs": ["neighborhood_order"],
    "astr": ["heuristic"],
}

# Define the valid neighborhood orders for BFS and DFS
VALID_NEIGHBORHOOD_ORDERS = ["RLDU", "RLUD", "RDUL", "RDLU", "RUDL", "RULD",
                             "LRDU", "LRUD", "LDUR", "LDRU", "LURD", "LUDR",
                             "DRUL", "DRLU", "DLUR", "DLRU", "DULR", "DURL",
                             "URDL", "URLD", "UDLR", "UDRL", "ULRD", "ULDR"]

# Define the valid heuristics for A*
VALID_HEURISTICS = ["manh", "hamm"]

# Parse the command line arguments
parser = argparse.ArgumentParser(description="Solve a sliding puzzle using different search strategies.")
parser.add_argument("strategy", choices=VALID_STRATEGIES.keys(), help="The search strategy to use")
parser.add_argument("param", help="The parameter for the selected strategy")
parser.add_argument("input_file", help="The input file containing the initial state of the puzzle")
parser.add_argument("output_file", help="The output file to save the solution")
parser.add_argument("stats_file", help="The file to save additional information about the search process")
args = parser.parse_args()

# Determine the selected strategy and its parameter
strategy = args.strategy
param: object = args.param

# Validate the strategy parameter
if strategy in ["bfs", "dfs"]:
    if param not in VALID_NEIGHBORHOOD_ORDERS:
        print(f"Error: Invalid neighborhood order {param} for {strategy} strategy "
              f"(choose any permutation of 'RDUL' letters )")
        exit()
elif strategy == "astr":
    if param not in VALID_HEURISTICS:
        print(f"Error: Invalid heuristic {param} for A* strategy "
              f"(choose from 'manh', 'hamm')")
        exit()

# Load the initial state from the input file
with open(args.input_file, "r") as f:
    next(f)
    state = [list(map(int, line.strip().split())) for line in f]

board = Board(state)
algorithms = Algorithms(board)
search_fn = None

# Define the search function based on the selected strategy
if strategy == "bfs":
    search_fn = lambda b: algorithms.bfs(b)
elif strategy == "dfs":
    search_fn = lambda b: algorithms.dfs(b, MAX_DFS_DEPTH)
elif strategy == "astr":
    search_fn = lambda b: algorithms.astr(b)

# Perform the search and measure the execution time
start_time = time.time()
solution, num_states, num_processed, max_depth = search_fn(param)
end_time = time.time()
duration = format((end_time - start_time) * 1000, '.3f')

# Write the solution to the output file
with open(args.output_file, "w") as f:
    if solution == -1:
        f.write("-1\n")
    else:
        f.write(f"{len(solution)}\n{solution}")

# Write the search stats to the stats file
with open(args.stats_file, "w") as f:
    f.write(f"{len(solution) if solution != -1 else -1}\n"
            f"{num_states}\n"
            f"{num_processed}\n"
            f"{max_depth}\n"
            f"{duration}")
