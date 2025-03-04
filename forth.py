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
