import pygame, constants, bullets

boat_missiles_group = pygame.sprite.Group()


class AimingMob(pygame.sprite.Sprite):
    def __init__(self, x, y, y_dest):
        super(AimingMob, self).__init__()
        self.image = pygame.image.load('graphics/boat_turret.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.speedx = 0
        self.speedy = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000
        self.y_dest = y_dest

    def update(self):
        if self.rect.top < self.y_dest:
            self.rect.y += self.speedy

        self.aim()
        self.shoot()
        # self.animate()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0, 'boat')
            boat_missiles_group.add(bullet)

    def aim(self):
        pass
