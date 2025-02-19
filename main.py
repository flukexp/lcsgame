import asyncio
import pygame
from menu import init_menu
from lcs import LCSGame
from tutorial import Tutorial

async def main():
    """Main function to run the game."""
    while True:
        action = init_menu()
        
        # Set the window icon
        icon = pygame.image.load('assets/logo.png')  # Replace with your icon file path
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