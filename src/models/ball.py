import random


class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.vx = random.choice([-1, 1])
        self.vy = random.uniform(-1.0, 1.0)

    def update(self, dt, arena_width, arena_height):
        self.x += self.vx * self.speed * dt * 60
        self.y += self.vy * self.speed * dt * 60

        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy *= -1
        elif self.y + self.radius >= arena_height:
            self.y = arena_height - self.radius
            self.vy *= -1

        if self.x - self.radius <= 0 or self.x + self.radius >= arena_width:
            return True
        return False

    def on_paddle_hit(self, paddle):
        relative_intersect = (paddle.y + (paddle.height / 2)) - self.y
        normalized_intersect = relative_intersect / (paddle.height / 2)
        self.vy = normalized_intersect * 4.5
        self.speed = min(self.speed + 0.25, 12)

        if self.x < paddle.x:
            self.vx = abs(self.vx)
        else:
            self.vx = -abs(self.vx)

    def draw(self, surface):
        pygame = __import__("pygame")
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
