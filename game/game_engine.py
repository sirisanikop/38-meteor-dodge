import pygame
import random
from game.ship import Ship
from game.meteor import Meteor
from game.laser import Laser
from game.shield import ShieldOrb

WIDTH,HEIGHT=700,520
FPS=60
BG=(8,5,20)

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Meteor Dodge")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("monospace",26,bold=True)
        self.big_font=pygame.font.SysFont("monospace",46,bold=True)
        self.stars=[(random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(1,3)) for _ in range(80)]
        self.reset()

    def reset(self):
        self.ship=Ship(WIDTH//2,HEIGHT-80)
        self.meteors=[]
        self.lasers=[]
        self.shield_orbs=[]
        self.shield_timer=0
        self.shield_spawn_interval=random.randint(450,650)
        self.timer=0
        self.spawn_interval=60
        self.score=0
        self.game_over=False
        self.started=False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: return False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if self.game_over: self.reset()
                    elif not self.started: self.started=True
                    else: self.lasers.append(Laser(self.ship.rect.centerx, self.ship.rect.top))
        return True

    def update(self):
        if self.game_over or not self.started: return
        keys=pygame.key.get_pressed()
        self.ship.move(keys,WIDTH,HEIGHT)
        self.timer+=1
        if self.timer>=self.spawn_interval:
            self.meteors.append(Meteor(WIDTH))
            self.timer=0
            self.spawn_interval=max(20,self.spawn_interval-0.3)
        self.shield_timer+=1
        if self.shield_timer>=self.shield_spawn_interval:
            self.shield_orbs.append(ShieldOrb(WIDTH))
            self.shield_timer=0
            self.shield_spawn_interval=random.randint(480,720)

        for m in self.meteors: m.update()
        for laser in self.lasers: laser.update()
        for orb in self.shield_orbs: orb.update()

        collected_orbs=set()
        for orb in self.shield_orbs:
            if orb.collides(self.ship.rect):
                self.ship.has_shield=True
                collected_orbs.add(orb)
        if collected_orbs:
            self.shield_orbs=[o for o in self.shield_orbs if o not in collected_orbs]
        self.shield_orbs=[o for o in self.shield_orbs if not o.off_screen(HEIGHT)]

        spawned_fragments=[]
        hit_lasers=set()
        hit_meteors=set()
        for laser in self.lasers:
            for m in self.meteors:
                if m not in hit_meteors and laser.collides(m):
                    hit_lasers.add(laser)
                    hit_meteors.add(m)
                    spawned_fragments.extend(m.split())
                    break

        if hit_meteors:
            self.meteors=[m for m in self.meteors if m not in hit_meteors]+spawned_fragments
        self.lasers=[l for l in self.lasers if l not in hit_lasers and not l.off_screen()]

        collided_meteors=set()
        for m in self.meteors:
            if m.collides(self.ship.rect):
                if self.ship.has_shield:
                    self.ship.has_shield=False
                    collided_meteors.add(m)
                else:
                    self.game_over=True
                    break
        if collided_meteors:
            self.meteors=[m for m in self.meteors if m not in collided_meteors]
        self.meteors=[m for m in self.meteors if not m.off_screen(HEIGHT)]
        self.score+=1

    def draw(self):
        self.screen.fill(BG)
        for sx,sy,sr in self.stars:
            pygame.draw.circle(self.screen,(200,200,220),(sx,sy),sr)
        for orb in self.shield_orbs: orb.draw(self.screen)
        for m in self.meteors: m.draw(self.screen)
        for laser in self.lasers: laser.draw(self.screen)
        self.ship.draw(self.screen)
        sc=self.font.render(f"Time: {self.score//60}s",True,(200,200,240))
        self.screen.blit(sc,(10,10))
        if self.ship.has_shield:
            sh_txt=self.font.render("SHIELD: ACTIVE",True,(0,220,255))
            self.screen.blit(sh_txt,(WIDTH-sh_txt.get_width()-10,10))
        if not self.started:
            msg=self.font.render("Press SPACE to launch",True,(180,180,240))
            self.screen.blit(msg,(WIDTH//2-msg.get_width()//2,HEIGHT//2))
        if self.game_over:
            ov=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
            ov.fill((0,0,0,150))
            self.screen.blit(ov,(0,0))
            m=self.big_font.render("DESTROYED!",True,(220,80,60))
            s=self.font.render(f"Survived {self.score//60}s | SPACE to Restart",True,(200,200,200))
            self.screen.blit(m,(WIDTH//2-m.get_width()//2,HEIGHT//2-40))
            self.screen.blit(s,(WIDTH//2-s.get_width()//2,HEIGHT//2+20))
        pygame.display.flip()

    def run(self):
        running=True
        while running:
            running=self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
