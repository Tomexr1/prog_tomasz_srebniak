import pygame, constants, bullets, animations
from pygame.locals import *


smoke_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
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
        self.smoke = False
        self.smoke_timer = pygame.time.get_ticks()
        self.invulnerable = True
        self.invulnerable_timer = pygame.time.get_ticks()

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

        if keystate[pygame.K_w] or keystate[pygame.K_a] or keystate[pygame.K_s] or keystate[pygame.K_d]:
            self.leave_smoke()

        self.invulnerable_check()
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
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, -5, 0, 'player')
            self.bullets.add(bullet)

    def move(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim > 100:
            self.last_anim = now
            self.frame += 1
            if self.frame > 7:
                self.frame = 0
            self.frames()

    def frames(self):
        if not self.invulnerable:
            if (self.frame % 4) == 0:
                self.image = animations.player_animations[0]
            if (self.frame % 4) == 1:
                self.image = animations.player_animations[1]
            if (self.frame % 4) == 2:
                self.image = animations.player_animations[2]
            if (self.frame % 4) == 3:
                self.image = animations.player_animations[3]
        else:
            if self.frame == 0:
                self.image = animations.player_animations[0]
            if self.frame == 1:
                self.image = animations.blank_image
            if self.frame == 2:
                self.image = animations.player_animations[1]
            if self.frame == 3:
                self.image = animations.blank_image
            if self.frame == 4:
                self.image = animations.player_animations[2]
            if self.frame == 5:
                self.image = animations.blank_image
            if self.frame == 6:
                self.image = animations.player_animations[3]
            if self.frame == 7:
                self.image = animations.blank_image

    def leave_smoke(self):
        if self.smoke:
            now = pygame.time.get_ticks()
            if now - self.smoke_timer > 100:
                self.smoke_timer = now
                smoke = Smoke((self.rect.centerx, self.rect.bottom), 50)
                smoke_group.add(smoke)

    def invulnerable_check(self):
        now = pygame.time.get_ticks()
        if now - self.invulnerable_timer > 1500:
            self.invulnerable = False


class Smoke(pygame.sprite.Sprite):
    def __init__(self, centre, size):
        super(Smoke, self).__init__()
        self.size = size
        self.image = animations.smoke_animations[0]
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = centre
        self.frame = 0
        self.last_anim = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim > 100:
            self.last_anim = now
            self.frame += 1
            if self.frame == len(animations.smoke_animations):
                self.kill()
            else:
                center = self.rect.center
                self.image = animations.smoke_animations[self.frame]
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
                self.rect = self.image.get_rect()
                self.rect.center = center
