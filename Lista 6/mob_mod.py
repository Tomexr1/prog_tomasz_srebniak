import pygame, constants, bullets, animations
import math


bullets_group = pygame.sprite.Group()


class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, speed_y, target_y=1000, move_type=0, shoot_delay=2000, shooting='no', type='down'):
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
        elif self.type == 'kamikazeleft':
            self.image = animations.kamikaze_l_animations[0]
        elif self.type == 'kamikazeright':
            self.image = animations.kamikaze_r_animations[0]
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
        self.burst_ticks = 0
        self.last_burst = pygame.time.get_ticks()
        self.target_y = target_y

    def update(self):
        if self.rect.top < self.target_y:
            if self.move_type == 1:
                self.speedy = 2*math.sin(2*math.pi*self.rect.x/(constants.WIDTH))

            self.rect.x += self.speedx
            self.rect.y += self.speedy

        if self.shooting != 'no':
            if self.shooting == 'tap':
                self.shoot()
            elif self.shooting == 'cone':
                self.shoot_in_cone()
            elif self.shooting == 'burst':
                self.burst()
            elif self.shooting == 'shoot_circle':
                self.shoot_circle()

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
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0, 'mob')
            bullets_group.add(bullet)

    def shoot_in_cone(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0, 'mob')
            bullets_group.add(bullet)
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 1, 10, 0, 'mob')
            bullets_group.add(bullet)
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, -1, 10, 0, 'mob')
            bullets_group.add(bullet)

    def burst(self):
        now = pygame.time.get_ticks()
        if (now - self.last_burst > 50) and (1 <= self.burst_ticks < 5):
            self.last_burst = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0, 'mob')
            bullets_group.add(bullet)
            self.burst_ticks += 1
        elif now - self.last_shot > self.shoot_delay:
            self.burst_ticks = 1
            bullet = bullets.Bullet(self.rect.centerx, self.rect.top, 0, 10, 0, 'mob')
            bullets_group.add(bullet)
            self.last_shot = now

    def shoot_circle(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            for i in range(0, 360, 30):
                bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, 4*math.cos(i), 4*math.sin(i), 0, 'mob')
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
        elif self.type == "kamikazeleft":
            if (self.frame % 2) == 0:
                self.image = animations.kamikaze_l_animations[0]
            if (self.frame % 2) == 1:
                self.image = animations.kamikaze_l_animations[1]
        elif self.type == 'kamikazeright':
            if (self.frame % 2) == 0:
                self.image = animations.kamikaze_r_animations[0]
            if (self.frame % 2) == 1:
                self.image = animations.kamikaze_r_animations[1]
