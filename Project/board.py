class Board:
    def __init__(self, state):
        self.state = state
        self.rows = len(state)
        self.cols = len(state[0])
        self.empty_value = 0
        self.goal_state = self.get_solved_state()

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.state])

    def __len__(self):
        return len(self.state)

    def find_empty(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.state[row][col] == 0:
                    return row, col

    def move(self, empty_field, direction):
        row, col = empty_field
        new_row, new_col = row, col

        if direction == "U":
            new_row -= 1
        elif direction == "D":
            new_row += 1
        elif direction == "L":
            new_col -= 1
        elif direction == "R":
            new_col += 1

        if new_row < 0 or new_col < 0 or new_row >= self.rows or new_col >= self.cols:
            return

        # Create a copy of the current board state
        new_state = [row[:] for row in self.state]
        # Update the board state
        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]

        return new_state

    def is_solved(self):
        return self.state == self.goal_state

    def get_solved_state(self):
        goal = [[i * self.cols + j + 1 for j in range(self.cols)] for i in range(self.rows)]
        goal[self.rows - 1][self.cols - 1] = 0
        return goal

    def get_state(self):
        return self.state
