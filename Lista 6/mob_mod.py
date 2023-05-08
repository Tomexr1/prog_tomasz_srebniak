import pygame, constants, bullets


bullets_group = pygame.sprite.Group()


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, dest_x, dest_y):
        super(Mob, self).__init__()
        self.image = pygame.image.load("jet.png").convert()
        self.image.set_colorkey(constants.WHITE, pygame.RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000
        # self.bullets = pygame.sprite.Group()

    def update(self):
        # if self.rect.centerx < self.dest_x:
        #     self.rect.centerx += self.speed
        # if self.rect.centerx > self.dest_x:
        #     self.rect.centerx -= self.speed
        # if self.rect.centery < self.dest_y:
        #     self.rect.centery += self.speed
        # if self.rect.centery > self.dest_y:
        #     self.rect.centery -= self.speed

        self.shoot()

        # if self.rect.bottom < 0:
        #     self.kill()
        # if self.rect.top > constants.HEIGHT:
        #     self.kill()
        # if self.rect.right < 0:
        #     self.kill()
        # if self.rect.left > constants.WIDTH:
        #     self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0)
            # self.bullets.add(bullet)
            bullets_group.add(bullet)
