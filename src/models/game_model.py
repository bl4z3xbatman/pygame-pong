from src.config import (
    BALL_RADIUS,
    BALL_START_SPEED,
    PADDLE_HEIGHT,
    PADDLE_MARGIN,
    PADDLE_SPEED,
    PADDLE_WIDTH,
    PLAYER_ONE_COLOR,
    PLAYER_TWO_COLOR,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.models.ball import Ball
from src.models.paddle import Paddle


class GameModel:
    def __init__(self):
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.mode = "single"
        self.state = "menu"
        self.left_score = 0
        self.right_score = 0

        self.left_paddle = Paddle(
            PADDLE_MARGIN,
            self.height / 2 - PADDLE_HEIGHT / 2,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_SPEED,
            PLAYER_ONE_COLOR,
        )
        self.right_paddle = Paddle(
            self.width - PADDLE_MARGIN - PADDLE_WIDTH,
            self.height / 2 - PADDLE_HEIGHT / 2,
            PADDLE_WIDTH,
            PADDLE_HEIGHT,
            PADDLE_SPEED,
            PLAYER_TWO_COLOR,
        )
        self.ball = Ball(
            self.width / 2,
            self.height / 2,
            BALL_RADIUS,
            (255, 255, 255),
            BALL_START_SPEED,
        )

    def set_mode(self, mode):
        self.mode = mode
        self.state = "playing"
        self.reset_positions()

    def reset_positions(self):
        self.left_paddle.y = self.height / 2 - self.left_paddle.height / 2
        self.right_paddle.y = self.height / 2 - self.right_paddle.height / 2
        self.ball.x = self.width / 2
        self.ball.y = self.height / 2
        self.ball.speed = BALL_START_SPEED
        self.ball.vx = 1 if self.mode == "single" else -1
        self.ball.vy = 0.6

    def reset_ball(self, direction):
        self.ball.x = self.width / 2
        self.ball.y = self.height / 2
        self.ball.speed = BALL_START_SPEED
        self.ball.vx = direction
        self.ball.vy = 0.8

    def update(self, dt, left_input, right_input):
        self.left_paddle.move(left_input, dt, self.height)

        if self.mode == "single":
            right_input = self._cpu_direction()
        self.right_paddle.move(right_input, dt, self.height)

        scored = self.ball.update(dt, self.width, self.height)
        if scored:
            if self.ball.x < self.width / 2:
                self.right_score += 1
                self.reset_ball(1)
            else:
                self.left_score += 1
                self.reset_ball(-1)

        if self._check_paddle_collision(self.left_paddle, self.ball):
            self.ball.on_paddle_hit(self.left_paddle)
            self.ball.x = self.left_paddle.x + self.left_paddle.width + self.ball.radius

        if self._check_paddle_collision(self.right_paddle, self.ball):
            self.ball.on_paddle_hit(self.right_paddle)
            self.ball.x = self.right_paddle.x - self.ball.radius

    def _check_paddle_collision(self, paddle, ball):
        return (
            ball.x - ball.radius <= paddle.x + paddle.width
            and ball.x + ball.radius >= paddle.x
            and ball.y - ball.radius <= paddle.y + paddle.height
            and ball.y + ball.radius >= paddle.y
        )

    def _cpu_direction(self):
        paddle_center = self.right_paddle.y + self.right_paddle.height / 2
        ball_center = self.ball.y
        difference = ball_center - paddle_center

        if abs(difference) < 12:
            return 0
        return 1 if difference > 0 else -1

    def return_to_menu(self):
        self.state = "menu"
        self.left_score = 0
        self.right_score = 0
        self.reset_positions()
