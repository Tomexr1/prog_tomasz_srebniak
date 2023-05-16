import pygame

pygame.init()
pygame.display.set_mode()

player_animations = []

for i in range(4):
    name = 'graphics/plane' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    player_animations.append(image)
