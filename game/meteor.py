import pygame
import random
import math

SPLIT_THRESHOLD = 18

class Meteor:
    def __init__(self, width=700, x=None, y=None, radius=None, vx=None, vy=None, color=None):
        if x is None:
            self.x = random.randint(0, width)
            self.y = -30
            self.radius = random.randint(12, 28)
            angle = random.uniform(70, 110)
            speed = random.uniform(2, 5)
            self.vx = math.cos(math.radians(angle)) * speed
            self.vy = math.sin(math.radians(angle)) * speed
            self.color = (
                random.randint(160, 220),
                random.randint(80, 120),
                random.randint(40, 80)
            )
            self.rot = 0
            self.rot_speed = random.uniform(-3, 3)
        else:
            self.x = x
            self.y = y
            self.radius = radius
            self.vx = vx
            self.vy = vy
            self.color = color if color is not None else (
                random.randint(160, 220),
                random.randint(80, 120),
                random.randint(40, 80)
            )
            self.rot = 0
            self.rot_speed = random.uniform(-5, 5)

    def split(self):
        if self.radius < SPLIT_THRESHOLD:
            return []
        base_angle = math.degrees(math.atan2(self.vy, self.vx))
        speed = max(2.5, math.hypot(self.vx, self.vy) * 1.15)
        child_radius = int(self.radius * 0.6)
        fragments = []
        for offset, rot_dir in [(-30, -1), (30, 1)]:
            rad = math.radians(base_angle + offset)
            vx = math.cos(rad) * speed
            vy = math.sin(rad) * speed
            frag = Meteor(
                x=self.x + offset * 0.2,
                y=self.y,
                radius=child_radius,
                vx=vx,
                vy=vy,
                color=self.color
            )
            frag.rot_speed = rot_dir * random.uniform(3, 5)
            fragments.append(frag)
        return fragments

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot = (self.rot + self.rot_speed) % 360

    def off_screen(self, height):
        return self.y > height + 60 or self.x < -60 or self.x > 760

    def collides(self, rect):
        cx, cy = rect.centerx, rect.centery
        dx, dy = self.x - cx, self.y - cy
        return (dx**2 + dy**2)**0.5 < self.radius + 16

    def draw(self, screen):
        pts = []
        for i in range(7):
            angle = math.radians(self.rot + i * (360 / 7))
            r = self.radius * (0.8 + 0.2 * (i % 2))
            pts.append((int(self.x + r * math.cos(angle)), int(self.y + r * math.sin(angle))))
        pygame.draw.polygon(screen, self.color, pts)
        inner = [(int(self.x + (r * 0.5) * math.cos(math.radians(self.rot + i * (360 / 7)))),
                 int(self.y + (r * 0.5) * math.sin(math.radians(self.rot + i * (360 / 7)))))
                for i, (cx, cy) in enumerate(pts)]
        pygame.draw.polygon(screen, tuple(max(0, c - 40) for c in self.color), inner)
