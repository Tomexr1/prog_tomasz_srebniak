import pygame, constants, bullets
import math


bullets_group = pygame.sprite.Group()


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, move_type=0, shoot_delay=2000):
        super(Mob, self).__init__()
        self.image = pygame.image.load("jet.png").convert()
        self.image.set_colorkey(constants.WHITE, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = speed_x
        self.speedy = speed_y
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = shoot_delay
        self.move_type = move_type

    def update(self):
        if self.move_type == 1:
            self.speedy = 2*math.sin(2*math.pi*self.rect.x/(constants.WIDTH))

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        self.shoot()

        if self.rect.bottom + 100 < 0:
            self.kill()
        if self.rect.top - 100 > constants.HEIGHT:
            self.kill()
        if self.rect.right + 100 < 0:
            self.kill()
        if self.rect.left - 100 > constants.WIDTH:
            self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0)
            bullets_group.add(bullet)
