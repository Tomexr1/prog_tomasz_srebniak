import pygame, constants, menu, player_mod, level_mod, utils, stats
from sys import exit

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Lista 6")

if __name__ == "__main__":
    try:
        while True:
            menu.start_menu()

            clock = pygame.time.Clock()
            menu_timer = pygame.time.get_ticks()
            player = player_mod.Player()

            level = level_mod.Level(player, screen, clock)
            level.running = True

            # kontrola muzyki
            if utils.get_music_settings()[0] == "on":
                pygame.mixer.music.load("music/ingame_music.mp3")  # po minucie zaczyna się perkusja
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)

            while level.running:
                clock.tick(constants.FPS)
                stats.time = pygame.time.get_ticks() - menu_timer - level.paused_timer

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        level.running = False
                        raise menu.MenuQuit

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
            pygame.mixer.music.stop()
            del level
    except menu.MenuQuit: pass

    pygame.mixer.quit()
    pygame.quit()
    exit()
