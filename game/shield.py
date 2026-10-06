import pygame
import random
import math

class ShieldOrb:
    def __init__(self, width):
        self.x = random.randint(40, width - 40)
        self.y = -20
        self.radius = 12
        self.vy = random.uniform(1.8, 2.5)
        self.vx = random.uniform(-0.5, 0.5)
        self.pulse = random.uniform(0, math.pi * 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.pulse += 0.08

    def off_screen(self, height):
        return self.y > height + 30 or self.x < -40 or self.x > 740

    def collides(self, rect):
        cx, cy = rect.centerx, rect.centery
        dx, dy = self.x - cx, self.y - cy
        return (dx**2 + dy**2)**0.5 < self.radius + 18

    def draw(self, screen):
        glow_r = int(self.radius + 4 + 2 * math.sin(self.pulse))
        glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (0, 220, 255, 60), (glow_r, glow_r), glow_r)
        screen.blit(glow_surf, (int(self.x - glow_r), int(self.y - glow_r)))
        pygame.draw.circle(screen, (0, 200, 255), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (220, 255, 255), (int(self.x - 3), int(self.y - 3)), self.radius // 3)
        pygame.draw.circle(screen, (100, 240, 255), (int(self.x), int(self.y)), self.radius, 2)
