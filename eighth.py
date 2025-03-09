import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mirror Maze")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
player_pos = [GRID_SIZE, GRID_SIZE]
goal_pos = [WIDTH - 2 * GRID_SIZE, HEIGHT - 2 * GRID_SIZE]

# Obstacles
num_obstacles = 8
obstacles = []
for _ in range(num_obstacles):
    x = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
    y = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
    if (x, y) != tuple(player_pos) and (x, y) != tuple(goal_pos):
        obstacles.append((x, y))
