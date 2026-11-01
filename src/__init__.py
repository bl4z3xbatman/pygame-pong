import pygame

from src.config import BACKGROUND_COLOR, DIVIDER_COLOR, MENU_OPTIONS, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


class GameView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        self.title_font = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 28)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)

        if self.model.state == "menu":
            self._draw_menu()
        else:
            self._draw_game()

        pygame.display.flip()

    def _draw_menu(self):
        title = self.title_font.render("PONG", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH / 2, 120))
        self.screen.blit(title, title_rect)

        for index, (key, label) in enumerate(MENU_OPTIONS.items()):
            menu_text = self.font.render(f"{key.upper()}: {label}", True, TEXT_COLOR)
            menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH / 2, 220 + index * 90))
            self.screen.blit(menu_text, menu_rect)

        hint = self.small_font.render("Press 1 or 2 to start", True, TEXT_COLOR)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH / 2, 500))
        self.screen.blit(hint, hint_rect)

    def _draw_game(self):
        self._draw_middle_line()
        self._draw_score()
        self.model.left_paddle.draw(self.screen)
        self.model.right_paddle.draw(self.screen)
        self.model.ball.draw(self.screen)

        if self.model.mode == "single":
            mode_text = self.small_font.render("Single Player", True, TEXT_COLOR)
        else:
            mode_text = self.small_font.render("Two Players", True, TEXT_COLOR)
        mode_rect = mode_text.get_rect(center=(WINDOW_WIDTH / 2, 30))
        self.screen.blit(mode_text, mode_rect)

    def _draw_middle_line(self):
        center_x = WINDOW_WIDTH / 2
        for y in range(0, WINDOW_HEIGHT, 30):
            pygame.draw.rect(self.screen, DIVIDER_COLOR, (center_x - 2, y, 4, 20))

    def _draw_score(self):
        left_score = self.font.render(str(self.model.left_score), True, TEXT_COLOR)
        right_score = self.font.render(str(self.model.right_score), True, TEXT_COLOR)
        left_rect = left_score.get_rect(center=(WINDOW_WIDTH / 2 - 80, 70))
        right_rect = right_score.get_rect(center=(WINDOW_WIDTH / 2 + 80, 70))
        self.screen.blit(left_score, left_rect)
        self.screen.blit(right_score, right_rect)
