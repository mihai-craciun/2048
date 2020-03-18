# Template for Pygame
import pygame
import misc
import random

# Window consts
WIDTH = 480
HEIGHT = 600
GRID_SIZE = 480
FPS = 120
TITLE = "2048 Game"

# Game consts
MARGIN = 10
GRID_N = 4

# App context initialization
ctx = misc.Context(GRID_N)
ctx.width = WIDTH
ctx.height = HEIGHT
ctx.grid_size = GRID_SIZE
ctx.margin = MARGIN
ctx.compute_block_size()

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Init context UI elements
ctx.screen = screen
ctx.create_grid()
ctx.compute_font()
ctx.compute_rects()

# Game objects
# Create the rect locations

all_sprites = pygame.sprite.Group()

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
                ctx.game.move(ctx.game.LEFT)
            if event.key == pygame.K_RIGHT:
                ctx.game.move(ctx.game.RIGHT)
            if event.key == pygame.K_UP:
                ctx.game.move(ctx.game.UP)
            if event.key == pygame.K_DOWN:
                ctx.game.move(ctx.game.DOWN)

    # Update
    all_sprites.update()
    # Draw / Render
    screen.fill(misc.BG_COLOR)
    all_sprites.draw(screen)
    misc.draw(ctx)
    # *after* drawing everything
    pygame.display.flip()

pygame.quit()