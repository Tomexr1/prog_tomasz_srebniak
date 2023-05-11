import pygame, constants
import json


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, constants.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)


def get_hs():
    with open('data.json', 'r') as f:
        data = json.load(f)
        names, scores = [], []
        for score in data["scores"]:
            names.append(score["name"])
            scores.append(score["score"])
    return names, scores


def get_music_settings():
    with open('data.json', 'r') as f:
        data = json.load(f)
        music_in_game = data["settings"]["music_in_game"]
        music_in_menu = data["settings"]["music_in_menu"]
    return music_in_game, music_in_menu


def set_music_settings(music_in_game, music_in_menu):
    with open('data.json', 'r') as f:
        data = json.load(f)
    with open('data.json', 'w') as f:
        data["settings"]["music_in_game"] = music_in_game
        data["settings"]["music_in_menu"] = music_in_menu
        json.dump(data, f)


class Button:
    def __init__(self, button_text, x, y, width, screen):
        self.text = button_text
        self.x = x
        self.y = y
        self.width = width
        self.screen = screen

    def draw(self):
        button_rect = pygame.Rect(self.x, self.y, self.width, 40)
        if self.check_click():
            button_text = pygame.font.Font(pygame.font.match_font('arial'), 18).render(self.text, True, constants.BLACK)
            pygame.draw.rect(self.screen, constants.WHITE, button_rect)
            pygame.draw.rect(self.screen, constants.DUSTY_BLUE, button_rect, 2)
        else:
            button_text = pygame.font.Font(pygame.font.match_font('arial'), 18).render(self.text, True, constants.WHITE)
            pygame.draw.rect(self.screen, constants.DUSTY_BLUE, button_rect)
            pygame.draw.rect(self.screen, constants.WHITE, button_rect, 2)
        self.screen.blit(button_text, (self.x + 7, self.y + 7))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.Rect(self.x, self.y, self.width, 40)
        if left_click and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class ImgButton:
    def __init__(self, x, y, image, scale, screen):
        wdth = image.get_width()
        hght = image.get_height()
        self.image = pygame.transform.scale(image, (int(wdth * scale), int(hght * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        if left_click and self.rect.collidepoint(mouse_pos):
            return True
        else:
            return False


class Button2:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


"""Sekcja menu głównego---------------------------------------------------------------------------------------------"""


def draw_main_menu_buttons(screen):
    background = pygame.image.load('space.png')
    background = pygame.transform.scale(background, (constants.WIDTH, constants.HEIGHT))
    screen.blit(background, (0, 0))

    s_shot = pygame.image.load('sshot.png')
    s_shot = pygame.transform.scale(s_shot, (constants.WIDTH/2, constants.HEIGHT/2))
    screen.blit(s_shot, (constants.WIDTH/2 - 70, constants.HEIGHT/2 - 80))

    draw_text(screen, "Menu", 70, constants.WIDTH/2, 50)
    exit_button = Button('Wyjście', 160, 500, 75, screen)
    start_button = Button('Zagraj', 160, 200, 70, screen)
    rules_button = Button('Zasady', 158, 260, 74, screen)
    settings_button = Button('Ustawienia', 140, 320, 108, screen)
    best_scores_button = Button('Najlepsze wyniki', 117, 380, 158, screen)
    about_button = Button('O autorze', 145, 440, 100, screen)

    start_button.draw()
    rules_button.draw()
    settings_button.draw()
    best_scores_button.draw()
    about_button.draw()
    exit_button.draw()

    command = None
    if start_button.check_click():
        command = 0
    elif rules_button.check_click():
        command = 1
    elif settings_button.check_click():
        command = 2
    elif best_scores_button.check_click():
        command = 3
    elif about_button.check_click():
        command = 4
    elif exit_button.check_click():
        command = 5
    return command


def draw_rules(screen):
    main_background = pygame.image.load('space.png')
    main_background = pygame.transform.scale(main_background, (constants.WIDTH, constants.HEIGHT))
    screen.blit(main_background, (0, 0))

    background = pygame.image.load('tan_pressed.png').convert_alpha()
    background = pygame.transform.scale(background, (constants.WIDTH/4*3, constants.HEIGHT/4*3))
    screen.blit(background, (100, 80))

    draw_text(screen, "Zasady", 60, constants.WIDTH / 2, constants.HEIGHT / 5)
    draw_text(screen, "Witaj w x.", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 100)
    draw_text(screen, "Gra polega na zestrzeliwaniu przeciwników", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 130)
    draw_text(screen, "i zbieraniu w ten sposób punktów.", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 160)
    draw_text(screen, "Unikaj pocisków przeciwnika.", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 190)
    draw_text(screen, "Aby wygrać, pokonaj bossa,", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 220)
    draw_text(screen, "Sterowanie: ", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 250)
    draw_text(screen, "[W], [A], [S], [D] - poruszanie się", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 280)
    draw_text(screen, "[Spacja] - strzelanie", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 310)
    draw_text(screen, "[P] - pauza", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 340)

    x_button_img = pygame.image.load('x_button.png').convert_alpha()
    x_button = ImgButton(560, 120, x_button_img, 5, screen)
    x_button.draw()

    command = None
    if x_button.check_click():
        command = 0
    return command


def draw_settings(screen):
    main_background = pygame.image.load('space.png')
    main_background = pygame.transform.scale(main_background, (constants.WIDTH, constants.HEIGHT))
    screen.blit(main_background, (0, 0))

    background = pygame.image.load('tan_pressed.png').convert_alpha()
    background = pygame.transform.scale(background, (constants.WIDTH / 4 * 3, constants.HEIGHT / 4 * 3))
    screen.blit(background, (100, 80))

    draw_text(screen, "Ustawienia", 60, constants.WIDTH / 2, constants.HEIGHT / 5)

    draw_text(screen, "Muzyka w grze: ", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 100)
    if get_music_settings()[0] == "off":
        in_game_off_img = pygame.image.load('off.png').convert_alpha()
        in_game_off = ImgButton(constants.WIDTH / 2 + 70, constants.HEIGHT / 5 + 100, in_game_off_img, 1.5, screen)
        in_game_off.draw()
        if in_game_off.check_click():
            set_music_settings("on", get_music_settings()[1])
        # in_game_off = Button2(constants.WIDTH / 2 + 70, constants.HEIGHT / 5 + 100, in_game_off_img, 1.5)
        # if in_game_off.draw(screen):
        #     set_music_settings("on", get_music_settings()[1])
    else:
        in_game_on_img = pygame.image.load('on.png').convert_alpha()
        in_game_on = ImgButton(constants.WIDTH/2 + 70, constants.HEIGHT/5 + 100, in_game_on_img, 1.5, screen)
        in_game_on.draw()
        if in_game_on.check_click():
            set_music_settings("off", get_music_settings()[1])
        # in_game_on = Button2(constants.WIDTH / 2 + 70, constants.HEIGHT / 5 + 100, in_game_on_img, 1.5)
        # if in_game_on.draw(screen):
        #     set_music_settings("off", get_music_settings()[1])
    if get_music_settings()[1] == "off":
        in_menu_off_img = pygame.image.load('off.png').convert_alpha()
        in_menu_off = ImgButton(constants.WIDTH / 2 + 75, constants.HEIGHT / 5 + 150, in_menu_off_img, 1.5, screen)
        in_menu_off.draw()
        if in_menu_off.check_click():
            set_music_settings(get_music_settings()[0], "on")
        # in_menu_off = Button2(constants.WIDTH / 2 + 75, constants.HEIGHT / 5 + 150, in_menu_off_img, 1.5)
        # if in_menu_off.draw(screen):
        #     set_music_settings(get_music_settings()[0], "on")
    else:
        in_menu_on_img = pygame.image.load('on.png').convert_alpha()
        in_menu_on = ImgButton(constants.WIDTH / 2 + 75, constants.HEIGHT / 5 + 150, in_menu_on_img, 1.5, screen)
        in_menu_on.draw()
        if in_menu_on.check_click():
            set_music_settings(get_music_settings()[0], "off")
        # in_menu_on = Button2(constants.WIDTH / 2 + 75, constants.HEIGHT / 5 + 150, in_menu_on_img, 1.5)
        # if in_menu_on.draw(screen):
        #     set_music_settings(get_music_settings()[0], "off")

    draw_text(screen, "Muzyka w menu: ", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 150)

    x_button_img = pygame.image.load('x_button.png').convert_alpha()
    x_button = ImgButton(560, 120, x_button_img, 5, screen)
    x_button.draw()

    command = None
    if x_button.check_click():
        command = 0
    return command


def draw_best_scores(screen):
    main_background = pygame.image.load('space.png')
    main_background = pygame.transform.scale(main_background, (constants.WIDTH, constants.HEIGHT))
    screen.blit(main_background, (0, 0))

    background = pygame.image.load('tan_pressed.png').convert_alpha()
    background = pygame.transform.scale(background, (constants.WIDTH / 4 * 3, constants.HEIGHT / 4 * 3))
    screen.blit(background, (100, 80))

    names, scores = get_hs()

    draw_text(screen, "Top wyniki", 60, constants.WIDTH / 2, constants.HEIGHT / 5)

    for i in range(3):
        try:
            draw_text(screen, str(i+1) + ". " + names[i] + " - " + str(scores[i]),
                      20, constants.WIDTH / 2, constants.HEIGHT / 5 + 100 + 30*i)
        except IndexError:
            draw_text(screen, str(i+1) + ". " + "brak",
                      20, constants.WIDTH / 2, constants.HEIGHT / 5 + 100 + 30*i)


    x_button_img = pygame.image.load('x_button.png').convert_alpha()
    x_button = ImgButton(560, 120, x_button_img, 5, screen)
    x_button.draw()

    command = None
    if x_button.check_click():
        command = 0
    return command


def draw_about(screen):
    main_background = pygame.image.load('space.png')
    main_background = pygame.transform.scale(main_background, (constants.WIDTH, constants.HEIGHT))
    screen.blit(main_background, (0, 0))

    background = pygame.image.load('tan_pressed.png').convert_alpha()
    background = pygame.transform.scale(background, (constants.WIDTH / 4 * 3, constants.HEIGHT / 4 * 3))
    screen.blit(background, (100, 80))

    draw_text(screen, "O autorze", 60, constants.WIDTH / 2, constants.HEIGHT / 5)
    draw_text(screen, "Bla bla bla", 20, constants.WIDTH / 2, constants.HEIGHT / 5 + 100)

    x_button_img = pygame.image.load('x_button.png').convert_alpha()
    x_button = ImgButton(560, 120, x_button_img, 5, screen)
    x_button.draw()

    command = None
    if x_button.check_click():
        command = 0
    return command


