import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Paddle
paddle_width, paddle_height = 80, 10
paddle = pygame.Rect(WIDTH//2 - paddle_width//2, HEIGHT - 30, paddle_width, paddle_height)

# Ball
ball_radius = 8
ball = pygame.Rect(WIDTH//2, HEIGHT//2, ball_radius, ball_radius)
ball_speed_x = 4 * random.choice((1, -1))
ball_speed_y = -4

# Bricks
brick_rows, brick_cols = 5, 8
brick_width, brick_height = WIDTH // brick_cols, 20
bricks = [pygame.Rect(col * brick_width, row * brick_height, brick_width, brick_height) 
          for row in range(brick_rows) for col in range(brick_cols)]

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 6
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += 6
    
    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # Ball collision with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    
    # Ball collision with paddle
    if ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y
    
    # Ball collision with bricks
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
            break
    
    # Lose condition
    if ball.bottom >= HEIGHT:
        running = False
    
    # Draw elements
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
