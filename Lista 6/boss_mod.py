import pygame, constants, bullets
import math

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
        self.speedx = 1
        self.speedy = 1
        self.last_shot = pygame.time.get_ticks()
        self.stage = 0
        self.shoot_delay = 2000
        self.aim_x = 0
        self.aim_y = 0
        self.angle = 0
        self.burst_ticks = 0
        self.last_burst = pygame.time.get_ticks()
        self.stage_timer = pygame.time.get_ticks()

    def update(self):
        if self.stage == 2:
            now = pygame.time.get_ticks()
            if now - self.stage_timer > 10000:
                self.stage = 3

        self.move()

        if self.stage == 0:
            self.burst()
        elif self.stage == 1 or self.stage == 4:
            self.shoot_in_cone()
        elif self.stage == 2:
            self.shoot_aimed_rocket()
        elif self.stage == 3:
            self.shoot_circle()
        elif self.stage == 5:
            self.aimed_burst()

    def move(self):
        if self.stage == 0:
            self.rect.y += self.speedy
            if self.rect.top > 60:
                self.stage = 1
        elif self.stage == 1:
            self.rect.x += self.speedx
            if self.rect.right > constants.WIDTH - 60:
                self.speedx = -self.speedx
            elif self.rect.left < 60:
                self.stage = 2
                self.speedx = -self.speedx
                self.stage_timer = pygame.time.get_ticks()
        elif self.stage == 3:
            self.rect.x += self.speedx
            if self.rect.right > constants.WIDTH - 60:
                self.speedx = -self.speedx
                self.stage = 4
        elif self.stage == 4:
            self.rect.x += self.speedx
            if self.rect.centerx < 400:
                self.stage = 5

    def burst(self):
        now = pygame.time.get_ticks()
        if (now - self.last_burst > 50) and (1 <= self.burst_ticks < 5):
            self.last_burst = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, 0, 10, 0, 'mob')
            bullets_group.add(bullet)
            self.burst_ticks += 1
        elif now - self.last_shot > self.shoot_delay:
            self.burst_ticks = 1
            bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, 0, 10, 0, 'mob')
            bullets_group.add(bullet)
            self.last_shot = now

    def shoot_in_cone(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, 0, 6, 0, 'mob')
            bullets_group.add(bullet)
            bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, 5, 6, 0, 'mob')
            bullets_group.add(bullet)
            bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, -5, 6, 0, 'mob')
            bullets_group.add(bullet)

    def shoot_aimed_rocket(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.aim()
            bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, self.aim_x * 3, self.aim_y * 3, 0, 'rocket',
                                    player_position)
            bullets_group.add(bullet)
            sound = pygame.mixer.Sound("music/rocket_launch.wav")
            sound.play()
            sound.set_volume(0.5)

    def aim(self):
        delta_x = player_position[0] - self.rect.centerx
        delta_y = player_position[1] - self.rect.bottom
        self.angle = math.atan2(delta_y, delta_x)
        self.aim_x = math.cos(self.angle)
        self.aim_y = math.sin(self.angle)

    def shoot_circle(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            for i in range(0, 360, 30):
                bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, 2*math.cos(i), 2*math.sin(i), 0, 'mob')
                bullets_group.add(bullet)

    def aimed_burst(self):
        now = pygame.time.get_ticks()
        self.aim()
        if (now - self.last_burst > 50) and (1 <= self.burst_ticks < 5):
            self.last_burst = now
            bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, self.aim_x * 8, self.aim_y * 6, 0, 'mob')
            bullets_group.add(bullet)
            self.burst_ticks += 1
        elif now - self.last_shot > self.shoot_delay:
            self.burst_ticks = 1
            bullet = bullets.Bullet(self.rect.centerx, self.rect.bottom, self.aim_x * 8, self.aim_y * 6, 0, 'mob')
            bullets_group.add(bullet)
            self.last_shot = now
