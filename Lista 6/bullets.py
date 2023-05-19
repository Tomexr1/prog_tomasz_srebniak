import pygame, constants, animations
from pygame.locals import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, rotate, kind):
        super(Bullet, self).__init__()
        self.kind = kind
        self.rotate = rotate
        if self.kind == 'player':
            self.image = animations.playerbullet_animations[0]
        elif self.kind == 'mob':
            self.image = animations.enemybullet_animations[0]
        elif self.kind == 'boat':
            self.image = animations.boatmissile_animations[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedx = speedx
        self.speedy = speedy
        self.sound = pygame.mixer.Sound("music/8bit_gunloop_explosion.wav")
        self.sound.play()
        self.sound.set_volume(0.05)
        self.last_anim = pygame.time.get_ticks()
        self.frame = 0
        self.x = x
        self.y = y

    def update(self):
        self.x += self.speedx
        self.y += self.speedy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.animate()

        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > constants.HEIGHT:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > constants.WIDTH:
            self.kill()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim > 50:
            self.last_anim = now
            self.frame += 1
            if self.frame > 4:
                self.frame = 0
            self.frames()

    def frames(self):
        if self.kind == 'player':
            if self.frame == 0:
                self.image = animations.playerbullet_animations[0]
            if self.frame == 1:
                self.image = animations.playerbullet_animations[1]
            if self.frame == 2:
                self.image = animations.playerbullet_animations[2]
            if self.frame == 3:
                self.image = animations.playerbullet_animations[3]
            if self.frame == 4:
                self.image = animations.playerbullet_animations[4]
        elif self.kind == 'mob':
            if (self.frame % 4) == 0:
                self.image = animations.enemybullet_animations[0]
            if (self.frame % 4) == 1:
                self.image = animations.enemybullet_animations[1]
            if (self.frame % 4) == 2:
                self.image = animations.enemybullet_animations[2]
            if (self.frame % 4) == 3:
                self.image = animations.enemybullet_animations[3]
        elif self.kind == 'boat':
            if (self.frame % 2) == 0:
                self.image = animations.boatmissile_animations[0]
                # self.image = pygame.transform.rotate(self.image, self.rotate)
            if (self.frame % 2) == 1:
                self.image = animations.boatmissile_animations[1]
                # self.image = pygame.transform.rotate(self.image, self.rotate)

