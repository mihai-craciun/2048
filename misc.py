import pygame

# Colors
BLK_COLOR = (187, 173, 160)
BG_COLOR = (119, 110, 101)


# Computes the block size given the width, the margin, and the number of blocks
def compute_block_size(width, margin, grid_size):
    return (width - (grid_size + 1) * margin) // grid_size


# Computes an matrix of rects based on the margin, block_size and grid size 
def create_rects(margin, b_size, grid_size):
    rects = [[] for _ in range(grid_size)]
    for i in range(grid_size):
        for j in range(grid_size):
            left = margin * (j + 1) + b_size * j 
            top = margin * (i + 1) + b_size * i
            rect = pygame.Rect(left, top, b_size, b_size)
            rects[i].append(rect)
    return rects


def draw_rects(screen, rects_mat):
    for rects_arr in rects_mat:
        for rect in rects_arr:
            pygame.draw.rect(screen, BLK_COLOR, rect)