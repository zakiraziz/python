import pygame
import random
import math
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # For sound effects

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Enhanced")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
COLORS = [WHITE, RED, YELLOW, GREEN]

# Load sounds (placeholder - add your own sound files)
try:
    jump_sound = pygame.mixer.Sound("jump.wav")
    score_sound = pygame.mixer.Sound("score.wav")
    crash_sound = pygame.mixer.Sound("crash.wav")
except:
    # Create dummy sound objects if files not found
    jump_sound = pygame.mixer.Sound(pygame.sndarray.array(bytearray(100)))
    score_sound = pygame.mixer.Sound(pygame.sndarray.array(bytearray(100)))
    crash_sound = pygame.mixer.Sound(pygame.sndarray.array(bytearray(100)))

# Bird settings
bird = pygame.Rect(100, HEIGHT//2, 30, 30)
gravity = 0.5
velocity = 0
bird_color = WHITE
flap_power = -7
rotation_angle = 0
bird_images = []  # For animated bird

# Create simple bird animation frames (colored circles)
for color in COLORS:
    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.ellipse(surf, color, (0, 0, 30, 30))
    pygame.draw.ellipse(surf, BLACK, (0, 0, 30, 30), 2)  # Outline
    bird_images.append(surf)

# Pipe settings
pipe_width = 70
pipe_gap = 150
pipe_speed = 3
pipes = []
pipe_color = GREEN
last_pipe_time = 0
pipe_frequency = 1500  # milliseconds

# Game state
running = True
game_over = False
score = 0
high_score = 0
flap_count = 0
start_time = time.time()
particles = []
cheat_sequence = []
konami_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
               pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT,
               pygame.K_b, pygame.K_a]
cheat_active = False

# Background elements
clouds = []
for _ in range(5):
    clouds.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT//2),
        'speed': random.uniform(0.2, 0.5),
        'size': random.randint(30, 60)
    })

def create_pipe():
    height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    pipes.extend([top_pipe, bottom_pipe])
    return height

def create_particles(x, y, color, count=10):
    for _ in range(count):
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

def check_cheat_code(key):
    global cheat_active, bird_color, flap_power, pipe_speed
    cheat_sequence.append(key)
    if len(cheat_sequence) > len(konami_code):
        cheat_sequence.pop(0)
    if cheat_sequence == konami_code:
        cheat_active = not cheat_active
        if cheat_active:
            bird_color = random.choice(COLORS)
            flap_power = -10
            pipe_speed = 2
            create_particles(bird.x, bird.y, YELLOW, 30)
        else:
            flap_power = -7
            pipe_speed = 3
        return True
    return False

def draw_bird():
    # Rotate bird based on velocity
    rotation_angle = min(max(-velocity * 3, -30), 30)  # Limit rotation angle
    
    # Get current bird image (cycle through colors if cheat active)
    bird_img = bird_images[COLORS.index(bird_color)] if not cheat_active else bird_images[int(time.time()*10) % len(bird_images)]
    
    # Rotate the bird image
    rotated_bird = pygame.transform.rotate(bird_img, rotation_angle)
    screen.blit(rotated_bird, (bird.x - rotated_bird.get_width()//2 + 15, 
                              bird.y - rotated_bird.get_height()//2 + 15))

def draw_clouds():
    for cloud in clouds:
        pygame.draw.circle(screen, WHITE, (int(cloud['x']), int(cloud['y'])), cloud['size'])
        pygame.draw.circle(screen, WHITE, (int(cloud['x']) + cloud['size']//2, int(cloud['y'])), cloud['size']//2)
        pygame.draw.circle(screen, WHITE, (int(cloud['x']) - cloud['size']//2, int(cloud['y'])), cloud['size']//2)

def update_clouds():
    for cloud in clouds:
        cloud['x'] -= cloud['speed']
        if cloud['x'] < -cloud['size']:
            cloud['x'] = WIDTH + cloud['size']
            cloud['y'] = random.randint(0, HEIGHT//2)

def show_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    font_large = pygame.font.SysFont('Arial', 48)
    font_small = pygame.font.SysFont('Arial', 24)
    
    game_over_text = font_large.render("Game Over", True, WHITE)
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    high_score_text = font_small.render(f"High Score: {high_score}", True, WHITE)
    restart_text = font_small.render("Press R to Restart", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//3))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 40))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))

# Initial pipe
create_pipe()
last_pipe_time = pygame.time.get_ticks()

# Main game loop
while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over and event.key == pygame.K_SPACE:
                velocity = flap_power
                flap_count += 1
                jump_sound.play()
                create_particles(bird.x + 15, bird.y + 15, WHITE, 5)
            elif game_over and event.key == pygame.K_r:
                # Reset game
                bird.y = HEIGHT//2
                velocity = 0
                pipes = []
                create_pipe()
                last_pipe_time = pygame.time.get_ticks()
                score = 0
                game_over = False
                particles = []
            elif event.key == pygame.K_h:
                # Toggle hitboxes (debug)
                pass  # Add hitbox visualization if needed
            else:
                check_cheat_code(event.key)  # Check for cheat codes
    
    if not game_over:
        # Bird movement
        velocity += gravity
        bird.y += velocity
        
        # Cloud movement
        update_clouds()
        
        # Pipe generation
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe_time > pipe_frequency:
            create_pipe()
            last_pipe_time = current_time
        
        # Pipe movement
        for pipe in pipes[:]:
            pipe.x -= pipe_speed
            
            # Score point when passing a pipe
            if pipe.right == bird.left and pipe.width == pipe_width:  # Only check once per pipe pair
                score += 1
                score_sound.play()
                high_score = max(score, high_score)
                create_particles(pipe.right, bird.y, YELLOW, 15)
        
        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.right > 0]
        
        # Check collisions
        if (bird.y > HEIGHT or bird.y < 0 or 
            any(pipe.colliderect(bird) for pipe in pipes)):
            crash_sound.play()
            create_particles(bird.x + 15, bird.y + 15, RED, 30)
            game_over = True
    
    # Drawing
    screen.fill(BLUE)
    
    # Draw background elements
    draw_clouds()
    
    # Draw pipes with outline
    for pipe in pipes:
        pygame.draw.rect(screen, pipe_color, pipe)
        pygame.draw.rect(screen, BLACK, pipe, 2)  # Outline
    
    # Draw particles
    update_particles()
    draw_particles()
    
    # Draw bird
    draw_bird()
    
    # Draw score
    font = pygame.font.SysFont('Arial', 36)
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 50))
    
    # Cheat indicator
    if cheat_active:
        cheat_text = font.render("CHEAT MODE", True, RED)
        screen.blit(cheat_text, (10, 10))
    
    # Game over screen
    if game_over:
        show_game_over()
    
    pygame.display.flip()

pygame.quit()
