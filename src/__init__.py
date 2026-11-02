import pygame

from src.config import (
    BACKGROUND_COLOR,
    DIVIDER_COLOR,
    PADDLE_COLORS,
    TEXT_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


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
        elif self.model.state == "color_select":
            self._draw_color_selection()
        else:
            self._draw_game()

        pygame.display.flip()

    def _draw_menu(self):
        title = self.title_font.render("PONG", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH / 2, 120))
        self.screen.blit(title, title_rect)

        single_text = self.font.render("1: 1 Player", True, TEXT_COLOR)
        single_rect = single_text.get_rect(center=(WINDOW_WIDTH / 2, 220))
        self.screen.blit(single_text, single_rect)

        multi_text = self.font.render("2: 2 Players", True, TEXT_COLOR)
        multi_rect = multi_text.get_rect(center=(WINDOW_WIDTH / 2, 300))
        self.screen.blit(multi_text, multi_rect)

        color_text = self.font.render("C: Paddle Colors", True, TEXT_COLOR)
        color_rect = color_text.get_rect(center=(WINDOW_WIDTH / 2, 380))
        self.screen.blit(color_text, color_rect)

        best_text = self.small_font.render(
            f"Best Survival: {self.model.get_best_survival_time():.1f}s",
            True,
            TEXT_COLOR,
        )
        best_rect = best_text.get_rect(center=(WINDOW_WIDTH / 2, 500))
        self.screen.blit(best_text, best_rect)

    def _draw_color_selection(self):
        title = self.title_font.render("PADDLE COLORS", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WINDOW_WIDTH / 2, 80))
        self.screen.blit(title, title_rect)

        color_status = self.model.get_color_status()
        start_y = 180
        for index, color in enumerate(color_status):
            color_name = color["name"]
            text = color_name.title()
            label = f"{index + 1}: {text}"
            if not color["unlocked"]:
                label += f"  (unlock at {color['requirement']:.0f}s)"
            if color["selected"]:
                label += "  [selected]"
            if index == self.model.color_selection_index:
                label = "> " + label

            rendered = self.small_font.render(label, True, TEXT_COLOR)
            rect = rendered.get_rect(center=(WINDOW_WIDTH / 2, start_y + index * 60))
            self.screen.blit(rendered, rect)

            if color["unlocked"]:
                color_box = pygame.Rect(WINDOW_WIDTH / 2 + 180, start_y + index * 60 - 10, 30, 30)
                pygame.draw.rect(self.screen, PADDLE_COLORS[color_name], color_box)

        hint = self.small_font.render("Use arrow keys or WASD to choose, Enter to confirm", True, TEXT_COLOR)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH / 2, 520))
        self.screen.blit(hint, hint_rect)

    def _draw_game(self):
        self._draw_middle_line()
        self._draw_score()
        self.model.left_paddle.draw(self.screen)
        self.model.right_paddle.draw(self.screen)
        self.model.ball.draw(self.screen)

        if self.model.mode == "single":
            mode_text = self.small_font.render("Single Player", True, TEXT_COLOR)
            survival_text = self.small_font.render(f"Survival: {self.model.current_survival_time:.1f}s", True, TEXT_COLOR)
            mode_rect = mode_text.get_rect(center=(WINDOW_WIDTH / 2, 30))
            survival_rect = survival_text.get_rect(center=(WINDOW_WIDTH / 2, 55))
            self.screen.blit(mode_text, mode_rect)
            self.screen.blit(survival_text, survival_rect)
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
