import pygame, constants, utils, stats

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
background = pygame.image.load("graphics/space.png").convert_alpha()
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
    pygame.mixer.music.pause()
    sound = pygame.mixer.Sound("music/Win sound.wav")
    sound.play()
    # sound.set_volume(0.1)

    background = pygame.image.load('graphics/white_pressed.png').convert_alpha()
    background = pygame.transform.scale(background, (constants.WIDTH, constants.HEIGHT))

    screen.fill(constants.ENDGAME_WHITE)

    paused_time = pygame.time.get_ticks()

    input_box = utils.InputBox(300, 300, 140, 32)

    won_running = True
    while won_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            input_box.handle_event(event)

            k = pygame.key.get_pressed()
            if k[pygame.K_RETURN]:
                utils.set_scores(input_box.text, stats.kills)
                won_running = False
            if k[pygame.K_ESCAPE]:
                won_running = False

        screen.blit(background, (0, 0))

        utils.draw_text(screen, "WYGRANA!", 50, 400, 70, color=constants.GRAY)
        utils.draw_text(screen, f"Twój wynik: {stats.kills}", 18, 400, 200, color=constants.GRAY)
        utils.draw_text(screen, "Podaj swoje imię i naciśnij [ENTER] aby zatwierdzić:", 18, 400, 250,
                        color=constants.GRAY)
        utils.draw_text(screen, "Albo naciśnij [ESC] aby wyjść do menu", 18, 400, 360, color=constants.GRAY)

        input_box.update()
        input_box.draw(screen)

        pygame.display.update()
        clock.tick(30)


def lost():
    pygame.mixer.music.pause()
    # sound = pygame.mixer.Sound("music/Lose sound.wav")
    # sound.play()
    # sound.set_volume(0.1)

    paused_time = pygame.time.get_ticks()

    background = pygame.image.load('graphics/white_pressed.png').convert_alpha()
    background = pygame.transform.scale(background, (constants.WIDTH, constants.HEIGHT))
    screen.fill(constants.ENDGAME_WHITE)

    input_box = utils.InputBox(300, 300, 140, 32)

    lost_running = True
    while lost_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            input_box.handle_event(event)

            k = pygame.key.get_pressed()
            if k[pygame.K_RETURN]:
                utils.set_scores(input_box.text, stats.kills)
                lost_running = False
            if k[pygame.K_ESCAPE]:
                lost_running = False

        screen.blit(background, (0, 0))

        utils.draw_text(screen, "PRZEGRANA", 50, 400, 70, color=constants.GRAY)
        utils.draw_text(screen, f"Twój wynik: {stats.kills}", 18, 400, 200, color=constants.GRAY)
        utils.draw_text(screen, "Podaj swoje imię i naciśnij [ENTER] aby zatwierdzić:", 18, 400, 250,
                        color=constants.GRAY)
        utils.draw_text(screen, "Albo naciśnij [ESC] aby wyjść do menu", 18, 400, 360, color=constants.GRAY)
        input_box.update()
        input_box.draw(screen)

        pygame.display.update()
        clock.tick(30)

