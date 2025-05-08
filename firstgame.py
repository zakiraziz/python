import pygame
import random
import math
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 600
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 72)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Enemies")

# Player setup
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5
invincible = False
invincible_timer = 0
shield_active = False
shield_timer = 0

# Enemy setup
enemy_size = 50
enemies = [{"x": random.randint(0, WIDTH - enemy_size), "y": -enemy_size, "speed": 3, "color": RED} for _ in range(3)]

# Power-ups
powerups = []
powerup_types = ["shield", "slow", "clear", "invincible"]
powerup_timer = 0

# Score and level
score = 0
high_score = 0
level = 1
enemy_speed_increase = 0

# Game state
running = True
game_over = False
game_started = False
secret_unlocked = False
cheat_sequence = []
konami_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, 
               pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, 
               pygame.K_b, pygame.K_a]

# Particle effects
particles = []

def create_particles(x, y, color):
    for _ in range(20):
        particles.append({
            "x": x,
            "y": y,
            "dx": random.uniform(-2, 2),
            "dy": random.uniform(-2, 2),
            "size": random.randint(2, 5),
            "life": 30,
            "color": color
        })

def update_particles():
    for particle in particles[:]:
        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]
        particle["life"] -= 1
        if particle["life"] <= 0:
            particles.remove(particle)

def draw_particles():
    for particle in particles:
        pygame.draw.circle(screen, particle["color"], 
                          (int(particle["x"]), int(particle["y"])), particle["size"])

def spawn_powerup():
    if random.random() < 0.01 and len(powerups) < 2:  # 1% chance per frame
        powerup_type = random.choice(powerup_types)
        powerups.append({
            "x": random.randint(0, WIDTH - 30),
            "y": -30,
            "type": powerup_type,
            "speed": 2
        })

def draw_powerup(powerup):
    if powerup["type"] == "shield":
        color = BLUE
    elif powerup["type"] == "slow":
        color = GREEN
    elif powerup["type"] == "clear":
        color = YELLOW
    else:  # invincible
        color = PURPLE
    
    pygame.draw.rect(screen, color, (powerup["x"], powerup["y"], 30, 30))
    pygame.draw.rect(screen, WHITE, (powerup["x"], powerup["y"], 30, 30), 2)

