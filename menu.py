import pygame
import json
import os
from settings import WIDTH, HEIGHT, WHITE, BLACK, GREEN, FONT_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the absolute path of the script's directory

# Load highest score from JSON
SCORE_FILE = os.path.join(BASE_DIR, "assets", "score.json") 

# remove background
BG_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "sun.png") 


def load_existing_data():
    """Load the existing score data, handling missing or corrupted files."""
    if os.path.exists(SCORE_FILE):
        print(f"Load Score Path: {SCORE_FILE}")
        with open(SCORE_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def load_highest_score():
    """Load the highest score, returning 0 if not found."""
    return load_existing_data().get("highest_score", 0)

def load_highest_level():
    """Load the highest level, returning 0 if not found."""
    return load_existing_data().get("highest_level", 0)

def save_highest_score(score):
    """Update the highest score while preserving other fields."""
    data = load_existing_data()
    data["highest_score"] = score
    save_data(data)

def save_highest_level(level):
    """Update the highest level while preserving other fields."""
    data = load_existing_data()
    data["highest_level"] = level
    save_data(data)

def save_data(data):
    """Ensure the directory exists before saving the updated score data."""
    os.makedirs(os.path.dirname(SCORE_FILE), exist_ok=True)  # ✅ Create directory if missing
    print(f"Save Score Path: {SCORE_FILE}")
    with open(SCORE_FILE, "w") as file:
        json.dump(data, file)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LCS Game Menu")

class Menu:
    """Class representing the game menu."""

    def __init__(self):
        """Initialize the menu."""
        self.menu_items = ["Start Game", "Tutorial", "Quit"]
        self.selected_item = 0
        self.running = True
        self.highest_score = load_highest_score()
        self.highest_level = load_highest_level()
        self.update_dimensions()

        # load BG
        self.bg_image = pygame.image.load(BG_IMAGE_PATH)
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

    def update_dimensions(self):
        """Update menu dimensions based on the current screen size."""
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.Font(FONT_PATH, int(self.screen_height * 0.05))
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2.5

    def draw(self):
        """Draw the menu on the screen."""
        # screen.fill(BLACK)
        screen.blit(self.bg_image, (0, 0))
        for idx, item in enumerate(self.menu_items):
            color = GREEN if idx == self.selected_item else WHITE
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(self.center_x, self.center_y + idx * int(self.screen_height * 0.1)))
            screen.blit(text, text_rect)
        score_text = self.font.render(f"Highest Score: {self.highest_score}", True, BLACK)
        score_rect = score_text.get_rect(topright=(WIDTH - 50, 30))
        screen.blit(score_text, score_rect)
        level_text = self.font.render(f"Highest Level: {self.highest_level}", True, BLACK)
        level_rect = score_text.get_rect(topleft=(50, 30))
        screen.blit(level_text, level_rect)
        pygame.display.flip()

    def handle_input(self):
        """Handle user input for menu navigation."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    if self.selected_item == 0:
                        return "start"
                    elif self.selected_item == 1:
                        return "tutorial"
                    elif self.selected_item == 2:
                        return "quit"
        return "none"

def init_menu():
    """Initialize and display the menu."""
    menu = Menu()
    while menu.running:
        menu.update_dimensions()
        menu.draw()
        action = menu.handle_input()
        if action in ["start", "tutorial", "quit"]:
            return action
        pygame.time.Clock().tick(30)