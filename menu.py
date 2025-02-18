import pygame
from settings import WIDTH, HEIGHT, FONT, WHITE, BLACK, GREEN

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LCS Game Menu")

class Menu:
    def __init__(self):
        self.menu_items = ["Start Game", "Tutorial", "Quit"]
        self.selected_item = 0
        self.running = True
        self.update_dimensions()

    def update_dimensions(self):
        self.screen_width, self.screen_height = screen.get_size()
        self.font = pygame.font.Font(None, int(self.screen_height * 0.05))
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2.5

    def draw(self):
        screen.fill(BLACK)
        for idx, item in enumerate(self.menu_items):
            color = GREEN if idx == self.selected_item else WHITE
            text = self.font.render(f"{item}", True, color)
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
                    if self.selected_item == 0:
                        return "start"
                    elif self.selected_item == 1:
                        return "scoreboard"
                    elif self.selected_item == 2:
                        return "quit"
        return "none"

def init_menu():
    menu = Menu()
    while menu.running:
        menu.update_dimensions()
        menu.draw()
        action = menu.handle_input()
        if action in ["start", "scoreboard", "quit"]:
            return action
        pygame.time.Clock().tick(30)