import pygame, constants, bullets, animations

bullets_group = pygame.sprite.Group()
player_position = []


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Boss, self).__init__()
        self.image = pygame.image.load("graphics/boss.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (160, 215))   # 641 x 861
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 0
        self.speedy = 0
        self.last_shot = pygame.time.get_ticks()
        self.stage = 0
        # self.shoot_delay = 2000
        # self.move_type = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

