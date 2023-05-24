import pygame, constants, bullets, animations
import math

boat_missiles_group = pygame.sprite.Group()
player_position = []


class BoatBody(pygame.sprite.Sprite):
    def __init__(self, x, y, target_y):
        super(BoatBody, self).__init__()
        self.image = pygame.image.load('graphics/boat_body1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 2
        self.last_shot = pygame.time.get_ticks()
        self.target_y = target_y
        self.last_anim = pygame.time.get_ticks()
        self.frame = 0

    def update(self):
        if self.rect.top < self.target_y:
            self.rect.y += self.speedy
        self.animate()

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim > 100:
            self.last_anim = now
            self.frame += 1
            if self.frame > 2:
                self.frame = 0
            self.frames()

    def frames(self):
        if self.frame == 0:
            self.image = animations.boat_animations[0]
        elif self.frame == 1:
            self.image = animations.boat_animations[1]
        elif self.frame == 2:
            self.image = animations.boat_animations[2]


class Boat(pygame.sprite.Sprite):
    def __init__(self, x, y, target_y):
        super(Boat, self).__init__()
        self.x = x
        self.y = y
        self.image = animations.boat_turret_animations[130]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # self.speedx = 0
        self.speedy = 2
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.target_y = target_y
        self.last_rotation = pygame.time.get_ticks()
        self.rotation = 0
        self.aim_x = 0
        self.aim_y = 0
        self.angle = 0

    def update(self):
        if self.rect.top < self.target_y:
            self.rect.y += self.speedy

        self.aim()
        self.shoot()
        self.rotate()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, self.aim_x*7, self.aim_y*7, 0, 'mob')
            boat_missiles_group.add(bullet)

    def aim(self):
        delta_x = player_position[0] - self.rect.centerx
        delta_y = player_position[1] - self.rect.centery
        self.angle = math.atan2(delta_y, delta_x)
        self.aim_x = math.cos(self.angle)
        self.aim_y = math.sin(self.angle)

    def rotate(self):
        if self.rect.top >= self.target_y:
            self.image = animations.boat_turret_animations[int(-self.angle*180/math.pi/2)]
            self.rect = self.image.get_rect(center=self.rect.center)
