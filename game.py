import pygame
import random
import time
from settings import WIDTH, HEIGHT
from lcs import find_lcs, is_subsequence
from ui import draw_screen
from dotenv import load_dotenv
import os
import nltk
from nltk.corpus import words

# Download words dataset (Run once)
nltk.download("words")

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

        # Load a list of words from NLTK
        self.word_list = words.words()
        
        self.current_pair = self.get_new_word_pair()
        self.user_sequence = ""
        self.correct_sequence = None
        self.start_time = time.time()
        self.time_limit = 60

    def generate_random_word_pair(self, min_length=5, max_length=10):
        """Generate a new random pair of words with a specified length range."""
        filtered_words = [word.upper() for word in self.word_list if min_length <= len(word) <= max_length]
        
        if len(filtered_words) < 2:
            raise ValueError("Not enough words available in the specified length range.")
        
        word1 = random.choice(filtered_words)
        word2 = random.choice(filtered_words)
        
        return word1, word2

    
    def get_new_word_pair(self):
        """Return a new random pair of words."""
        return self.generate_random_word_pair()

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
