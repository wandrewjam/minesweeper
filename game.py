import random


class MinesweeperBoard:
    _offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    def __init__(self, nrow: int, ncol: int, nmine: int):
        self._nel = nrow * ncol
        if nmine >= self._nel:
            raise ValueError("Number of mines must be less than rows * columns")
        
        self._nrow = nrow
        self._ncol = ncol
        self._nmine = nmine
        
        # Position double is interpreted in C? order: k = ncol * i + j
        self._mine_pos = random.sample(range(self._nel), self._nmine)

        self._clue_grid = [0 for _ in range(self._nel)]
        for mine in self._mine_pos:
            mine_tuple = self._int_to_tuple(mine)
            for pos in self._compute_adjacent_positions(*mine_tuple):
                self._clue_grid[pos] += 1
        
        for mine in self._mine_pos:
            self._clue_grid[mine] = -1
        
        self._flagged = [False for _ in range(self._nel)]
        self._revealed = [False for _ in range(self._nel)]
        self.game_status = 0  # -1: Game lost, 0: Game ongoing, 1: Game won

    def __repr__(self) -> str:
        return f"MinesweeperBoard(nrow={nrow}, ncol={ncol}, nmine={nmine})"

    def __str__(self) -> str:
        outstr = ""

        for int_pos, adjacent_mines in enumerate(self._clue_grid):
            if self._flagged[int_pos]:
                outstr += "X"
            elif not self._revealed[int_pos]:
                outstr += "."
            else:
                outstr += str(adjacent_mines)

            if (int_pos + 1) % self._ncol == 0:
                outstr += "\n"
        return outstr

    def _tuple_to_int(self, i: int, j: int) -> int:
        return self._ncol * i + j

    def _int_to_tuple(self, int_pos: int) -> int:
        return int_pos // self._ncol, int_pos % self._ncol

    def _compute_adjacent_positions(self, i: int, j: int) -> list:
        adjacent_positions = [(i + i_offset, j + j_offset) for i_offset, j_offset in self._offsets if self.is_valid_position(i + i_offset, j + j_offset)]
        return [self._tuple_to_int(i, j) for i, j in adjacent_positions]

    def is_valid_position(self, i, j):
        return (0 <= i < self._nrow) and (0 <= j < self._ncol)
    
    def mark(self, i: int, j: int):
        if not self.is_valid_position(i, j):
            raise ValueError(f"Invalid position specified. The position (i, j) must satisfy 0 <= i < {self._nrow} and 0 <= j < {self._ncol}")
        
        int_pos = self._tuple_to_int(i, j)
        self._flagged[int_pos] = not self._flagged[int_pos]

    def reveal(self, i: int, j: int):
        if not self.is_valid_position(i, j):
            raise ValueError(f"Invalid position specified. The position (i, j) must satisfy 0 <= i < {self._nrow} and 0 <= j < {self._ncol}")
        int_pos = self._tuple_to_int(i, j)
        
        if self._revealed[int_pos] or self._flagged[int_pos]:
            # Square has already been revealed or flagged
            return
        
        if self._clue_grid[int_pos] == -1:
            # Stepped on a mine!
            self.game_status = -1
            return
        
        self._revealed[int_pos] = True
        if self._clue_grid[int_pos] == 0:
            for pos in self._compute_adjacent_positions(i, j):
                self.reveal(*self._int_to_tuple(pos))

        if sum(self._revealed) + self._nmine >= self._nel:
            # All non-mine squares have been revealed
            self.game_status = 1


def play_game(nrow: int, ncol: int, nmine: int):
    game = MinesweeperBoard(nrow=nrow, ncol=ncol, nmine=nmine)
    while game.game_status == 0:
        print(game)

        in_str = input("Enter guess as x, y -- or type F to flag a location: ")
        try:
            i, j = [int(el.strip()) for el in in_str.split(',')]
        except ValueError:
            if in_str == "F":
                try:
                    i, j = [int(el.strip()) for el in input("Enter flag location as x, y: ").split(',')]
                except ValueError:
                    print("Please enter a valid position")
                    continue
                else:
                    action = game.mark
            else:
                print("Please enter a valid position")
                continue
        else:
            action = game.reveal

        if not game.is_valid_position(i, j):
            print("Please enter a valid position")
            continue
        
        action(i, j)
    if game.game_status == 1:
        print("You win!")
    elif game.game_status == -1:
        print("You lose")
        print("Goodbye")

if __name__ == "__main__":
    print("Welcome to Minesweeper!")
    # nrow = int(input("Enter number of rows: "))
    # ncol = int(input("Enter number of columns: "))
    # nmine = int(input("Enter number of mines: "))
    random.seed(1)
    nrow, ncol, nmine = 10, 8, 10

    play_game(nrow=nrow, ncol=ncol, nmine=nmine)
