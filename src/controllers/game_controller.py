import pygame

from src.config import FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from src.models.game_model import GameModel
from src.views.game_view import GameView


class GameController:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.model = GameModel()
        self.view = GameView(self.screen, self.model)
        self.clock = pygame.time.Clock()
        self.running = True

    def _handle_menu_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.model.set_mode("single")
        elif keys[pygame.K_2]:
            self.model.set_mode("multi")

    def _handle_game_input(self):
        keys = pygame.key.get_pressed()
        left_input = 0
        right_input = 0

        if keys[pygame.K_w]:
            left_input -= 1
        if keys[pygame.K_s]:
            left_input += 1

        if self.model.mode == "multi":
            if keys[pygame.K_UP]:
                right_input -= 1
            if keys[pygame.K_DOWN]:
                right_input += 1

        return left_input, right_input

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAME_RATE) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.model.state == "playing":
                        self.model.return_to_menu()

            if self.model.state == "menu":
                self._handle_menu_input()
            else:
                left_input, right_input = self._handle_game_input()
                self.model.update(dt, left_input, right_input)

            self.view.render()

        pygame.quit()
