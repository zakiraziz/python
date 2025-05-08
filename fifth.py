import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RAINBOW_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), 
                 (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Snake and food
snake = [(100, 100), (90, 100), (80, 100)]
snake_dir = (CELL_SIZE, 0)
food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
        random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)

# Mr. Ecode variables
score = 0
rainbow_mode = False
secret_message = ""
message_timer = 0
special_food = None
special_food_timer = 0
god_mode = False

clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont(None, 36)

def draw_special_food():
    if special_food:
        x, y = special_food
        # Draw a spinning square
        size = CELL_SIZE - 2
        points = []
        for i in range(4):
            angle = pygame.time.get_ticks() / 200 + i * math.pi / 2
            px = x + CELL_SIZE // 2 + math.cos(angle) * size
            py = y + CELL_SIZE // 2 + math.sin(angle) * size
            points.append((px, py))
        pygame.draw.polygon(screen, BLUE, points)

def show_secret_message():
    if secret_message and message_timer > 0:
        text = font.render(secret_message, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

def check_special_combination(keys):
    # Konami code (simplified): UP, UP, DOWN, DOWN, LEFT, RIGHT, LEFT, RIGHT, B, A
    combination = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
                   pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT,
                   pygame.K_b, pygame.K_a]
    
    if len(keys) >= len(combination) and keys[-len(combination):] == combination:
        return True
    return False

key_history = []

while running:
    screen.fill(WHITE)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key_history.append(event.key)
            if len(key_history) > 10:  # Keep only last 10 keys
                key_history.pop(0)
                
            # Check for special combination
            if check_special_combination(key_history):
                rainbow_mode = not rainbow_mode
                secret_message = "RAINBOW MODE!" if rainbow_mode else "Rainbow mode off"
                message_timer = 100
                
            # God mode (hidden)
            if event.key == pygame.K_g and event.mod & pygame.KMOD_CTRL:
                god_mode = not god_mode
                secret_message = "GOD MODE!" if god_mode else "Mortal again"
                message_timer = 100
                
            # Normal controls
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)
    
    # Move snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    # Collision with walls or itself (unless in god mode)
    if not god_mode and (new_head in snake or new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT):
        running = False
    
    snake.insert(0, new_head)
    
    # Eating food
    if new_head == food:
        score += 1
        food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
        
        # 10% chance to spawn special food
        if random.random() < 0.1 and not special_food:
            special_food = (random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
                           random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE)
            special_food_timer = 300  # 300 frames = ~30 seconds at 10 FPS
    else:
        snake.pop()
    
    # Check special food
    if special_food:
        special_food_timer -= 1
        if special_food_timer <= 0:
            special_food = None
            
        if new_head == special_food:
            score += 5
            secret_message = "SPECIAL FOOD! +5 points"
            message_timer = 100
            special_food = None
    
    # Draw snake with rainbow colors if enabled
    for i, segment in enumerate(snake):
        if rainbow_mode:
            color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
        else:
            color = GREEN
        pygame.draw.rect(screen, color, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    # Draw food
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))
    
    # Draw special food
    draw_special_food()
    
    # Show score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # Show secret message
    if message_timer > 0:
        message_timer -= 1
    show_secret_message()
    
    # Easter egg: Draw a hidden smiley when score is 42
    if score == 42:
        pygame.draw.circle(screen, (255, 255, 0), (WIDTH - 30, 30), 15)
        pygame.draw.circle(screen, BLACK, (WIDTH - 35, 25), 3)
        pygame.draw.circle(screen, BLACK, (WIDTH - 25, 25), 3)
        pygame.draw.arc(screen, BLACK, (WIDTH - 35, 30, 20, 10), 0, math.pi, 2)
    
    pygame.display.update()
    clock.tick(10)

# Game over message
screen.fill(WHITE)
game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
pygame.display.update()
pygame.time.wait(2000)  # Show message for 2 seconds

pygame.quit()
