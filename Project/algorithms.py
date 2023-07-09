from queue import Queue, PriorityQueue
from Project.board import Board


class Algorithms:
    def __init__(self, board):
        self.board = board
        self.visited = set()

    def bfs(self, order):
        # Initialize counters
        num_states = 1  # count the initial state as visited
        num_processed = 0
        max_depth = 0
        start = self.board
        self.visited.add(tuple(map(tuple, start.state)))
        queue = Queue()
        queue.put((start.state, "", 0))

        # Check if the initial state is the solution
        if start.is_solved():
            return "", num_states, num_processed, max_depth

        while not queue.empty():
            curr, path, depth = queue.get()
            curr_board = Board(curr)

            # Check if the current state is the solution
            if curr_board.is_solved():
                return path, num_states, num_processed, max_depth

            empty_field = curr_board.find_empty()
            num_processed += 1
            for direction in order:
                new_board = curr_board.move(empty_field, direction)
                if new_board is not None and tuple(map(tuple, new_board)) not in self.visited:
                    self.visited.add(tuple(map(tuple, new_board)))
                    num_states += 1
                    new_path = path + direction
                    max_depth = max(max_depth, depth)
                    queue.put((new_board, new_path, depth + 1))

        # No solution found, return -1 and the counters
        return -1, num_states, num_processed, max_depth

    '''# iterative dfs
    def dfs(self, order, max_limit):
        # Initialize counters
        num_states = 1  # count the initial state as visited
        num_processed = 0
        max_depth = 0
        start = self.board

        # Check if the initial state is the solution
        if start.is_solved():
            return "", num_states, num_processed, max_depth

        # Iteratively increase depth limit until a solution is found
        for limit in range(1, max_limit):
            stack = [(start.state, "", 0)]
            self.visited = set((tuple(map(tuple, start.state))))
            num_states = 1
            num_processed = 0
            max_depth = 0

            while stack:
                curr, path, depth = stack.pop()
                curr_board = Board(curr)

                # Check if the current state is the solution
                if curr_board.is_solved():
                    return path, num_states, num_processed, max_depth

                empty_field = curr_board.find_empty()

                # Generate all possible moves in the same direction
                if depth < limit:
                    for direction in order:
                        new_board = curr_board.move(empty_field, direction)
                        if new_board is not None and tuple(map(tuple, new_board)) not in self.visited:
                            self.visited.add(tuple(map(tuple, new_board)))
                            num_states += 1
                            new_path = path + direction
                            max_depth = max(max_depth, depth)
                            print(new_path)
                            stack.append((new_board, new_path, depth + 1))
                    num_processed += 1

        # No solution found, return -1 and the counters
        return -1, num_states, num_processed, max_depth'''

    def dfs(self, order, limit):
        # Initialize counters
        num_states = 1  # count the initial state as visited
        num_processed = 0
        max_depth = 0
        start = self.board
        # store depth of each visited state
        visited = {tuple(map(tuple, start.state)): 0}

        def dfs_helper(curr, path, depth):
            nonlocal num_states, num_processed, max_depth, result
            curr_board = Board(curr)

            # Check if the current state is the solution
            if curr_board.is_solved():
                return path, num_states, num_processed, max_depth

            num_processed += 1
            # Check if we have reached the depth limit
            if depth >= limit:
                return None

            empty_field = curr_board.find_empty()

            # Generate all possible moves in the same direction
            for direction in order:
                new_board = curr_board.move(empty_field, direction)
                if new_board is not None:
                    new_state = tuple(map(tuple, new_board))
                    if new_state not in visited or visited[new_state] > depth:
                        visited[new_state] = depth
                        num_states += 1
                        new_path = path + direction
                        max_depth = max(max_depth, len(new_path))
                        result = dfs_helper(new_board, new_path, depth + 1)
                        if result is not None:
                            return result
            return None

        # Call the recursive helper function
        result = dfs_helper(start.state, "", 0)
        if result is None:
            return -1, num_states, num_processed, max_depth
        else:
            return result

    def astr(self, heuristic):
        # Initialize counters
        num_states = 1  # count the initial state as visited
        num_processed = 0
        max_depth = 0
        start = self.board
        solved = start.get_solved_state()
        self.visited.add(tuple(map(tuple, start.state)))

        # Define the heuristic function
        def h(node):
            distance = 0
            # get number of misplaced puzzles
            if heuristic == 'hamm':
                for i, j in zip(range(start.rows), range(start.cols)):
                    if node[i][j] != 0 and node[i][j] != solved[i][j]:
                        distance += 1
            # get number of puzzles away from goal state
            elif heuristic == 'manh':
                for i, j in zip(range(start.rows), range(start.cols)):
                    if node[i][j] != 0 and node[i][j] != solved[i][j]:
                        goal_i, goal_j = [(index, row.index(node[i][j]))
                                          for index, row in enumerate(solved)
                                          if node[i][j] in row][0]
                        diff = abs(i - goal_i) + abs(j - goal_j)
                        distance += diff

            # return distance
            return distance

        # Define the priority queue and add the initial state
        queue = PriorityQueue()
        queue.put((h(start.state), 0, start.state, ""))

        while not queue.empty():
            _, depth, curr, path = queue.get()
            curr_board = Board(curr)
            empty_field = curr_board.find_empty()

            # Update the counters
            num_processed += 1
            max_depth = max(max_depth, depth)

            # Check if the current state is the solution
            if curr_board.is_solved():
                return path, num_states, num_processed, max_depth

            # Generate the successor states and add them to the queue
            for direction in ['L', 'U', 'D', 'R']:
                new_board = curr_board.move(empty_field, direction)
                if new_board is not None and tuple(map(tuple, new_board)) not in self.visited:
                    self.visited.add(tuple(map(tuple, new_board)))
                    # f = g + h
                    f = depth + 1 + h(new_board)
                    new_path = path + direction
                    num_states += 1
                    queue.put((f, depth + 1, new_board, new_path))

        # No solution found
        return -1, num_states, num_processed, max_depth
