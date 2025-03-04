import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
BASKET_WIDTH, BASKET_HEIGHT = 80, 20
STAR_RADIUS = 10

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Stars")

# Basket setup
basket_x = WIDTH // 2 - BASKET_WIDTH // 2
basket_y = HEIGHT - BASKET_HEIGHT - 10
basket_speed = 8

# Star setup
stars = []
score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
# Game Loop
running = True
while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Basket movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - BASKET_WIDTH:
        basket_x += basket_speed
    
    # Star generation
    if random.randint(1, 30) == 1:
        stars.append([random.randint(0, WIDTH - STAR_RADIUS), 0])
    
    # Star movement
    for star in stars[:]:
        star[1] += 5  # Move the star down
        if star[1] > HEIGHT:
            stars.remove(star)
        elif basket_x < star[0] < basket_x + BASKET_WIDTH and star[1] >= basket_y:
            stars.remove(star)
            score += 1
    
    # Draw basket
    pygame.draw.rect(screen, BLUE, (basket_x, basket_y, BASKET_WIDTH, BASKET_HEIGHT))
    # Draw stars
    for star in stars:
        pygame.draw.circle(screen, RED, (star[0], star[1]), STAR_RADIUS)
    
    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

