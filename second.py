import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)

# Load bird image
bird = pygame.Rect(100, HEIGHT//2, 30, 30)
gravity = 0.5
velocity = 0

# Pipe settings
pipe_width = 70
pipe_gap = 150
pipe_speed = 3
pipes = []

def create_pipe():
    height = random.randint(100, 400)
    pipes.append(pygame.Rect(WIDTH, 0, pipe_width, height))
    pipes.append(pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap))

# Game loop
running = True
create_pipe()
score = 0

while running:
    screen.fill(BLUE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            velocity = -7  # Jump

    # Bird movement
    velocity += gravity
    bird.y += velocity

    # Pipe movement
    for pipe in pipes:
        pipe.x -= pipe_speed

    # Check collision
    if bird.y > HEIGHT or bird.y < 0 or any(pipe.colliderect(bird) for pipe in pipes):
        running = False  # Game over

    # Remove off-screen pipes and add new ones
    if pipes[0].x < -pipe_width:
        pipes = pipes[2:]  # Remove old pipes
        create_pipe()
        score += 1  # Increase score

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

    # Draw bird
    pygame.draw.ellipse(screen, WHITE, bird)

    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
