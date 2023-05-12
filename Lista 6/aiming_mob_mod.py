import pygame, constants, bullets


class AimingMob(pygame.sprite.Sprite):
    def __init__(self):
        super(AimingMob, self).__init__()
        self.image = pygame.image.load("jet.png").convert()
        self.image.set_colorkey(constants.WHITE, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = constants.WIDTH/2
        self.rect.y = 0
        self.speedx = 0
        self.speedy = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000
        self.move_type = 0
