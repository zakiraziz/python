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

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, (obs[0], obs[1], GRID_SIZE, GRID_SIZE))

    # Draw goal
    pygame.draw.rect(screen, GREEN, (goal_pos[0], goal_pos[1], GRID_SIZE, GRID_SIZE))

    # Draw player
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], GRID_SIZE, GRID_SIZE))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Mirrored movement
            if event.key == pygame.K_LEFT and player_pos[0] + GRID_SIZE < WIDTH:
                player_pos[0] += GRID_SIZE
            elif event.key == pygame.K_RIGHT and player_pos[0] - GRID_SIZE >= 0:
                player_pos[0] -= GRID_SIZE
            elif event.key == pygame.K_UP and player_pos[1] + GRID_SIZE < HEIGHT:
                player_pos[1] += GRID_SIZE
            elif event.key == pygame.K_DOWN and player_pos[1] - GRID_SIZE >= 0:
                player_pos[1] -= GRID_SIZE

            # Check collision with obstacles
            if tuple(player_pos) in obstacles:
                player_pos = [GRID_SIZE, GRID_SIZE]  # Reset to start

            # Check if reached goal
            if tuple(player_pos) == tuple(goal_pos):
                print("You Win!")
                running = False

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
