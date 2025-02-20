import asyncio
import pygame
import os
from menu import init_menu
from lcs import LCSGame
from tutorial import Tutorial

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")

async def main():
    """Main function to run the game."""
    while True:
        action = init_menu()
        
        # Set the window icon
        icon = pygame.image.load(LOGO_PATH)  # Replace with your icon file path
        pygame.display.set_icon(icon)
        
        await asyncio.sleep(0)
        if action == "start":
            game = LCSGame()
            result = game.run()
            if result == "exit_to_menu":
                continue
        elif action == "tutorial":
            tutorial = Tutorial()
            tutorial.show()
        else:
            pygame.quit()
            break

if __name__ == "__main__":
    asyncio.run(main())