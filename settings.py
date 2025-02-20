import pygame
import os

# Screen dimensions
WIDTH = 1024
HEIGHT = 768

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (40, 40, 40)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)

# Initialize Pygame
pygame.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the script's directory

FONT_PATH = os.path.join(BASE_DIR, "assets", "fontvit.otf") 

FONT = pygame.font.Font(FONT_PATH, 28)  # lcs