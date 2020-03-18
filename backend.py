import numpy as np


# Class containing the model and logic of the game
class Game:
    # Directions for movement
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
    PTS_GAME_OVER = -1
    EMPTY = 0

    # Constructor
    def __init__(self, board=None, n=None, score=None):
        # If no board is present, generate one
        if board is None:
            if n is None:
                n = 4
            self.score = 0
            self.n = n
            self.board = np.zeros((n, n), dtype=int)
            # Initialize the game by adding two initial blocks
            self.board = self.add_brick_to_board(self.board)
            self.board = self.add_brick_to_board(self.board)
        # Else check if the board has only power of two elements and matches the size
        else:
            if score is None:
                score = 0
            self.score = score
            self.board = np.array(board, dtype=np.int)
            shape = self.board.shape
            if shape[0] != shape[1] or (n is not None and shape[0] != n):
                raise Exception("The board is not a square, or wrong grid size specified")
        self.game_over = False

    # Returns a clone board by inserting a random brick of 2 or 4 in a random free position
    @staticmethod
    def add_brick_to_board(board):
        board = np.array(board)
        empty_i, empty_j = np.where(board == 0)
        brick = np.random.choice([2, 4])
        # Apply brick in a random free spot
        idx = np.random.randint(len(empty_i))
        board[empty_i[idx]][empty_j[idx]] = brick
        return board

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
            return 0, line
        # copy line
        line = np.array(line)
        # The locations the bricks shifted to
        bricks_move_location = np.zeros(bricks.shape, dtype=int)
        # Reference for collapse, a brick can only collapse once in a move
        # -1 for None, x for position of leftmost neighbour it collapsed with
        bricks_collapsed = -np.ones(bricks.shape, dtype=int)
        # Score
        points = 0
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
                # update points with collapse value
                points += line[b]
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
                bricks_move_location[i] = bricks_move_location[bci]
            else:
            # was not collapsed, or was collapsed into
                bricks_move_location[i] = lm_free
                lm_free += 1
        # Apply move to line
        newline = np.zeros(line.shape)
        for b, newloc in zip(bricks, bricks_move_location):
            newline[newloc] = line[b]
        return points, newline

    # Applys a move to a board
    # Returns the points and the new board
    @staticmethod
    def move_board(board, direction):
        if direction not in [Game.LEFT, Game.RIGHT, Game.UP, Game.DOWN]:
            raise Exception("Invalid direction '{}'".format(direction))
        # The algorithm will apply to the left and use transforms to handle directions
        board = Game.get_transformed_board(board, direction)
        points = 0
        # Apply algorithm
        for i, line in enumerate(board):
            l_points, newline = Game.move_line(line)
            board[i] = newline
            points += l_points
        board = Game.get_revert_transformed_board(board, direction)
        # If the board is full after the move, no piece can be added, game over
        if (np.where(board == 0)[0].size == 0):
            return Game.PTS_GAME_OVER, board
        # Add a new brick and return the points accumulated and the new board
        board = Game.add_brick_to_board(board)
        return points, board

    
    # Moves the board in the given direction and returns a flag telling if game is over
    def move(self, direction):
        pts, board = self.move_board(self.board, direction)
        if (pts == self.PTS_GAME_OVER):
            self.game_over = True
            return
        self.score += pts
        self.board = board


# When running the file as primary, play a game
if __name__ == "__main__":

    action = {
        'u' : 'up',
        'l' : 'left',
        'd' : 'down',
        'r' : 'right',
    }

    game = Game()
    game_over = False
    while not game.game_over:
        print("Score: {}".format(game.score))
        print(game.board)
        a = input('Action: ')
        try:
            game.move(action[a])
        except KeyError:
            print("Wrong character")
            continue