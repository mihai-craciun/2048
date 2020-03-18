import pygame
import backend

# Colors
# Empty block color
BLK_COLOR = (187, 173, 160)
# Background/grid color
BG_COLOR = (119, 110, 101)

# Font
FONT_SIZE_RATIO = 0.08
FONT_FILE = "ClearSans-Bold.ttf"


# Application context
class Context:
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

    def __init__(self, grid_n):
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

    def __init__(self, rect, value, ctx: Context):
        bg_color = self.BG_POINTS_COLOR.get(value, self.BG_POINTS_COLOR['rest'])
        txt_color = self.TXT_POINTS_COLOR.get(value, self.TXT_POINTS_COLOR['rest'])
        self.surface = pygame.Surface(rect.size)
        self.surface.fill(bg_color)
        self.rect = self.surface.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        text = ctx.font.render(str(value), True, txt_color)
        tw, th = text.get_size()
        self.surface.blit(text, (rect.width // 2 - tw // 2, rect.height // 2 - th // 2))


# Draws bricks on the context screen
def draw_bricks(ctx: Context):
    board = ctx.game.board
    rects = ctx.rects
    for line, rect_vec in zip(board, rects):
        for val, rect in zip(line, rect_vec):
            if val != ctx.game.EMPTY:
                brick = Brick(rect, val, ctx)
                ctx.grid.blit(brick.surface, rect)


# Draws the rectangular slots of the grid directly on the screen
def draw_rect_slots(ctx: Context):
    for rects_arr in ctx.rects:
        for rect in rects_arr:
            pygame.draw.rect(ctx.grid, BLK_COLOR, rect)


def draw_grid(ctx: Context):
    ctx.screen.blit(ctx.grid, ctx.grid_rect)


def draw_stats(ctx: Context):
    string = ""
    if ctx.game.game_over:
        string = "Game over! "
    string += "Score: {}".format(ctx.game.score)
    text = ctx.font.render(string, True, Brick.TXT_POINTS_COLOR['rest'])
    tw, th = text.get_size()
    ctx.screen.blit(text, (ctx.grid_rect.width//2 - tw//2, ctx.grid_rect.y//2 - th//2))


def draw(ctx: Context):
    draw_stats(ctx)
    draw_rect_slots(ctx)
    draw_bricks(ctx)
    draw_grid(ctx)