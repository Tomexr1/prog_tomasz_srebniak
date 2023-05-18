import pygame
import animations


class Explosion(pygame.sprite.Sprite):
    def __init__(self, centre, size):
        super(Explosion, self).__init__()
        self.size = size
        self.image = animations.explosion_animations[0]
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = centre
        self.frame = 0
        self.last_anim = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim > 20:
            self.last_anim = now
            self.frame += 1
            if self.frame == len(animations.explosion_animations):
                self.kill()
            else:
                center = self.rect.center
                self.image = animations.explosion_animations[self.frame]
                self.image = pygame.transform.scale(self.image, (self.size, self.size))
                self.rect = self.image.get_rect()
                self.rect.center = center
