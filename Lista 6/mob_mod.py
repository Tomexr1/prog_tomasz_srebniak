import pygame, constants, bullets, animations
import math


bullets_group = pygame.sprite.Group()


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, move_type=0, shoot_delay=2000, shooting=False, type='down'):
        super(Mob, self).__init__()
        self.type = type
        if self.type == 'down':
            self.image = animations.enemydown_animations[0]
        elif self.type == 'right':
            self.image = animations.enemyright_animations[0]
        elif self.type == 'left':
            self.image = animations.enemyleft_animations[0]
        elif self.type == 'flipper':
            self.image = animations.flipper_animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = speed_x
        self.speedy = speed_y
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = shoot_delay
        self.move_type = move_type
        self.last_anim = pygame.time.get_ticks()
        self.frame = 0
        self.shooting = shooting

    def update(self):
        if self.move_type == 1:
            self.speedy = 2*math.sin(2*math.pi*self.rect.x/(constants.WIDTH))

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.shooting:
            self.shoot()

        self.animate()

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
        # if self.shoot_delay == 0:
        #     if now - self.last_shot > 1000:
        #         self.last_shot = now
        #         bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0, 'mob')
        #         bullets_group.add(bullet)
        #

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0, 'mob')
            bullets_group.add(bullet)

    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim > 100:
            self.last_anim = now
            self.frame += 1
            if self.frame > 6:
                self.frame = 0
            self.frames()

    def frames(self):
        if self.type == 'down':
            if (self.frame % 2) == 0:
                self.image = animations.enemydown_animations[0]
            if (self.frame % 2) == 1:
                self.image = animations.enemydown_animations[1]
        elif self.type == 'right':
            if (self.frame % 2) == 0:
                self.image = animations.enemyright_animations[0]
            if (self.frame % 2) == 1:
                self.image = animations.enemyright_animations[1]
        elif self.type == 'left':
            if (self.frame % 2) == 0:
                self.image = animations.enemyleft_animations[0]
            if (self.frame % 2) == 1:
                self.image = animations.enemyleft_animations[1]
        elif self.type == 'flipper':
            if self.frame == 0:
                self.image = animations.flipper_animations[0]
            if self.frame == 1:
                self.image = animations.flipper_animations[1]
            if self.frame == 2:
                self.image = animations.flipper_animations[2]
            if self.frame == 3:
                self.image = animations.flipper_animations[3]
            if self.frame == 4:
                self.image = animations.flipper_animations[4]
            if self.frame == 5:
                self.image = animations.flipper_animations[5]
            if self.frame == 6:
                self.image = animations.flipper_animations[6]
