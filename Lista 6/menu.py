import pygame, constants, text
import sys

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

clock = pygame.time.Clock()


class MenuQuit(Exception): pass


def start_menu():
    menu_running = True
    screen.fill(constants.MENU_FILL)
    pygame.display.flip()

    while menu_running:
        clock.tick(constants.FPS)

        command = draw_buttons()
        if command == 0:
            raise MenuQuit
        elif command == 1:
            menu_running = False
            print("zagraj")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # screen.fill(constants.MENU_FILL)



        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            menu_running = False
            print("spacja")
        elif keystate[pygame.K_ESCAPE]:
            raise MenuQuit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # pygame.display.update()
        pygame.display.flip()


def won():
    pass


def draw_buttons():
    text.draw_text(screen, "Menu", 50, constants.WIDTH / 2, constants.HEIGHT / 4)
    exit_button = text.Button('Wyjście', 160, 500, 75, screen)
    start_button = text.Button('Zagraj', 160, 200, 70, screen)
    rules_button = text.Button('Zasady', 158, 260, 74, screen)
    settings_button = text.Button('Ustawienia', 140, 320, 108, screen)
    best_scores_button = text.Button('Najlepsze wyniki', 117, 380, 158, screen)
    about_button = text.Button('O autorze', 145, 440, 100, screen)

    start_button.draw()
    rules_button.draw()
    settings_button.draw()
    best_scores_button.draw()
    about_button.draw()
    exit_button.draw()

    command = None

    if exit_button.check_click():
        command = 0
    if start_button.check_click():
        command = 1
    return command


