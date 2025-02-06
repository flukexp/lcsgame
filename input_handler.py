import pygame
from lcs import find_lcs

def handle_input(event, game):
    """Handle user input."""
    if event.type == pygame.QUIT:
        game.running = False

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            game.running = False

        elif event.key == pygame.K_RETURN:
            if game.check_user_sequence():
                correct_lcs = find_lcs(*game.current_pair)
                if len(game.user_sequence) == len(correct_lcs):
                    game.score += len(game.user_sequence) * 10
                    game.level += 1
                    game.current_pair = game.get_new_word_pair()
                    game.user_sequence = ""
                    game.game_state = "playing"

        elif event.key == pygame.K_BACKSPACE:
            game.user_sequence = game.user_sequence[:-1]

        elif event.key == pygame.K_SPACE:
            game.correct_sequence = find_lcs(*game.current_pair)
            game.game_state = "showing_solution"

        elif event.unicode.isalpha():
            game.user_sequence += event.unicode.upper()
