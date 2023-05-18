import pygame

pygame.init()
pygame.display.set_mode()

player_animations = []
explosion_animations = []
enemybullet_animations = []
playerbullet_animations = []
enemydown_animations = []
enemyright_animations = []
enemyleft_animations = []
boatmissile_animations = []
flipper_animations = []

for i in range(4):
    name = 'graphics/plane' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    player_animations.append(image)

for i in range(16):
    name = 'graphics/expl' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    explosion_animations.append(image)

for i in range(4):
    name = 'graphics/enemyshot' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    image = pygame.transform.scale(image, (10, 10))
    enemybullet_animations.append(image)

for i in range(5):
    name = 'graphics/playershot' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    playerbullet_animations.append(image)

for i in range(2):
    name = 'graphics/enemy' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    image = pygame.transform.rotate(image, -90)
    enemydown_animations.append(image)

for i in range(2):
    name = 'graphics/enemy' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    enemyright_animations.append(image)

for i in range(2):
    name = 'graphics/enemy' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    image = pygame.transform.rotate(image, 180)
    enemyleft_animations.append(image)

for i in range(2):
    name = 'graphics/boatshot' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    boatmissile_animations.append(image)

for i in range(7):
    name = 'graphics/flipper' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    flipper_animations.append(image)
