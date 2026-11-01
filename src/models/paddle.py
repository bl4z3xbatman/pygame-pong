import pygame


class Paddle:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.velocity = 0

    def move(self, direction, dt, arena_height):
        self.velocity = direction * self.speed
        next_y = self.y + self.velocity * dt * 60
        max_y = arena_height - self.height
        self.y = max(0, min(next_y, max_y))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.width, self.height))
