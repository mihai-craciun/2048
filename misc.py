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
    # Grid margin
    margin: int
    # Grid size (number of lines/columns)
    grid_size: int
    # Brick size (computed)
    brick_size: int
    # Game API
    game: backend.Game
    # UI grid rects
    rects: list
    # Screen
    screen: pygame.Surface
    # Font
    font: pygame.font.Font

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.game = backend.Game(n=grid_size)

    # Computes the block size
    def compute_block_size(self):
        self.brick_size = (self.width - (self.grid_size + 1) * self.margin) // self.grid_size

    # Computes the rects
    def compute_rects(self):
        self.rects = [[] for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                left = self.margin * (j + 1) + self.brick_size * j
                top = self.margin * (i + 1) + self.brick_size * i
                rect = pygame.Rect(left, top, self.brick_size, self.brick_size)
                self.rects[i].append(rect)

    # Computes the font
    def compute_font(self):
        self.font = pygame.font.Font(FONT_FILE, int(self.width * FONT_SIZE_RATIO))

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
                ctx.screen.blit(brick.surface, rect)


# Draws the rectangular slots of the grid directly on the screen
def draw_rect_slots(ctx: Context):
    for rects_arr in ctx.rects:
        for rect in rects_arr:
            pygame.draw.rect(ctx.screen, BLK_COLOR, rect)