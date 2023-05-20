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
boat_turret_animations = []
boat_animations = []
smoke_animations = []
kamikaze_animations = []
blank_image = pygame.Surface((1, 1), pygame.SRCALPHA)


for i in range(4):
    name = 'graphics/plane' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    image = pygame.transform.scale(image, (80, 49))
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

for i in range(3):
    name = 'graphics/boat_body' + str(i+1) + '.png'
    image = pygame.image.load(name).convert_alpha()
    boat_animations.append(image)

for i in range(180):
    image = pygame.image.load('graphics/turret/boat_turret' + str(i) + '.png').convert_alpha()
    boat_turret_animations.append(image)

for i in range(7):
    image = pygame.image.load('graphics/smoke' + str(i+1) + '.png').convert_alpha()
    smoke_animations.append(image)

for i in range(2):
    image = pygame.image.load('graphics/kamikaze' + str(i+1) + '.png').convert_alpha()
    image = pygame.transform.scale(image, (40, 46))
    kamikaze_animations.append(image)
