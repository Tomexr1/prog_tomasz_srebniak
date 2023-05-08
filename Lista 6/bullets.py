import pygame, constants
from pygame.locals import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy, rotate):
        super(Bullet, self).__init__()
        self.bullet_img = pygame.image.load("jet.png").convert()
        self.image = pygame.transform.scale(self.bullet_img, (7, 19))
        self.image = pygame.transform.rotate(self.image, rotate)
        self.image.set_colorkey(constants.WHITE, RLEACCEL)
        # self.surf = pygame.Surface((8,4))
        # self.surf.fill(constants.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > constants.HEIGHT:
            self.kill()
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > constants.WIDTH:
            self.kill()