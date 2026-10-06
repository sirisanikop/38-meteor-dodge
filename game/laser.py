import pygame

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 9
        self.radius = 3

    def update(self):
        self.y -= self.speed

    def off_screen(self):
        return self.y < -15

    def collides(self, meteor):
        dx = self.x - meteor.x
        dy = self.y - meteor.y
        return (dx**2 + dy**2)**0.5 < self.radius + meteor.radius

    def draw(self, screen):
        pygame.draw.line(screen, (255, 70, 70), (self.x, self.y - 8), (self.x, self.y + 8), 3)
        pygame.draw.circle(screen, (255, 220, 220), (int(self.x), int(self.y - 8)), 2)
