import pygame, asyncio, random, time, os, json, nltk
from collections import defaultdict
from pymongo import MongoClient
from dotenv import load_dotenv

# Initialize Pygame
pygame.init()

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

# Fonts
FONT = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LCS Algorithm Game")

# MongoDB connection
def connect_to_mongo():
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")

    if not MONGO_URI:
        raise ValueError("MONGO_URI is not set in .env")

    client = MongoClient(MONGO_URI)
    db = client["LCS"]
    collection = db["user"]

    test_data = {"name": "Test User", "score": 0}
    insert_result = collection.insert_one(test_data)
    print(f"✅ Inserted ID: {insert_result.inserted_id}")

    found_data = collection.find_one({"name": "Test User"})
    print(f"✅ Found Data: {found_data}")

    client.close() 
    print("✅ MongoDB connection closed.")

# Menu class
class Menu:
    def __init__(self):
        self.menu_items = ["Start Game", "Score Board", "Quit"]
        self.selected_item = 0  # Default selection is the first item
        self.running = True
        self.update_dimensions()

    def update_dimensions(self):
        # Dynamically adjust based on the current screen size
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.Font(None, int(self.screen_height * 0.05))  # Font size proportional to screen height

        # Center position of the menu
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2.5

    def draw(self):
        screen.fill(BLACK)

        # Display menu items, positioning and sizing dynamically
        for idx, item in enumerate(self.menu_items):
            color = GREEN if idx == self.selected_item else WHITE
            text = self.font.render(f"{item}", True, color)

            # Adjust vertical spacing based on screen height
            text_rect = text.get_rect(center=(self.center_x, self.center_y + idx * int(self.screen_height * 0.1)))
            screen.blit(text, text_rect)
        
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    if self.selected_item == 0:  # Start Game
                        return "start"
                    elif self.selected_item == 1:  # Scoreboard
                        return "scoreboard"
                    elif self.selected_item == 2:  # Quit
                        return "quit"
        return "none"

def init_menu():
    menu = Menu()

    while menu.running:
        menu.update_dimensions()  # Update dimensions on window resize
        menu.draw()
        action = menu.handle_input()
        
        if action == "start":
            return "start"  # Start the game
        elif action == "scoreboard":
            return "scoreboard"
        elif action == "quit":
            return "quit" # Exit the game
        
        pygame.time.Clock().tick(30)  # Limit to 30 frames per second

# LCS Game class
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
                action = self.handle_input()
                
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
        
    def handle_input(self):
        """Handle user input."""
        if self.event.type == pygame.QUIT:
            self.running = False

        elif self.event.type == pygame.KEYDOWN:
            if self.event.key == pygame.K_ESCAPE:
                self.running = False
                return "exit_to_menu"

            elif self.event.key == pygame.K_RETURN:
                if self.check_user_sequence():
                    correct_lcs = self.find_lcs(*self.current_pair)
                    if len(self.user_sequence) == len(correct_lcs):
                        self.score += len(self.user_sequence) * 10
                        self.level += 1
                        self.current_pair = self.get_new_word_pair()
                        self.user_sequence = ""
                        self.game_state = "playing"

            elif self.event.key == pygame.K_BACKSPACE:
                self.user_sequence = self.user_sequence[:-1]

            elif self.event.key == pygame.K_SPACE:
                self.correct_sequence = self.find_lcs(*self.current_pair)
                self.game_state = "showing_solution"

            elif self.event.unicode.isalpha():
                self.user_sequence += self.event.unicode.upper()
    
    def find_lcs(self, str1, str2):
        """Find the longest common subsequence (LCS) using Hunter Szymanski's Algorithm."""
        m, n = len(str1), len(str2)

        # Dictionary to store positions of each character in str2
        pos = defaultdict(list)
        for j in range(n):
            pos[str2[j]].append(j)

        lcs = []
        last_j = -1  # Tracks the last position in str2

        for i in range(m):
            if str1[i] in pos:
                # Get positions in str2 where this character appears
                for j in reversed(pos[str1[i]]):  # Process in reverse order for correct sequence
                    if j > last_j:
                        lcs.append(str1[i])
                        last_j = j
                        break  # Move to the next character in str1

        return ''.join(lcs)

    def is_subsequence(self, s, t):
        """Check if s is a subsequence of t."""
        s_idx = 0
        for char in t:
            if s_idx < len(s) and char == s[s_idx]:
                s_idx += 1
        return s_idx == len(s)

# Scoreboard class
class Scoreboard:
    def __init__(self):
        self.scores = self.load_scores()
        self.scroll_offset = 0  # Offset for scrolling

    def load_scores(self):
        try:
            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, 'assets', 'user_score.json')

            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def show(self):
        # Sort scores in descending order
        self.screen_width, self.screen_height = screen.get_size()
        
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        
        sorted_scores = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)

        font = pygame.font.Font(None, int(self.screen_height * 0.05))
        scroll_speed = int(self.screen_height * 0.1)  # Adjust scrolling speed
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_DOWN:  # Scroll down
                        self.scroll_offset += scroll_speed
                    elif event.key == pygame.K_UP:  # Scroll up
                        self.scroll_offset -= scroll_speed

            # Limit scroll offset to valid range (don't scroll beyond first or last score)
            max_scroll = max(0, len(sorted_scores) * int(self.screen_height * 0.1) - self.screen_height + int(self.screen_height * 0.05))  # Extra space for title
            if self.scroll_offset > max_scroll:
                self.scroll_offset = max_scroll
            if self.scroll_offset < 0:
                self.scroll_offset = 0

            # Fill the screen with black
            screen.fill(BLACK)

            # Title
            title_text = font.render("Scoreboard", True, GREEN)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 10))
            screen.blit(title_text, title_rect)

            # Display scores with scrolling offset
            y_offset = self.screen_height // 5 - self.scroll_offset
            max_displayable_scores = (self.screen_height - int(self.screen_height * 0.2)) // int(self.screen_height * 0.1)  # Max number of scores that can fit
            for idx, (player, score) in enumerate(sorted_scores[:max_displayable_scores]):
                score_text = font.render(f"{player}: {score}", True, WHITE)
                score_rect = score_text.get_rect(center=(self.screen_width // 2, y_offset + idx * int(self.screen_height * 0.1)))
                screen.blit(score_text, score_rect)

            pygame.display.flip()
            pygame.time.Clock().tick(30)  # Limit to 30 frames per second

# Main function
async def main():
    while True:
        action = init_menu()
        await asyncio.sleep(0)
        if action == "start":
            # Run the game
            game = LCSGame()  # Create the game instance
            result = game.run()  # Start the game
            if result == "exit_to_menu":
                continue  # Return to the main menu
            
        elif action == "scoreboard":
            # Show the scoreboard
            scoreboard = Scoreboard()
            scoreboard.show()
        else:
            pygame.quit()  # Quit Pygame if user chooses to quit
            break    

asyncio.run(main())