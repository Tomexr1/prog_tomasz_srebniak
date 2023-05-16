import pygame, constants, bullets, animations
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.image = pygame.image.load("graphics/plane1.png").convert_alpha()
        self.image = animations.player_animations[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = constants.WIDTH / 2 + 7
        self.rect.bottom = constants.HEIGHT - 60
        self.xvel = 0
        self.yvel = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 300
        self.bullets = pygame.sprite.Group()
        self.frame = 0
        self.last_anim = pygame.time.get_ticks()

    def update(self):
        self.xvel = 0
        self.yvel = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.yvel = -6.5
        if keystate[pygame.K_s]:
            self.yvel = 6.5
        if keystate[pygame.K_a]:
            self.xvel = -8.5
        if keystate[pygame.K_d]:
            self.xvel = 8.5
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.move()
        self.animate()

        if self.rect.right > constants.WIDTH:
            self.rect.right = constants.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > constants.HEIGHT:
            self.rect.bottom = constants.HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, -5, 0)
            self.bullets.add(bullet)

    def move(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim > 100:
            self.last_anim = now
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
            self.frames()

    def frames(self):
        if self.frame == 0:
            self.image = animations.player_animations[0]
        if self.frame == 1:
            self.image = animations.player_animations[1]
        if self.frame == 2:
            self.image = animations.player_animations[2]
        if self.frame == 3:
            self.image = animations.player_animations[3]
