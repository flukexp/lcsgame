import pygame
import random
import time
import nltk
import math
from collections import defaultdict
from settings import WIDTH, HEIGHT, FONT, WHITE, BLACK, GREEN, RED, BLUE, DARK_GREEN, GRAY, LIGHT_GRAY
from menu import save_highest_score, load_highest_score, save_highest_level, load_highest_level

nltk.download("words")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# remove background
BG_IMAGE_PATH = "assets/sun.png"


class LCSGame:
    def __init__(self):
        self.screen_width, self.screen_height = screen.get_size()
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2

        # Improved fonts with better sizing
        self.title_font = pygame.font.Font(None, int(self.screen_height * 0.08))
        self.font = pygame.font.Font(None, int(self.screen_height * 0.05))
        self.small_font = pygame.font.Font(None, int(self.screen_height * 0.03))
        
        # load BG
        self.bg_image = pygame.image.load(BG_IMAGE_PATH)
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

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

        # Animation variables
        self.animation_counter = 0
        self.animation_speed = 2

    def draw_rounded_rect(self, surface, rect, color, radius=20):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

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
        clock = pygame.time.Clock()
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
            
            self.animation_counter += self.animation_speed
            pygame.display.flip()
            clock.tick(60)


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

        # self.screen.fill(BLACK)
        # เพิ่ม background
        self.screen.blit(self.bg_image, (0, 0))

        pulse = abs(math.sin(self.animation_counter / 30)) * 10
        title_size = int(self.screen_height * 0.08 + pulse)
        title_font = pygame.font.Font("assets/fontvit.otf", title_size)
        title_text = title_font.render("LCS Game!", True, BLACK)
        title_rect = title_text.get_rect(center=(self.center_x, self.screen_height // 10))
        screen.blit(title_text, title_rect)

        add_y = 100
        control_rect = pygame.Rect(30, 30+ add_y, 964, 420)
        self.draw_rounded_rect(screen, control_rect, GRAY)

        control_rect = pygame.Rect(40, 40+add_y, 944, 95)
        self.draw_rounded_rect(screen, control_rect, DARK_GREEN)

        control_rect = pygame.Rect(40, 170+add_y, 944, 90)
        self.draw_rounded_rect(screen, control_rect, WHITE)

        word1, word2 = self.current_pair
        self.screen.blit(FONT.render(f"Word 1: {word1}", True, WHITE), (50, 50+add_y))
        self.screen.blit(FONT.render(f"Word 2: {word2}", True, WHITE), (50, 100+add_y))
        sequence_color = GREEN if self.game_state == "playing" else RED
        self.screen.blit(FONT.render(f"Your sequence:", True, sequence_color), (50, 200+add_y))
        self.screen.blit(FONT.render(f"{self.user_sequence}", True, BLACK), (280, 200+add_y))
        self.screen.blit(FONT.render(f"Score: {self.score}", True, WHITE), (50, 300+add_y))
        self.screen.blit(FONT.render(f"Level: {self.level}", True, WHITE), (50, 350+add_y))
        self.screen.blit(FONT.render(f"Time: {int(time_remaining)}s", True, WHITE), (50, 400+add_y))
        # instructions = [
        #     "Instructions:",
        #     "- Type letters to build a common subsequence",
        #     "- Press ENTER to submit",
        #     "- Press BACKSPACE to delete",
        #     "- Press SPACE to see solution",
        #     "- Press ESC to quit",
        # ]

        # control_rect = pygame.Rect(30, 480, 964, 260)
        # self.draw_rounded_rect(screen, control_rect, GRAY)

        # control_rect = pygame.Rect(40, 490, 180, 45)
        # self.draw_rounded_rect(screen, control_rect, DARK_GREEN)

        # for i, instruction in enumerate(instructions):
        #     self.screen.blit(FONT.render(instruction, True, WHITE), (50, 500 + i * 40))

        
        self.draw_controls()

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

        # self.screen.fill(BLACK)
        self.screen.blit(self.bg_image, (0, 0))

        card_rect = pygame.Rect(
            self.center_x - 300,
            self.screen_height // 4 - 50,
            600,
            300
        )
        self.draw_rounded_rect(screen, card_rect, GRAY)

        number_rect = pygame.Rect(
            card_rect.left + 20,
            card_rect.top + 20,
            200,
            40
        )
        self.draw_rounded_rect(screen, number_rect, DARK_GREEN)

        example_text = self.font.render(f"Solution", True, WHITE)
        example_rect = example_text.get_rect(center=number_rect.center)
        screen.blit(example_text, example_rect)

        self.screen.blit(FONT.render('Word 1:', True, WHITE), (270, 240))

        self.screen.blit(FONT.render('Word 2:', True, WHITE), (270, 300))

        self.screen.blit(word1_surface, (370, 190))
        self.screen.blit(word2_surface, (370, 250))

        # self.screen.blit(FONT.render(f"Solution: {lcs}", True, BLUE), (50, 250))

        y_offset = card_rect.top + 100

        result_rect = pygame.Rect(
            card_rect.left + 50,
            y_offset + 120,
            500,
            60
        )

        self.draw_rounded_rect(screen, result_rect, DARK_GREEN)
        result_text = self.font.render(f"Solution: {lcs}", True, WHITE)
        result_rect = result_text.get_rect(center=(result_rect.centerx, result_rect.centery))
        screen.blit(result_text, result_rect)

        # instructions = [
        #     "Instructions:",
        #     "- Type letters to build a common subsequence",
        #     "- Press ENTER to submit",
        #     "- Press BACKSPACE to delete",
        #     "- Press SPACE to see solution",
        #     "- Press ESC to quit",
        # ]

        # control_rect = pygame.Rect(30, 480, 964, 260)
        # self.draw_rounded_rect(screen, control_rect, GRAY)

        # control_rect = pygame.Rect(40, 490, 180, 45)
        # self.draw_rounded_rect(screen, control_rect, DARK_GREEN)

        # for i, instruction in enumerate(instructions):
        #     self.screen.blit(FONT.render(instruction, True, WHITE), (50, 500 + i * 40))

        self.draw_controls()
        
        pygame.display.flip()

        pygame.time.delay(2000)  # Show for 3 seconds
        self.current_pair = self.get_new_word_pair()
        self.user_sequence = ""
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
        shake_delay = 70  # Delay between shakes in milliseconds
        
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
    
    def draw_controls(self):
        # Draw controls in a bottom bar
        control_rect = pygame.Rect(0, self.screen_height - 60, self.screen_width, 60)
        self.draw_rounded_rect(screen, control_rect, DARK_GREEN)
        
        controls = [
            "ENTER: submit",
            "BACKSPACE: delete",
            "SPACE: see solution",
            "ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            x_pos = self.screen_width // 5 * (i + 1) - text.get_width() // 2
            screen.blit(text, (x_pos, self.screen_height - 37))
