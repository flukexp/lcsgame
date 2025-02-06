import pygame
from settings import FONT, WHITE, BLACK, GREEN, RED, BLUE

def draw_screen(screen, word_pair, user_sequence, score, level, time_remaining, game_state, correct_sequence):
    """Render the game screen."""
    screen.fill(BLACK)

    word1, word2 = word_pair
    screen.blit(FONT.render(f"Word 1: {word1}", True, WHITE), (50, 50))
    screen.blit(FONT.render(f"Word 2: {word2}", True, WHITE), (50, 100))

    sequence_color = GREEN if game_state == "playing" else RED
    screen.blit(FONT.render(f"Your sequence: {user_sequence}", True, sequence_color), (50, 200))

    screen.blit(FONT.render(f"Score: {score}", True, WHITE), (50, 300))
    screen.blit(FONT.render(f"Level: {level}", True, WHITE), (50, 350))
    screen.blit(FONT.render(f"Time: {int(time_remaining)}s", True, WHITE), (50, 400))

    instructions = [
        "Instructions:",
        "- Type letters to build a common subsequence",
        "- Press ENTER to submit",
        "- Press BACKSPACE to delete",
        "- Press SPACE to see solution",
        "- Press ESC to quit",
    ]

    for i, instruction in enumerate(instructions):
        screen.blit(FONT.render(instruction, True, WHITE), (50, 500 + i * 40))

    if game_state == "showing_solution":
        screen.blit(FONT.render(f"Solution: {correct_sequence}", True, BLUE), (50, 250))

    pygame.display.flip()
