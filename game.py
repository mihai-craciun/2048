# Template for Pygame
import pygame
import misc
import random

# Window consts
WIDTH = 480
HEIGHT = 480
FPS = 120
TITLE = "2048 Game"

# Game consts
MARGIN = 15
GRID_SIZE = 4
BLOCK_SIZE = misc.compute_block_size(WIDTH, MARGIN, GRID_SIZE)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Game objects
# Create the rect locations
rects = misc.create_rects(MARGIN, BLOCK_SIZE, GRID_SIZE)

all_sprites = pygame.sprite.Group()

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    # Draw / Render
    screen.fill(misc.BG_COLOR)
    all_sprites.draw(screen)
    misc.draw_rects(screen, rects)
    # *after* drawing everything
    pygame.display.flip()

pygame.quit()