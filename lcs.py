import pygame
import random
import time
import nltk
from collections import defaultdict
from settings import WIDTH, HEIGHT, FONT, WHITE, BLACK, GREEN, RED, BLUE
from menu import save_highest_score, load_highest_score, save_highest_level, load_highest_level

nltk.download("words")

class LCSGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("LCS Algorithm Game")
        self.score = 0
        self.level = 1
        self.running = True
        self.game_state = "playing"
        self.word_list = nltk.corpus.words.words()
        self.current_pair = self.get_new_word_pair()
        self.user_sequence = ""
        self.correct_sequence = None
        self.start_time = time.time()
        self.time_limit = 60

    def generate_random_word_pair(self, min_length=5, max_length=10):
        filtered_words = [word.upper() for word in self.word_list if min_length <= len(word) <= max_length]
        if len(filtered_words) < 2:
            raise ValueError("Not enough words available in the specified length range.")
        word1 = random.choice(filtered_words)
        word2 = random.choice(filtered_words)
        return word1, word2

    def get_new_word_pair(self):
        return self.generate_random_word_pair()

    def check_user_sequence(self):
        word1, word2 = self.current_pair
        return self.is_subsequence(self.user_sequence, word1) and self.is_subsequence(self.user_sequence, word2)

    def run(self):
        pygame.mixer.init()
        while self.running:
            for event in pygame.event.get():
                self.event = event
                action = self.handle_input(event)
                if action == "exit_to_menu":
                    return "exit_to_menu"
            time_remaining = max(0, self.time_limit - (time.time() - self.start_time))
            self.draw_screen(time_remaining)
            if time_remaining <= 0:
                self.running = False

        highest_score = load_highest_score()
        highest_level = load_highest_level()
        new_high_score = self.score > highest_score
        new_high_level = self.level > highest_level
        
        if new_high_score or new_high_level:
            if new_high_level:
                save_highest_level(self.level)
                self.show_congratulations(f"New High Level: {self.level}!")
            if new_high_score:
                save_highest_score(self.score)
                self.show_congratulations(f"New High Score: {self.score}!")
        
        print(f"Final Score: {self.score}")
        print(f"Final Level: {self.level}")

    def draw_screen(self, time_remaining):
        self.screen.fill(BLACK)
        word1, word2 = self.current_pair
        self.screen.blit(FONT.render(f"Word 1: {word1}", True, WHITE), (50, 50))
        self.screen.blit(FONT.render(f"Word 2: {word2}", True, WHITE), (50, 100))
        sequence_color = GREEN if self.game_state == "playing" else RED
        self.screen.blit(FONT.render(f"Your sequence: {self.user_sequence}", True, sequence_color), (50, 200))
        self.screen.blit(FONT.render(f"Score: {self.score}", True, WHITE), (50, 300))
        self.screen.blit(FONT.render(f"Level: {self.level}", True, WHITE), (50, 350))
        self.screen.blit(FONT.render(f"Time: {int(time_remaining)}s", True, WHITE), (50, 400))
        instructions = [
            "Instructions:",
            "- Type letters to build a common subsequence",
            "- Press ENTER to submit",
            "- Press BACKSPACE to delete",
            "- Press SPACE to see solution",
            "- Press ESC to quit",
        ]
        for i, instruction in enumerate(instructions):
            self.screen.blit(FONT.render(instruction, True, WHITE), (50, 500 + i * 40))
        pygame.display.flip()
        
    def handle_input(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return "exit_to_menu"
            elif event.key == pygame.K_RETURN:
                if self.check_user_sequence():
                    correct_lcs = self.find_lcs(*self.current_pair)
                    if len(self.user_sequence) == len(correct_lcs):
                        try:
                            correct_sound = pygame.mixer.Sound("assets/correct.mp3")  
                            correct_sound.play()
                        except Exception as e:
                            print("Error loading sound:", e)
                        self.score += len(self.user_sequence) * 10
                        self.level += 1
                        self.current_pair = self.get_new_word_pair()
                        self.user_sequence = ""
                        self.game_state = "playing"
                    else:
                        self.wrong_answer_effect()
                else:
                    self.wrong_answer_effect()
            elif event.key == pygame.K_BACKSPACE:
                self.user_sequence = self.user_sequence[:-1]
            elif event.key == pygame.K_SPACE:
                self.correct_sequence = self.find_lcs(*self.current_pair)
                self.game_state = "showing_solution"
                self.highlight_correct_sequence()
            elif event.unicode.isalpha():
                self.user_sequence += event.unicode.upper()
    
    def highlight_correct_sequence(self):
        """Highlight correct LCS sequence for 3 seconds."""
        word1, word2 = self.current_pair
        lcs = self.correct_sequence

        def render_word_with_highlight(word, lcs):
            """Returns a rendered word where LCS characters are highlighted in GREEN."""
            text_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            x, y = 50, 50  # Position of words
            offset_x = 0

            for char in word:
                color = GREEN if char in lcs else WHITE
                char_surface = FONT.render(char, True, color)
                text_surface.blit(char_surface, (x + offset_x, y))
                offset_x += char_surface.get_width() + 5  # Space between characters
            return text_surface

        # Highlight LCS in both words
        word1_surface = render_word_with_highlight(word1, lcs)
        word2_surface = render_word_with_highlight(word2, lcs)

        self.screen.fill(BLACK)
        self.screen.blit(word1_surface, (50, 50))
        self.screen.blit(word2_surface, (50, 100))
        self.screen.blit(FONT.render(f"Solution: {lcs}", True, BLUE), (50, 250))
        instructions = [
            "Instructions:",
            "- Type letters to build a common subsequence",
            "- Press ENTER to submit",
            "- Press BACKSPACE to delete",
            "- Press SPACE to see solution",
            "- Press ESC to quit",
        ]
        for i, instruction in enumerate(instructions):
            self.screen.blit(FONT.render(instruction, True, WHITE), (50, 500 + i * 40))
        pygame.display.flip()

        pygame.time.delay(2000)  # Show for 3 seconds
        self.game_state = "playing"  # Return to normal gameplay

                
    def show_congratulations(self, message):
        """Displays a congratulatory message on the screen."""
        self.screen.fill(BLACK)
        congrats_text = FONT.render(message, True, GREEN)
        text_rect = congrats_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(congrats_text, text_rect)
        pygame.display.flip()
        
        try:
            win_sound = pygame.mixer.Sound("assets/win.wav")  
            win_sound.play()
        except Exception as e:
            print("Error loading sound:", e)
        
        pygame.time.delay(2000)  # Show message for 2 seconds

    def wrong_answer_effect(self):
        original_x, original_y = 50, 50  # Original position of the word
        shake_amount = 5  # Number of pixels the word will "shake"
        shake_count = 10  # Number of shakes
        shake_delay = 30  # Delay between shakes in milliseconds
        
        try:
            error_sound = pygame.mixer.Sound("assets/wrong.mp3")  # Ensure the file exists
            error_sound.play()
        except Exception as e:
            print("Error loading sound:", e)
        
        # Shake effect
        
        for _ in range(shake_count):
            offset_x = random.randint(-shake_amount, shake_amount)
            offset_y = random.randint(-shake_amount, shake_amount)
            self.screen.fill(BLACK)  # Fill screen with black for clean slate
            word1, word2 = self.current_pair  # Get current words to display
            self.screen.blit(FONT.render(f"Word 1: {word1}", True, WHITE), (original_x + offset_x, original_y + offset_y))
            self.screen.blit(FONT.render(f"Word 2: {word2}", True, WHITE), (original_x + offset_x, original_y + 50 + offset_y))
            if (self.user_sequence != ""):
                self.screen.blit(FONT.render(f"Your sequence: {self.user_sequence}", True, RED), (original_x + offset_x, original_y + 150 + offset_y))
            pygame.display.flip()
            pygame.time.delay(shake_delay)
        
        # Clear screen or make the word disappear after shake
        self.screen.fill(BLACK)  # Clear screen
        pygame.display.flip()

        # Reset user sequence after shake effect
        self.user_sequence = ""  # Reset user input
        self.game_state = "playing"  # Return to playing state

    def find_lcs(self, str1, str2):
        m, n = len(str1), len(str2)
        pos = defaultdict(list)
        for j in range(n):
            pos[str2[j]].append(j)
        lcs = []
        last_j = -1
        for i in range(m):
            if str1[i] in pos:
                for j in reversed(pos[str1[i]]):
                    if j > last_j:
                        lcs.append(str1[i])
                        last_j = j
                        break
        return ''.join(lcs)

    def is_subsequence(self, s, t):
        s_idx = 0
        for char in t:
            if s_idx < len(s) and char == s[s_idx]:
                s_idx += 1
        return s_idx == len(s)