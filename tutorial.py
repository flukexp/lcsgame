import pygame
import math
from settings import WIDTH, HEIGHT, WHITE, BLACK, GREEN, DARK_GREEN, GRAY

screen = pygame.display.set_mode((WIDTH, HEIGHT))
BG_IMAGE_PATH = "assets/sun.png"

class Tutorial:
    def __init__(self):
        self.screen_width, self.screen_height = screen.get_size()
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        self.scroll_offset = 0
        
        # Improved fonts with better sizing
        self.title_font = pygame.font.Font(None, int(self.screen_height * 0.08))
        self.font = pygame.font.Font("assets/fontvit.otf", int(self.screen_height * 0.05))
        self.small_font = pygame.font.Font(None, int(self.screen_height * 0.03))
        
        # Simple examples that kids can relate to
        self.sequences = [
            {'seq1': 'BANANA', 'seq2': 'APPLE'},
            {'seq1': 'KITTEN', 'seq2': 'SITTING'},
            {'seq1': 'DRAGON', 'seq2': 'GARDEN'}
        ]
        self.current_example = 0
        self.matrix = self.calculate_lcs_matrix(
            self.sequences[self.current_example]['seq1'],
            self.sequences[self.current_example]['seq2']
        )
        self.lcs_result = self.get_lcs(
            self.sequences[self.current_example]['seq1'],
            self.sequences[self.current_example]['seq2'],
            self.matrix
        )
        
        # Animation variables
        self.animation_counter = 0
        self.animation_speed = 2

        # load BG
        self.bg_image = pygame.image.load(BG_IMAGE_PATH)
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        
        
    def draw_rounded_rect(self, surface, rect, color, radius=20):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def calculate_lcs_matrix(self, seq1, seq2):
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp
    
    def get_lcs(self, seq1, seq2, matrix):
        m, n = len(seq1), len(seq2)
        i, j = m, n
        lcs = []
        
        while i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                lcs.append(seq1[i-1])
                i -= 1
                j -= 1
            elif matrix[i-1][j] > matrix[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs))
    
    def draw_explanation(self):
        # Animated title with pulsing effect
        pulse = abs(math.sin(self.animation_counter / 30)) * 10
        title_size = int(self.screen_height * 0.08 + pulse)
        title_font = pygame.font.Font("assets/fontvit.otf", title_size)
        title_text = title_font.render("Tutorial LCS Game!", True, BLACK)
        title_rect = title_text.get_rect(center=(self.center_x, self.screen_height // 10))
        screen.blit(title_text, title_rect)
        
        # Example card background
        card_rect = pygame.Rect(
            self.center_x - 300,
            self.screen_height // 4 - 50,
            600,
            300
        )
        self.draw_rounded_rect(screen, card_rect, GRAY)
        
        # Current example with friendly explanation
        seq1 = self.sequences[self.current_example]['seq1']
        seq2 = self.sequences[self.current_example]['seq2']
        
        # Game number with background
        number_rect = pygame.Rect(
            card_rect.left + 20,
            card_rect.top + 20,
            200,
            40
        )
        self.draw_rounded_rect(screen, number_rect, DARK_GREEN)
        example_text = self.font.render(f"Game #{self.current_example + 1}", True, WHITE)
        example_rect = example_text.get_rect(center=number_rect.center)
        screen.blit(example_text, example_rect)
        
        # Words with highlighting
        y_offset = card_rect.top + 100
        for idx, (label, word) in enumerate([("Word 1:", seq1), ("Word 2:", seq2)]):
            label_text = self.font.render(label, True, WHITE)
            word_text = self.font.render(word, True, GREEN)
            screen.blit(label_text, (card_rect.left + 50, y_offset + idx * 60))
            screen.blit(word_text, (card_rect.left + 250, y_offset + idx * 60))
        
        # Result in highlighted box
        result_rect = pygame.Rect(
            card_rect.left + 50,
            y_offset + 120,
            500,
            60
        )
        self.draw_rounded_rect(screen, result_rect, DARK_GREEN)
        result_text = self.font.render(f"Matching letters: {self.lcs_result}", True, WHITE)
        result_rect = result_text.get_rect(center=(result_rect.centerx, result_rect.centery))
        screen.blit(result_text, result_rect)
        
        # Draw kid-friendly explanation in a scrollable card
        explanation_card = pygame.Rect(
            self.center_x - 300,
            self.screen_height // 2 + 100,
            600,
            200
        )
        self.draw_rounded_rect(screen, explanation_card, GRAY)
        
        explanations = [
            "This game finds the letters that appear in the same order",
            "in both words, even if they're not next to each other!",
            "",
            "For example, in BANANA and APPLE:",
            "• A appears in both",
            "• N doesn't match anything in APPLE",
            "• A matches again",
            "",
            "How it works:",
            "1. We look at each letter in both words",
            "2. When letters match, we add them to our result",
            "3. If they don't match, we skip to the next letter",
            "4. The longest match wins!"
        ]
        
        # Create a clipping rectangle for scrolling
        pygame.draw.rect(screen, BLACK, (
            explanation_card.left,
            explanation_card.top - 2,
            explanation_card.width,
            2
        ))
        pygame.draw.rect(screen, BLACK, (
            explanation_card.left,
            explanation_card.bottom,
            explanation_card.width,
            2
        ))
        
        y_offset = explanation_card.top + 20 - self.scroll_offset
        for i, line in enumerate(explanations):
            text = self.small_font.render(line, True, WHITE)
            rect = text.get_rect(left=explanation_card.left + 30, top=y_offset + i * 25)
            if explanation_card.top <= rect.top <= explanation_card.bottom - 30:
                screen.blit(text, rect)
    
    def draw_controls(self):
        # Draw controls in a bottom bar
        control_rect = pygame.Rect(0, self.screen_height - 60, self.screen_width, 60)
        self.draw_rounded_rect(screen, control_rect, DARK_GREEN)
        
        controls = [
            "UP/DOWN arrows: Scroll",
            "LEFT/RIGHT arrows: Change Words",
            "ESC: Exit"
        ]
        
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            x_pos = self.screen_width // 4 * (i + 1) - text.get_width() // 2
            screen.blit(text, (x_pos, self.screen_height - 37))
    
    def show(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.animation_counter += self.animation_speed
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_DOWN:
                        self.scroll_offset += 20
                    elif event.key == pygame.K_UP:
                        self.scroll_offset -= 20
                    elif event.key == pygame.K_RIGHT:
                        self.current_example = (self.current_example + 1) % len(self.sequences)
                        self.matrix = self.calculate_lcs_matrix(
                            self.sequences[self.current_example]['seq1'],
                            self.sequences[self.current_example]['seq2']
                        )
                        self.lcs_result = self.get_lcs(
                            self.sequences[self.current_example]['seq1'],
                            self.sequences[self.current_example]['seq2'],
                            self.matrix
                        )
                    elif event.key == pygame.K_LEFT:
                        self.current_example = (self.current_example - 1) % len(self.sequences)
                        self.matrix = self.calculate_lcs_matrix(
                            self.sequences[self.current_example]['seq1'],
                            self.sequences[self.current_example]['seq2']
                        )
                        self.lcs_result = self.get_lcs(
                            self.sequences[self.current_example]['seq1'],
                            self.sequences[self.current_example]['seq2'],
                            self.matrix
                        )
            
            # Adjust scroll bounds
            max_scroll = 13 * 25 - 150  # Approximate max scroll
            self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
            
            # screen.fill(BLACK)
            screen.blit(self.bg_image, (0, 0))
            self.draw_explanation()
            self.draw_controls()
            pygame.display.flip()
            clock.tick(60)