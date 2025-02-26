import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Enemies")

# Player setup
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5

# Enemy setup
enemy_size = 50
enemies = [{"x": random.randint(0, WIDTH - enemy_size), "y": -enemy_size, "speed": 3} for _ in range(3)]

# Score
score = 0

# Game loop
running = True
game_over = False

while running:
    pygame.time.delay(20)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart game
                player_x = WIDTH // 2 - player_size // 2
                enemies = [{"x": random.randint(0, WIDTH - enemy_size), "y": -enemy_size, "speed": 3} for _ in range(3)]
                score = 0
                game_over = False

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed

        # Enemy movement
        for enemy in enemies:
            enemy["y"] += enemy["speed"]
            if enemy["y"] > HEIGHT:
                enemy["y"] = -enemy_size
                enemy["x"] = random.randint(0, WIDTH - enemy_size)
                score += 1  # Increase score

            # Collision detection
            if (
                player_x < enemy["x"] + enemy_size
                and player_x + player_size > enemy["x"]
                and player_y < enemy["y"] + enemy_size
                and player_y + player_size > enemy["y"]
            ):
                game_over = True

        # Draw player and enemies
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
        for enemy in enemies:
            pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], enemy_size, enemy_size))

        # Draw score
        score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
    
    else:
        # Game Over screen
        game_over_text = FONT.render("Game Over! Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))

    pygame.display.update()

pygame.quit()
