import pygame
import random
import time
from settings import WIDTH, HEIGHT
from lcs import find_lcs, is_subsequence
from ui import draw_screen
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
database_url = os.getenv('DATABASE_URL')
secret_key = os.getenv('SECRET_KEY')

class LCSGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("LCS Algorithm Game")

        self.score = 0
        self.level = 1
        self.running = True
        self.game_state = "playing"

        self.word_pairs = [
            ("HELLO", "WORLD"),
            ("PYTHON", "PROGRAMMING"),
            ("ALGORITHM", "ARITHMETIC"),
            ("SEQUENCE", "SCIENCE"),
            ("COMPUTER", "COMMUTER"),
        ]
        
        self.current_pair = self.get_new_word_pair()
        self.user_sequence = ""
        self.correct_sequence = None
        self.start_time = time.time()
        self.time_limit = 60

    def get_new_word_pair(self):
        """Return a new random pair of words."""
        return random.choice(self.word_pairs)

    def check_user_sequence(self):
        """Check if user input is a valid subsequence of both words."""
        word1, word2 = self.current_pair
        return is_subsequence(self.user_sequence, word1) and is_subsequence(self.user_sequence, word2)

    def run(self):
        """Main game loop."""
        while self.running:
            for event in pygame.event.get():
                from input_handler import handle_input
                handle_input(event, self)

            time_remaining = max(0, self.time_limit - (time.time() - self.start_time))
            draw_screen(self.screen, self.current_pair, self.user_sequence, self.score, self.level, time_remaining, self.game_state, self.correct_sequence)

            if time_remaining <= 0:
                self.running = False

        pygame.quit()
        print(f"Final Score: {self.score}")
        print(f"Final Level: {self.level}")
