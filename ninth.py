import pygame
import random
import math
import time

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
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]

# Font
font = pygame.font.SysFont('Arial', 24)
big_font = pygame.font.SysFont('Arial', 48)

# Player settings
player_pos = [GRID_SIZE, GRID_SIZE]
player_color = RED
goal_pos = [WIDTH - 2 * GRID_SIZE, HEIGHT - 2 * GRID_SIZE]

# Obstacles
num_obstacles = 8
obstacles = []
mirrors = []  # New: Mirrors that reflect movement
teleports = []  # New: Teleport pairs

# Game state
running = True
game_won = False
level = 1
moves = 0
show_help = False
secret_activated = False
cheat_sequence = []
konami_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
               pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT,
               pygame.K_b, pygame.K_a]

# Particles for effects
particles = []

def generate_level():
    global obstacles, mirrors, teleports, player_pos, goal_pos
    
    obstacles = []
    mirrors = []
    teleports = []
    
    # Generate obstacles
    for _ in range(num_obstacles + level):
        x = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
        y = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
        if (x, y) != tuple(player_pos) and (x, y) != tuple(goal_pos):
            obstacles.append((x, y))
    
    # Generate mirrors (fewer than obstacles)
    for _ in range(min(level, 3)):
        x = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE
        y = random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
        if (x, y) not in obstacles and (x, y) != tuple(player_pos) and (x, y) != tuple(goal_pos):
            mirrors.append((x, y))
    
    # Generate teleport pairs (1 pair every 3 levels)
    if level >= 3 and len(teleports) == 0:
        for _ in range(level // 3):
            x1, y1 = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE, random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
            x2, y2 = random.randint(1, (WIDTH // GRID_SIZE) - 2) * GRID_SIZE, random.randint(1, (HEIGHT // GRID_SIZE) - 2) * GRID_SIZE
            if (x1, y1) not in obstacles and (x2, y2) not in obstacles and \
               (x1, y1) != tuple(player_pos) and (x2, y2) != tuple(goal_pos):
                teleports.append(((x1, y1), (x2, y2)))

def create_particles(x, y, color):
    for _ in range(15):
        particles.append({
            'x': x,
            'y': y,
            'dx': random.uniform(-2, 2),
            'dy': random.uniform(-2, 2),
            'size': random.randint(2, 5),
            'life': random.randint(20, 40),
            'color': color
        })

def update_particles():
    for p in particles[:]:
        p['x'] += p['dx']
        p['y'] += p['dy']
        p['life'] -= 1
        if p['life'] <= 0:
            particles.remove(p)

def draw_particles():
    for p in particles:
        pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['size'])

def check_teleport(pos):
    for tp in teleports:
        if (pos[0], pos[1]) == tp[0]:
            create_particles(pos[0] + GRID_SIZE//2, pos[1] + GRID_SIZE//2, PURPLE)
            return list(tp[1])
        elif (pos[0], pos[1]) == tp[1]:
            create_particles(pos[0] + GRID_SIZE//2, pos[1] + GRID_SIZE//2, PURPLE)
            return list(tp[0])
    return pos

def check_mirror_effect(pos, key):
    for mirror in mirrors:
        if (pos[0], pos[1]) == mirror:
            # Mirror reverses movement again (since movement is already mirrored)
            if key == pygame.K_LEFT: return pygame.K_RIGHT
            if key == pygame.K_RIGHT: return pygame.K_LEFT
            if key == pygame.K_UP: return pygame.K_DOWN
            if key == pygame.K_DOWN: return pygame.K_UP
    return key

def check_cheat_code(key):
    global secret_activated, player_color
    cheat_sequence.append(key)
    if len(cheat_sequence) > len(konami_code):
        cheat_sequence.pop(0)
    if cheat_sequence == konami_code:
        secret_activated = True
        player_color = random.choice(COLORS)
        create_particles(player_pos[0] + GRID_SIZE//2, player_pos[1] + GRID_SIZE//2, player_color)
        return True
    return False

# Generate first level
generate_level()

# Main game loop
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_won:
                if event.key == pygame.K_n:
                    level += 1
                    player_pos = [GRID_SIZE, GRID_SIZE]
                    moves = 0
                    game_won = False
                    generate_level()
                elif event.key == pygame.K_q:
                    running = False
            elif event.key == pygame.K_h:
                show_help = not show_help
            elif event.key == pygame.K_r:
                player_pos = [GRID_SIZE, GRID_SIZE]
                moves = 0
            else:
                # Check for cheat codes
                check_cheat_code(event.key)
                
                # Movement handling
                original_key = event.key
                new_key = check_mirror_effect(player_pos, original_key)
                
                new_pos = player_pos.copy()
                if new_key == pygame.K_LEFT and new_pos[0] + GRID_SIZE < WIDTH:
                    new_pos[0] += GRID_SIZE
                elif new_key == pygame.K_RIGHT and new_pos[0] - GRID_SIZE >= 0:
                    new_pos[0] -= GRID_SIZE
                elif new_key == pygame.K_UP and new_pos[1] + GRID_SIZE < HEIGHT:
                    new_pos[1] += GRID_SIZE
                elif new_key == pygame.K_DOWN and new_pos[1] - GRID_SIZE >= 0:
                    new_pos[1] -= GRID_SIZE
                
                # Check teleport before collision
                new_pos = check_teleport(new_pos)
                
                # Check collision with obstacles
                if tuple(new_pos) not in obstacles:
                    player_pos = new_pos
                    moves += 1
                    
                    # Secret: change color when moving (if cheat activated)
                    if secret_activated and random.random() < 0.3:
                        player_color = random.choice(COLORS)
                
                # Check if reached goal
                if tuple(player_pos) == tuple(goal_pos):
                    create_particles(goal_pos[0] + GRID_SIZE//2, goal_pos[1] + GRID_SIZE//2, GREEN)
                    game_won = True
    
    # Drawing
    screen.fill(WHITE)
    
    # Draw grid (faint)
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))
    
    # Draw obstacles
    for obs in obstacles:
        pygame.draw.rect(screen, BLACK, (obs[0], obs[1], GRID_SIZE, GRID_SIZE))
    
    # Draw mirrors
    for mirror in mirrors:
        pygame.draw.rect(screen, BLUE, (mirror[0], mirror[1], GRID_SIZE, GRID_SIZE))
        # Draw diagonal line to indicate mirror
        pygame.draw.line(screen, WHITE, (mirror[0], mirror[1]), 
                         (mirror[0] + GRID_SIZE, mirror[1] + GRID_SIZE), 3)
    
    # Draw teleports
    for tp in teleports:
        pygame.draw.rect(screen, PURPLE, (tp[0][0], tp[0][1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, PURPLE, (tp[1][0], tp[1][1], GRID_SIZE, GRID_SIZE))
        # Draw "T" symbol
        t_font = pygame.font.SysFont('Arial', 30)
        t_text = t_font.render("T", True, WHITE)
        screen.blit(t_text, (tp[0][0] + GRID_SIZE//2 - t_text.get_width()//2, 
                            tp[0][1] + GRID_SIZE//2 - t_text.get_height()//2))
        screen.blit(t_text, (tp[1][0] + GRID_SIZE//2 - t_text.get_width()//2, 
                            tp[1][1] + GRID_SIZE//2 - t_text.get_height()//2))
    
    # Draw goal
    pygame.draw.rect(screen, GREEN, (goal_pos[0], goal_pos[1], GRID_SIZE, GRID_SIZE))
    goal_text = font.render("GOAL", True, WHITE)
    screen.blit(goal_text, (goal_pos[0] + GRID_SIZE//2 - goal_text.get_width()//2, 
                           goal_pos[1] + GRID_SIZE//2 - goal_text.get_height()//2))
    
    # Draw player
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], GRID_SIZE, GRID_SIZE))
    
    # Draw particles
    update_particles()
    draw_particles()
    
    # Draw HUD
    level_text = font.render(f"Level: {level}", True, BLACK)
    moves_text = font.render(f"Moves: {moves}", True, BLACK)
    screen.blit(level_text, (10, 10))
    screen.blit(moves_text, (10, 40))
    
    if secret_activated:
        cheat_text = font.render("SECRET MODE!", True, PURPLE)
        screen.blit(cheat_text, (WIDTH - cheat_text.get_width() - 10, 10))
    
    # Help screen
    if show_help:
        help_surface = pygame.Surface((WIDTH - 100, HEIGHT - 100), pygame.SRCALPHA)
        help_surface.fill((50, 50, 50, 200))
        screen.blit(help_surface, (50, 50))
        
        help_title = big_font.render("Mirror Maze Help", True, WHITE)
        screen.blit(help_title, (WIDTH//2 - help_title.get_width()//2, 70))
        
        help_lines = [
            "Movement is MIRRORED (left moves right, up moves down)",
            "Blue mirrors DOUBLE the mirror effect",
            "Purple teleports (T) transport you to their pair",
            "Press R to reset position",
            "Press H to toggle this help",
            "Find the hidden Konami code cheat!",
            "",
            "Press H to close"
        ]
        
        for i, line in enumerate(help_lines):
            text = font.render(line, True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 130 + i * 30))
    
    # Win screen
    if game_won:
        win_surface = pygame.Surface((WIDTH - 100, HEIGHT - 100), pygame.SRCALPHA)
        win_surface.fill((0, 100, 0, 200))
        screen.blit(win_surface, (50, 50))
        
        win_text = big_font.render("Level Complete!", True, WHITE)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - 60))
        
        stats_text = font.render(f"Level {level} completed in {moves} moves", True, WHITE)
        screen.blit(stats_text, (WIDTH//2 - stats_text.get_width()//2, HEIGHT//2))
        
        next_text = font.render("Press N for next level or Q to quit", True, WHITE)
        screen.blit(next_text, (WIDTH//2 - next_text.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.flip()

pygame.quit()