def activate_powerup(powerup_type):
    global shield_active, shield_timer, invincible, invincible_timer
    
    if powerup_type == "shield":
        shield_active = True
        shield_timer = 300  # 5 seconds at 60 FPS
    elif powerup_type == "slow":
        for enemy in enemies:
            enemy["speed"] = max(1, enemy["speed"] - 1)
    elif powerup_type == "clear":
        for enemy in enemies[:]:
            create_particles(enemy["x"] + enemy_size//2, enemy["y"] + enemy_size//2, enemy["color"])
            enemies.remove(enemy)
        # Add new enemies to replace cleared ones
        while len(enemies) < 3:
            enemies.append(create_enemy())
    elif powerup_type == "invincible":
        invincible = True
        invincible_timer = 600  # 10 seconds at 60 FPS

def create_enemy():
    speed = 3 + enemy_speed_increase + random.random() * level * 0.2
    colors = [RED, (255, 165, 0), (255, 0, 255), (0, 255, 255)]
    return {
        "x": random.randint(0, WIDTH - enemy_size),
        "y": -enemy_size,
        "speed": speed,
        "color": random.choice(colors)
    }

def draw_shield():
    if shield_active:
        pygame.draw.circle(screen, (0, 100, 255, 100), 
                          (player_x + player_size//2, player_y + player_size//2), 
                          player_size + 15, 2)

def check_cheat_code(key):
    global secret_unlocked
    cheat_sequence.append(key)
    if len(cheat_sequence) > len(konami_code):
        cheat_sequence.pop(0)
    if cheat_sequence == konami_code:
        secret_unlocked = True
        return True
    return False

# Main game loop
clock = pygame.time.Clock()
while running:
    dt = clock.tick(60)  # Cap at 60 FPS
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_started:
                game_started = True
            if game_over and event.key == pygame.K_r:
                # Reset game
                player_x = WIDTH // 2 - player_size // 2
                enemies = [create_enemy() for _ in range(3)]
                powerups.clear()
                particles.clear()
                score = 0
                level = 1
                enemy_speed_increase = 0
                game_over = False
                shield_active = False
                invincible = False
            # Check for cheat codes
            check_cheat_code(event.key)

    if not game_started:
        # Title screen
        title = BIG_FONT.render("DODGE THE ENEMIES", True, BLUE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        start = FONT.render("Press any key to start", True, RED)
        screen.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2))
        pygame.display.update()
        continue

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        
        # Secret cheat: teleport with space
        if secret_unlocked and keys[pygame.K_SPACE]:
            player_x = random.randint(0, WIDTH - player_size)
            create_particles(player_x + player_size//2, player_y + player_size//2, PURPLE)

        # Enemy movement and spawning
        for enemy in enemies[:]:
            enemy["y"] += enemy["speed"]
            
            # Respawn enemy when off screen
            if enemy["y"] > HEIGHT:
                create_particles(enemy["x"] + enemy_size//2, HEIGHT + enemy_size//2, enemy["color"])
                enemies.remove(enemy)
                enemies.append(create_enemy())
                score += 1

            # Collision detection
            if (not invincible and not shield_active and
                player_x < enemy["x"] + enemy_size and
                player_x + player_size > enemy["x"] and
                player_y < enemy["y"] + enemy_size and
                player_y + player_size > enemy["y"]):
                create_particles(player_x + player_size//2, player_y + player_size//2, RED)
                game_over = True
                high_score = max(high_score, score)

        # Powerup spawning and movement
        spawn_powerup()
        for powerup in powerups[:]:
            powerup["y"] += powerup["speed"]
            
            # Collect powerup
            if (player_x < powerup["x"] + 30 and
                player_x + player_size > powerup["x"] and
                player_y < powerup["y"] + 30 and
                player_y + player_size > powerup["y"]):
                activate_powerup(powerup["type"])
                create_particles(powerup["x"] + 15, powerup["y"] + 15, GREEN)
                powerups.remove(powerup)
            # Remove if off screen
            elif powerup["y"] > HEIGHT:
                powerups.remove(powerup)

        # Update timers
        if shield_active:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False
        if invincible:
            invincible_timer -= 1
            if invincible_timer <= 0:
                invincible = False

        # Level progression
        if score > level * 10:
            level += 1
            enemy_speed_increase += 0.5
            enemies.append(create_enemy())  # Add more enemies each level

        # Update particles
        update_particles()

        # Draw everything
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
        draw_shield()
        
        for enemy in enemies:
            pygame.draw.rect(screen, enemy["color"], (enemy["x"], enemy["y"], enemy_size, enemy_size))
        
        for powerup in powerups:
            draw_powerup(powerup)
        
        draw_particles()

        # Draw HUD
        score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
        level_text = FONT.render(f"Level: {level}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        
        if shield_active:
            shield_text = FONT.render(f"Shield: {shield_timer//60 + 1}s", True, BLUE)
            screen.blit(shield_text, (WIDTH - 150, 10))
        if invincible:
            invincible_text = FONT.render(f"Invincible: {invincible_timer//60 + 1}s", True, PURPLE)
            screen.blit(invincible_text, (WIDTH - 180, 50))
        
        # Secret cheat indicator
        if secret_unlocked:
            cheat_text = FONT.render("CHEATS: ON", True, GREEN)
            screen.blit(cheat_text, (WIDTH - 150, HEIGHT - 30))
    
    else:
        # Game Over screen
        game_over_text = BIG_FONT.render("GAME OVER", True, RED)
        score_text = FONT.render(f"Score: {score} (High: {high_score})", True, (0, 0, 0))
        restart_text = FONT.render("Press R to Restart", True, (0, 0, 0))
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

    pygame.display.update()

pygame.quit()
