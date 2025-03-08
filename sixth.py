import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 500, 600
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
PADDLE_SPEED = 7
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Paddle and Ball Setup
paddle = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

running = True
clock = pygame.time.Clock()
score = 0

# Game Loop
while running:
    screen.fill(WHITE)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Paddle Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.x > 0:
        paddle.x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.x < WIDTH - PADDLE_WIDTH:
        paddle.x += PADDLE_SPEED
    
    # Move Ball
    ball.x += ball_dx
    ball.y += ball_dy
    
    # Ball Collision with Walls
    if ball.x <= 0 or ball.x >= WIDTH - BALL_SIZE:
        ball_dx = -ball_dx
    if ball.y <= 0:
        ball_dy = -ball_dy
    
    # Ball Collision with Paddle
    if ball.colliderect(paddle):
        ball_dy = -ball_dy
        score += 1  # Increase score when ball hits paddle
    
    # Ball Falls Below Paddle (Game Over)
    if ball.y >= HEIGHT:
        print(f"Game Over! Your score: {score}")
        running = False
    
    # Draw Paddle and Ball
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.ellipse(screen, RED, ball)
    
    # Update Screen
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
