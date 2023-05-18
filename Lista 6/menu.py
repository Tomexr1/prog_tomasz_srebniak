import pygame, constants, utils

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
background = pygame.image.load("space.png").convert_alpha()
background = pygame.transform.scale(background, (constants.WIDTH, constants.HEIGHT))

clock = pygame.time.Clock()


class MenuQuit(Exception): pass


def start_menu():
    menu_running = True
    screen.fill(constants.MENU_FILL)
    menu_state = "main_menu"

    while menu_running:
        clock.tick(constants.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise MenuQuit

        # kontrola muzyki
        if utils.get_music_settings()[1] == "on":
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("music/menu_music.mp3")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

        k = pygame.key.get_pressed()

        if menu_state == "main_menu":
            command = utils.draw_main_menu_buttons(screen)
            if command == 0:  # start
                menu_running = False
            elif command == 1:  # rules
                menu_state = "rules"
            elif command == 2:  # settings
                menu_state = "settings"
            elif command == 3:  # best scores
                menu_state = "best_scores"
            elif command == 4:  # about
                menu_state = "about"
            elif command == 5:  # exit
                raise MenuQuit
        elif menu_state == "rules":
            command = utils.draw_rules(screen)
            if command == 0:  # back
                menu_state = "main_menu"
        elif menu_state == "settings":
            command = utils.draw_settings(screen)
            if command == 0:
                menu_state = "main_menu"
        elif menu_state == "best_scores":
            command = utils.draw_best_scores(screen)
            if command == 0:
                menu_state = "main_menu"
        elif menu_state == "about":
            command = utils.draw_about(screen)
            if command == 0:
                menu_state = "main_menu"

        pygame.display.flip()


def won():
    pass



