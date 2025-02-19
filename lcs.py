import pygame
import random
import time
import nltk
from collections import defaultdict
from settings import WIDTH, HEIGHT, FONT, WHITE, BLACK, GREEN, RED, BLUE

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
        pygame.quit()
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
        if self.game_state == "showing_solution":
            self.screen.blit(FONT.render(f"Solution: {self.correct_sequence}", True, BLUE), (50, 250))
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
                        self.score += len(self.user_sequence) * 10
                        self.level += 1
                        self.current_pair = self.get_new_word_pair()
                        self.user_sequence = ""
                        self.game_state = "playing"
            elif event.key == pygame.K_BACKSPACE:
                self.user_sequence = self.user_sequence[:-1]
            elif event.key == pygame.K_SPACE:
                self.correct_sequence = self.find_lcs(*self.current_pair)
                self.game_state = "showing_solution"
            elif event.unicode.isalpha():
                self.user_sequence += event.unicode.upper()

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