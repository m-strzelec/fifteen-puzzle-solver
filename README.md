# Fifteen-puzzle-solver

Python project solving 15-puzzle game using bfs, dfs and A* strategies.

## Run

```sh
py main.py 'strategy' 'param' 'input_file' 'output_file' 'stats_file'
```

## Example

```sh
py main.py dfs RDUL input.txt solution.txt stats.txt
```

## Description

- `strategy` - The search strategy to use (`bfs`, `dfs`, `astr`).
- `param` - The parameter for the selected strategy (for `dfs` and `bfs` the sequence in which the possible movements are to be checked for example `RDUL`. For `astr` the heuristic `manh` or `hamm`).
- `input_file` - The input file containing initial state of the puzzle.
- `output_file` - The output file to save the solution.
- `stats_file` - The file to save additional information about the search process.

`input_file` example format:
```sh
4 4
1 0 3 4
5 2 6 8
9 10 7 11
13 14 15 12
```

where first row is size of the puzzle - 4x4 and the goal state of the puzzle is:
```sh
4 4
1 2 3 4
5 6 7 8
9 10 11 12
13 14 15 0
```

The solution file contains the number of moves required to complete the puzzle and sequence of moves to complete it. The stats file contains the number of moves, the number of states visited, the number of states processed, the maximum depth of the algorithm and the elapsed time for solving the puzzle. 
