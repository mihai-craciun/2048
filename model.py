import numpy as np


# Class containing the model and logic of the game
class Game:
    # Directions for movement
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'

    # Constructor
    def __init__(self, board=None, n=None):
        # If no board is present, generate one
        if board is None:
            if n is None:
                n = 4
            self.n = n
            self.board = np.zeros((n, n), dtype=int)
            # Initialize the game by adding two initial blocks
            self.add_brick()
            self.add_brick()
        # Else check if the board has only power of two elements and matches the size
        else:
            self.board = np.array(board, dtype=np.int)
            shape = self.board.shape
            if shape[0] != shape[1] or (n is not None and shape[0] != n):
                raise Exception("The board is not a square, or wrong grid size specified")

    # Inserts a random brick of 2 or 4 in a random free position
    def add_brick(self):
        empty_i, empty_j = np.where(self.board == 0)
        brick = np.random.choice([2, 4])
        # Apply brick in a random free spot
        idx = np.random.randint(len(empty_i))
        self.board[empty_i[idx]][empty_j[idx]] = brick

    # The score is the sum of all the points
    def get_score(self):
        return np.sum(self.board)

    # Returns a transformed board
    @staticmethod
    def get_transformed_board(board, direction):
        if direction not in [Game.LEFT, Game.RIGHT, Game.UP, Game.DOWN]:
            raise Exception("Invalid direction '{}'".format(direction))
        elif direction == Game.LEFT:
            return np.array(board)
        elif direction == Game.RIGHT:
            return np.flip(board, 1)
        elif direction == Game.UP:
            return board.T
        elif direction == Game.DOWN:
            return np.flip(board, 0).T
    
    # Restores a baord from transformation
    @staticmethod
    def get_revert_transformed_board(board, direction):
        if direction not in [Game.LEFT, Game.RIGHT, Game.UP, Game.DOWN]:
            raise Exception("Invalid direction '{}'".format(direction))
        elif direction == Game.LEFT:
            return np.array(board)
        elif direction == Game.RIGHT:
            return np.flip(board, 1)
        elif direction == Game.UP:
            return board.T
        elif direction == Game.DOWN:
            return np.flip(board.T, 0)

    # Moves a line to the left
    # Returns a line of transitions
    @staticmethod
    def move_line(line):
        # Locations of bricks
        bricks = np.where(line != 0)[0]
        # If there is no brick return
        if len(bricks) == 0:
            return line
        # copy line
        line = np.array(line)
        # The locations the bricks shifted to
        bricks_move_location = np.zeros(bricks.shape, dtype=int)
        # Reference for collapse, a brick can only collapse once in a move
        # -1 for None, x for position of leftmost neighbour it collapsed with
        bricks_collapsed = -np.ones(bricks.shape, dtype=int)
        # Collapse bricks
        for i, b in enumerate(bricks):
            # get next neighbor
            ni = i+1
            # if not exists return, no more collapses
            if ni == len(bricks):
                break 
            nb = bricks[i+1]
            # if they can collapse
            if line[b] == line[nb] and bricks_collapsed[i] == -1 and bricks_collapsed[ni] == -1:
                line[b] *= 2
                line[nb] *= 2
                bricks_collapsed[i] = i
                bricks_collapsed[ni] = i
        # init leftmost free element
        lm_free = 0
        # Calculate move bricks vector
        for i, b in enumerate(bricks):
            bci = bricks_collapsed[i]
            bc = bricks[bci] if bci != -1 else -1
            if bc != b and bc != -1:
            # if it is a collapsed right brick, move it with it's neighbor
                bricks_move_location[i] = bricks_move_location[bc]
            else:
            # was not collapsed, or was collapsed into
                bricks_move_location[i] = lm_free
                lm_free += 1
        # Apply move to line
        newline = np.zeros(line.shape)
        for b, newloc in zip(bricks, bricks_move_location):
            newline[newloc] = line[b]
        return newline

    # Applys a move to the board
    def move(self, direction):
        if direction not in [self.LEFT, self.RIGHT, self.UP, self.DOWN]:
            raise Exception("Invalid direction '{}'".format(direction))
        # The algorithm will apply to the left and use transforms to handle directions
        board = self.get_transformed_board(self.board, direction)
        # Apply algorithm
        for i, line in enumerate(board):
            board[i] = self.move_line(line)
        self.board = self.get_revert_transformed_board(board, direction)
        self.add_brick()

action = {
    'u' : 'up',
    'l' : 'left',
    'd' : 'down',
    'r' : 'right',
}

game = Game()
while True:
    print(game.board)
    a = raw_input('Action: ')
    game.move(action[a])