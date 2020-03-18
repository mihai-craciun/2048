# Template for Pygame
import pygame
import backend
import random

# Window consts
WIDTH = 480
HEIGHT = 600
GRID_SIZE = 480
FPS = 120
TITLE = "2048 Game"

# Colors
# Empty block color
BLK_COLOR = (187, 173, 160)
# Background/grid color
BG_COLOR = (119, 110, 101)

# Font
FONT_SIZE_RATIO = 0.08
FONT_FILE = "ClearSans-Bold.ttf"

# Game consts
MARGIN = 10
GRID_N = 4

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


# Application context
class GameGui:
    # Window width
    width: int
    # Window height
    height: int
    # Grid margin
    margin: int
    # Grid n (number of lines/columns)
    grid_n: int
    # Grid rect
    grid_rect: pygame.rect.Rect
    # Grid size (width/height of grid)
    grid_size: int
    # Brick size (computed)
    brick_size: int
    # Game API
    game: backend.Game
    # UI grid rects
    rects: list
    # Screen
    screen: pygame.Surface
    # grid surface
    grid: pygame.Surface
    # Font
    font: pygame.font.Font

    def __init__(self, grid_n, transitions=False):
        self.transitions = transitions
        self.grid_n = grid_n
        self.game = backend.Game(n=grid_n)

    # Computes the block size
    def compute_block_size(self):
        self.brick_size = (self.width - (self.grid_n + 1) * self.margin) // self.grid_n

    # Computes the rects
    def compute_rects(self):
        self.rects = [[] for _ in range(self.grid_n)]
        for i in range(self.grid_n):
            for j in range(self.grid_n):
                left = self.margin * (j + 1) + self.brick_size * j
                top = self.margin * (i + 1) + self.brick_size * i
                rect = pygame.Rect(left, top, self.brick_size, self.brick_size)
                self.rects[i].append(rect)

    # Computes the font
    def compute_font(self):
        self.font = pygame.font.Font(FONT_FILE, int(self.width * FONT_SIZE_RATIO))

    # Positions the grid inside the screen
    def create_grid(self):
        self.grid = pygame.Surface((self.grid_size, self.grid_size))
        self.grid.fill(BG_COLOR)
        self.grid_rect = pygame.rect.Rect(0, self.height - self.grid_size, self.grid_size, self.grid_size)

    # Draws bricks on the context screen
    def draw_bricks(self):
        board = self.game.board
        rects = self.rects
        for line, rect_vec in zip(board, rects):
            for val, rect in zip(line, rect_vec):
                if val != self.game.EMPTY:
                    brick = Brick(rect, val, self)
                    self.grid.blit(brick.surface, rect)

    # Draws the rectangular slots of the grid directly on the screen
    def draw_rect_slots(self):
        for rects_arr in self.rects:
            for rect in rects_arr:
                pygame.draw.rect(self.grid, BLK_COLOR, rect)

    # Draws the game grid
    def draw_grid(self):
        self.screen.blit(self.grid, self.grid_rect)

    # Draws status text bar
    def draw_stats(self):
        string = ""
        if self.game.game_over:
            string = "Game over! "
        string += "Score: {}".format(self.game.score)
        text = self.font.render(string, True, Brick.TXT_POINTS_COLOR['rest'])
        tw, th = text.get_size()
        self.screen.blit(text, (self.grid_rect.width // 2 - tw // 2, self.grid_rect.y // 2 - th // 2))

    # Draws all the elements to the screen
    def draw(self):
        self.draw_stats()
        self.draw_rect_slots()
        self.draw_bricks()
        self.draw_grid()

    def move(self, dir):
        if not self.game.game_over:
            self.game.move(dir)

    def right(self):
        self.move(self.game.RIGHT)

    def left(self):
        self.move(self.game.LEFT)

    def up(self):
        self.move(self.game.UP)

    def down(self):
        self.move(self.game.DOWN)


# App context initialization
game = GameGui(GRID_N, transitions=False)
game.width = WIDTH
game.height = HEIGHT
game.grid_size = GRID_SIZE
game.margin = MARGIN
game.compute_block_size()

# Init context UI elements
game.screen = screen
game.create_grid()
game.compute_font()
game.compute_rects()


# UI Brick element
class Brick:
    # Brick colors for all point ranges
    BG_POINTS_COLOR = {
        2: (238, 228, 218),
        4: (237, 224, 200),
        8: (242, 177, 121),
        16: (245, 149, 99),
        32: (246, 124, 95),
        64: (246, 94, 59),
        'rest': (237, 207, 114),
    }
    # Brick text colors
    TXT_POINTS_COLOR = {
        2: (119, 110, 101),
        4: (119, 110, 101),
        'rest': (249, 246, 242)
    }

    def __init__(self, rect, value, game_gui: GameGui):
        bg_color = self.BG_POINTS_COLOR.get(value, self.BG_POINTS_COLOR['rest'])
        txt_color = self.TXT_POINTS_COLOR.get(value, self.TXT_POINTS_COLOR['rest'])
        self.surface = pygame.Surface(rect.size)
        self.surface.fill(bg_color)
        self.rect = self.surface.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        text = game_gui.font.render(str(value), True, txt_color)
        tw, th = text.get_size()
        self.surface.blit(text, (rect.width // 2 - tw // 2, rect.height // 2 - th // 2))


# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing the window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.left()
            if event.key == pygame.K_RIGHT:
                game.right()
            if event.key == pygame.K_UP:
                game.up()
            if event.key == pygame.K_DOWN:
                game.down()
    # Update
    all_sprites.update()
    # Draw / Render
    screen.fill(BG_COLOR)
    all_sprites.draw(screen)
    game.draw()
    # *after* drawing everything
    pygame.display.flip()

pygame.quit()