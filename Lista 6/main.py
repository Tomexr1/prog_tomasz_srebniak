import pygame, constants, menu, player_mod, level_mod
from sys import exit

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Lista 6")

if __name__ == "__main__":
    try:
        while True:
            print("Start gry")
            menu.start_menu()

            clock = pygame.time.Clock()
            # menu_timer = pygame.time.get_ticks()
            player = player_mod.Player()

            level = level_mod.Level(player, screen, clock)
            level.running = True

            while level.running:
                clock.tick(constants.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        level.running = False

                level.update()

                if level.scrolling:
                    level.starting_position += 2
                    level.background_y = level.starting_position
                    if level.starting_position + constants.HEIGHT + 2 > 0:
                        level.scrolling = False
                        screen.fill(constants.BLACK)
                        screen.blit(level.background, (0, level.background_y+constants.HEIGHT))
                    screen.fill(constants.BLACK)
                    screen.blit(level.background, (0, level.background_y+constants.HEIGHT))
                else:
                    screen.fill(constants.BLACK)
                    screen.blit(level.background, (0, level.background_y + constants.HEIGHT))

                level.draw()
                pygame.display.flip()
            del level
    except menu.MenuQuit: pass
    print("Koniec gry")
    pygame.mixer.quit()
    pygame.quit()
    exit()
