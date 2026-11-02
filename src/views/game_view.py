import pygame

from src.config import FRAME_RATE, WINDOW_HEIGHT, WINDOW_WIDTH
from src.models.game_model import GameModel, PaddleProgress
from src.views.game_view import GameView


class GameController:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")

        self.progress = PaddleProgress()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.model = GameModel(self.progress)
        self.view = GameView(self.screen, self.model)
        self.clock = pygame.time.Clock()
        self.running = True

    def _handle_menu_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_1]:
            self.model.set_mode("single")
        elif keys[pygame.K_2]:
            self.model.set_mode("multi")
        elif keys[pygame.K_c]:
            self.model.state = "color_select"
            self.model.color_selection_index = self.model.color_choices.index(self.model.selected_color)

    def _handle_color_selection_input(self):
        keys = pygame.key.get_pressed()
        color_names = self.model.color_choices

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.model.color_selection_index = (self.model.color_selection_index - 1) % len(color_names)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.model.color_selection_index = (self.model.color_selection_index + 1) % len(color_names)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.model.color_selection_index = (self.model.color_selection_index - 1) % len(color_names)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.model.color_selection_index = (self.model.color_selection_index + 1) % len(color_names)

        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            color_name = color_names[self.model.color_selection_index]
            if color_name in self.model.get_unlocked_colors():
                self.model.set_selected_color(color_name)
                self.model.state = "menu"
            return

        if keys[pygame.K_ESCAPE]:
            self.model.state = "menu"

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
            elif self.model.state == "color_select":
                self._handle_color_selection_input()
            else:
                left_input, right_input = self._handle_game_input()
                self.model.update(dt, left_input, right_input)

            self.view.render()

        pygame.quit()
