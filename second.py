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
