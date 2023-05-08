import pygame
from pygame import mixer
import sys
from pygame.locals import (
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        K_RETURN,
        K_a,
        K_d,
        K_BACKSPACE,
        KEYDOWN,
        QUIT
        )
from random import randint, choice
import json
from SpriteSheet import SpriteSheet
from Enemy import Enemy


# zmienne
window_width = 400
window_height = 600
gravity = 0.5
max_platforms = 7
scroll_threshold = 200
bg_scroll = 0
score = 0
fade_counter = 0
panel_color = (153, 217, 234)
collision_time = -2000

# inicjalizacja pygame
mixer.init()
pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('arcade')

# fonty
font_small = pygame.font.SysFont('Lucida Sans', 18)
font_big = pygame.font.SysFont('Lucida Sans', 24)
font_menu = pygame.font.SysFont('LucidaSans', 66)
font_cat = pygame.font.SysFont('LucidaSans', 56)

clock = pygame.time.Clock()
FPS = 60


def read_music():
    with open('scores.json', 'r') as f:
        music = json.load(f)
    if music['music'] == 'on':
        return True


# muzyka
pygame.mixer.music.load('media/music.mp3')
pygame.mixer.music.set_volume(0.5)
jump_fx = pygame.mixer.Sound('media/jump.mp3')
jump_fx.set_volume(0.4)
death_fx = pygame.mixer.Sound('media/death.mp3')
death_fx.set_volume(0.4)

# grafika
bg_image = pygame.image.load('media/bg.png').convert_alpha()
jumpy_image = pygame.image.load('media/jump.png').convert_alpha()
pad_image = pygame.image.load('media/pad.png').convert_alpha()
bird_spritesheet_img = pygame.image.load('media/bird.png').convert_alpha()
bird_spritesheet = SpriteSheet(bird_spritesheet_img)


def draw_bg(bg_scrl):
    window.blit(bg_image, (0, bg_scrl))
    window.blit(bg_image, (0, -600 + bg_scroll))  # na górze


def draw_text(text_to_draw, font, draw_color, x, y):
    img = font.render(text_to_draw, True, draw_color)
    window.blit(img, (x, y))


def draw_lives(surf, x, y, lives, img):
    img = pygame.transform.flip(img, True, False)
    for j in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x - 30 * j
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_panel():
    pygame.draw.rect(window, panel_color, (0, 0, window_width, 32))
    pygame.draw.line(window, 'white', (0, 32), (window_width, 32), 2)
    draw_text(f'WYNIK: {score}', font_small, 'white', 15, 5)


def read_control():
    with open('scores.json', 'r') as f:
        control = json.load(f)
    if control['control'] == 'arrows':
        return True


# klasa gracza
class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(jumpy_image, (45, 45))
        # dopasowanie prostokąta do kolizji
        self.width = 27
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.lives = 3
        self.last_one = 0, 0  # ostatnia dotknięta platforma
        self.flip = False
        self.mask = 0

    def move(self):
        dx = 0
        # dy = 0
        scrl = 0  # scroll
        key = pygame.key.get_pressed()
        if read_control():
            if key[K_LEFT]:
                dx = -5
                self.flip = True
            elif key[K_RIGHT]:
                dx = 5
                self.flip = False
        else:
            if key[K_a]:
                dx = -5
                self.flip = True
            elif key[K_d]:
                dx = 5
                self.flip = False
        self.vel_y += gravity  # spycha w dół
        dy = self.vel_y  # ustala się pozycja rect
        # kontrola wyjścia poza krawędź
        if self.rect.right + dx < 10:
            self.rect.x = window_width
        elif self.rect.left + dx > window_width - 10:
            self.rect.x = 0
        # kontrola kontaktu z platformami
        for plat in platform_group:
            if plat.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.rect.bottom < plat.rect.centery:
                    if self.vel_y > 0:
                        self.last_one = plat.rect.midtop
                        self.rect.bottom = plat.rect.top
                        self.vel_y = -15
                        if read_music():
                            jump_fx.play()
        # przesuwanie obrazu
        if self.rect.top <= scroll_threshold:
            if self.vel_y < 0:
                scrl = -dy

        self.rect.x += dx
        self.rect.y += dy + scrl

        # maska
        self.mask = pygame.mask.from_surface(self.image)
        return scrl

    def draw(self):
        window.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 10, self.rect.y - 5))
        # pygame.draw.rect(window, 'white', self.rect, 2)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pad_image, (width, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = moving
        self.move_counter = randint(0, 50)
        self.direction = choice([-1, 1])
        self.speed = randint(1, 2)

    def update(self, scrl):
        # poruszające się platformy
        if self.moving:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed
        # kontrola wyjścia poza ekran
        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > window_width:
            self.direction *= -1
            self.move_counter = 0
        # aktualizaja położenia platform
        self.rect.y += scrl
        # kontrola wyjścia poza ekran
        if self.rect.top > window_height:
            self.kill()


class Button:
    def __init__(self, button_text, x, y, width):
        self.text = button_text
        self.x = x
        self.y = y
        self.width = width

    def draw(self):
        button_rect = pygame.Rect(self.x, self.y, self.width, 40)
        if self.check_click():
            button_text = font_small.render(self.text, True, 'black')
            pygame.draw.rect(window, 'white', button_rect)
            pygame.draw.rect(window, 'black', button_rect, 2)
        else:
            button_text = font_small.render(self.text, True, 'white')
            pygame.draw.rect(window, 'black', button_rect)
            pygame.draw.rect(window, 'white', button_rect, 2)
        window.blit(button_text, (self.x + 7, self.y + 7))

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.Rect(self.x, self.y, self.width, 40)
        if left_click and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False


# gracz
jumpy = Player(window_width // 2, window_height - 150)
# sprite group
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


# początkowa platforma
platform = Platform(window_width // 2 - 60, window_height - 100, 100, False)
platform_group.add(platform)  # błąd to problem pycharma

# przyciski
menu_button = Button('Zapisz i wróć do menu', 100, 470, 210)
start_button = Button('Zagraj', 160, 200, 70)
rules_button = Button('Zasady', 158, 260, 74)
settings_button = Button('Ustawienia', 140, 320, 108)
best_scores_button = Button('Najlepsze wyniki', 117, 380, 158)
about_button = Button('O autorze', 145, 440, 100)
back_button = Button('Powrót', 10, 10, 75)
control_button = Button('Zmień', 160, 290, 68)
music_button = Button('Zmień', 160, 430, 68)
exit_button = Button('Wyjście', 160, 500, 75)


def read_scores():
    with open('scores.json', 'r') as f:
        scores = json.load(f)
    in_names = []
    in_points = []
    for k in scores['scores']:
        in_names.append(k['name'])
        in_points.append(k['score'])
    return in_names, in_points


def game():
    if read_music():
        pygame.mixer.music.play(-1, 0.0)

    done = False
    running = True
    game_over = False
    global bg_scroll, score, platform, fade_counter, collision_time

    names, points = read_scores()

    while running:
        clock.tick(FPS)
        if not game_over:
            scroll = jumpy.move()
            # tło
            bg_scroll += scroll
            if bg_scroll >= 600:
                bg_scroll = 0
            draw_bg(bg_scroll)
            if pygame.time.get_ticks() - collision_time > 2000:
                collision_immute = False
            # generowanie platform
            if len(platform_group) < max_platforms:
                plat_width = randint(60, 100)
                plat_x = randint(0, window_width - plat_width)
                plat_y = platform.rect.y - randint(80, 120)
                plat_type = randint(1, 2)
                if plat_type == 1 and score > 1000:
                    plat_moving = True
                else:
                    plat_moving = False
                platform = Platform(plat_x, plat_y, plat_width, plat_moving)
                platform_group.add(platform)
            # aktualizacja wyniku
            if scroll > 0:
                score += scroll
            # linia z najwyższym wynikiem
            best = read_scores()[1]
            pygame.draw.line(window, 'white', (0, score - best[0] + scroll_threshold),
                             (window_width, score - best[0] + scroll_threshold), 3)
            draw_text('BEST_SCORE', font_small, 'white', window_width - 130, score - best[0] + scroll_threshold)
            # sprites
            platform_group.update(scroll)
            platform_group.draw(window)

            # tworzenie wrogów
            if len(enemy_group) == 0 and score > 2000:
                enemy = Enemy(window_width, 100, bird_spritesheet, 1.5)
                enemy_group.add(enemy)

            enemy_group.draw(window)
            enemy_group.update(scroll, window_width)

            jumpy.draw()
            draw_panel()
            # kontrola żyć
            if jumpy.rect.top > window_height and jumpy.lives > 0:
                jumpy.lives -= 1
                jumpy.rect.midbottom = jumpy.last_one
                if read_music():
                    death_fx.play()
            if pygame.sprite.spritecollide(jumpy, enemy_group, False) and jumpy.lives > 0 \
                    and not collision_immute:
                if pygame.sprite.spritecollide(jumpy, enemy_group, False, pygame.sprite.collide_mask):
                    jumpy.lives -= 1
                    collision_immute = True
                    collision_time = pygame.time.get_ticks()
                    if read_music():
                        death_fx.play()
            if jumpy.lives == 0:
                game_over = True
            draw_lives(window, 355, 0, jumpy.lives, jumpy_image)
        else:
            if fade_counter < window_width:
                fade_counter += 10
                # animacja tła dla wyniku
                for i in range(0, 6, 2):
                    pygame.draw.rect(window, 'black', (0, i * 100, fade_counter, 100))
                    pygame.draw.rect(window, 'black', (window_width - fade_counter, (i + 1) * 100, window_width, 100))
            elif not done:
                pygame.mixer.music.stop()
                input_box = pygame.Rect(130, 400, 140, 32)
                color_inactive = 'white'
                color_active = 'royalblue'
                color = color_inactive
                active = False
                text = ''
                while not done:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                        if pygame.mouse.get_pressed()[0]:
                            if input_box.collidepoint(pygame.mouse.get_pos()):
                                active = not active
                            else:
                                active = False
                            color = color_active if active else color_inactive
                        if event.type == KEYDOWN:
                            if active:
                                if event.key == K_RETURN:
                                    once = 0
                                    for j in points:
                                        if score > j and once == 0:
                                            index = points.index(j)
                                            points.insert(index, score)
                                            names.insert(index, text)
                                            once += 1
                                    x = {"scores": [{"name": names[0], "score": points[0]},
                                                    {"name": names[1], "score": points[1]},
                                                    {"name": names[2], "score": points[2]},
                                                    {"name": names[3], "score": points[3]},
                                                    {"name": names[4], "score": points[4]},
                                                    ],
                                         "control": "arrows" if read_control() else "a-d",
                                         "music": "on" if read_music() else "off"}
                                    with open('scores.json', 'w', encoding='utf-8') as f:
                                        json.dump(x, f, indent=4)
                                    done = True
                                elif event.key == K_BACKSPACE:
                                    text = text[:-1]
                                elif len(text) < 9:
                                    text += event.unicode
                        if menu_button.check_click():
                            once = 0
                            for j in points:
                                if score > j and once == 0:
                                    index = points.index(j)
                                    points.insert(index, score)
                                    names.insert(index, text)
                                    once += 1
                            x = {"scores": [{"name": names[0], "score": points[0]},
                                            {"name": names[1], "score": points[1]},
                                            {"name": names[2], "score": points[2]},
                                            {"name": names[3], "score": points[3]},
                                            {"name": names[4], "score": points[4]},
                                            ],
                                 "control": "arrows" if read_control() else "a-d",
                                 "music": "on" if read_music() else "off"}
                            with open('scores.json', 'w', encoding='utf-8') as f:
                                json.dump(x, f, indent=4)
                            done = True
                    window.fill('black')
                    draw_text('KONIEC GRY', font_big, 'white', 125, 150)
                    draw_text(f'WYNIK:', font_big, 'white', 157, 200)
                    draw_text(str(score), font_big, 'white', window_width // 2 - 7 * len(str(score)), 250)
                    draw_text('Wprowadź imię:', font_small, 'white', 130, 350)
                    txt_surface = font_small.render(text, True, color)
                    window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                    pygame.draw.rect(window, color, input_box, 2)
                    menu_button.draw()
                    pygame.display.update()

            else:
                # reset zmiennych
                game_over = False
                score = 0
                jumpy.lives = 3
                fade_counter = 0
                # reset obiektów
                jumpy.rect.center = window_width // 2, window_height - 150
                platform_group.empty()
                enemy_group.empty()
                # początkowa platforma
                platform = Platform(window_width // 2 - 60, window_height - 100, 100, False)
                platform_group.add(platform)
                running = False
        # opcje zakończenia gry
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def rules():
    clock.tick(FPS)
    running = True
    window.fill('black')
    draw_text('ZASADY', font_cat, 'white', 90, 70)
    draw_text('Celem gry jest zdobycie jak największej', font_small, 'white', 27, 180)
    draw_text('liczby punktów i uplasowanie się', font_small, 'white', 55, 220)
    draw_text('na pierwszym miejscu w tabeli wyników.', font_small, 'white', 27, 260)
    draw_text('Poruszając się na boki wskakuj', font_small, 'white', 60, 330)
    draw_text('na kolejne platformy.', font_small, 'white', 105, 370)
    draw_text('Uważaj na poruszające się', font_small, 'white', 85, 410)
    draw_text('oraz chcące Cię strącić ptaki!', font_small, 'white', 68, 450)
    draw_text('Masz 3 życia.', font_small, 'white', 140, 490)

    while running:
        for event in pygame.event.get():
            if back_button.check_click():
                running = False
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        back_button.draw()
        pygame.display.update()


def settings():
    clock.tick(FPS)
    running = True
    while running:
        for event in pygame.event.get():
            if back_button.check_click():
                running = False
            elif control_button.check_click():
                names, points = read_scores()
                if read_control():
                    x = {"scores": [{"name": names[0], "score": points[0]},
                                    {"name": names[1], "score": points[1]},
                                    {"name": names[2], "score": points[2]},
                                    {"name": names[3], "score": points[3]},
                                    {"name": names[4], "score": points[4]},
                                    ],
                         "control": "a-d",
                         "music": "on" if read_music() else "off"}
                    with open('scores.json', 'w', encoding='utf-8') as f:
                        json.dump(x, f, indent=4)
                else:
                    x = {"scores": [{"name": names[0], "score": points[0]},
                                    {"name": names[1], "score": points[1]},
                                    {"name": names[2], "score": points[2]},
                                    {"name": names[3], "score": points[3]},
                                    {"name": names[4], "score": points[4]},
                                    ],
                         "control": "arrows",
                         "music": "on" if read_music() else "off"}
                    with open('scores.json', 'w', encoding='utf-8') as f:
                        json.dump(x, f, indent=4)
            elif music_button.check_click():
                names, points = read_scores()
                if read_music():
                    x = {"scores": [{"name": names[0], "score": points[0]},
                                    {"name": names[1], "score": points[1]},
                                    {"name": names[2], "score": points[2]},
                                    {"name": names[3], "score": points[3]},
                                    {"name": names[4], "score": points[4]},
                                    ],
                         "control": "arrows" if read_control() else "a-d",
                         "music": "off"}
                    with open('scores.json', 'w', encoding='utf-8') as f:
                        json.dump(x, f, indent=4)
                else:
                    x = {"scores": [{"name": names[0], "score": points[0]},
                                    {"name": names[1], "score": points[1]},
                                    {"name": names[2], "score": points[2]},
                                    {"name": names[3], "score": points[3]},
                                    {"name": names[4], "score": points[4]},
                                    ],
                         "control": "arrows" if read_control() else "a-d",
                         "music": "on"}
                    with open('scores.json', 'w', encoding='utf-8') as f:
                        json.dump(x, f, indent=4)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        window.fill('black')
        draw_text('USTAWIENIA', font_cat, 'white', 40, 90)
        if read_control():
            draw_text('Steruj strzałkami', font_big, 'white', 100, 240)
        else:
            draw_text('Steruj klawiaszami a-d', font_big, 'white', 75, 240)
        if read_music():
            draw_text('Muzyka włączona', font_big, 'white', 100, 380)
        else:
            draw_text('Muzyka wyłączona', font_big, 'white', 90, 380)
        music_button.draw()
        control_button.draw()
        back_button.draw()
        pygame.display.update()


def best_scores():
    clock.tick(FPS)
    running = True
    window.fill('black')
    draw_text('NAJLEPSZE', font_cat, 'white', 55, 90)
    draw_text('WYNIKI', font_cat, 'white', 100, 160)
    while running:
        for event in pygame.event.get():
            if back_button.check_click():
                running = False
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        names, points = read_scores()
        for i in range(len(names)):
            draw_text(f'{i + 1}. {names[i]}', font_big, 'white', 40, 285 + i * 50)
            draw_text(str(points[i]), font_big, 'white', 240, 285 + i * 50)
        back_button.draw()
        pygame.display.update()


def about():
    clock.tick(FPS)
    running = True
    window.fill('black')
    draw_text('O AUTORZE', font_cat, 'white', 35, 90)
    draw_text('Cześć!', font_small, 'white', 170, 200)
    draw_text('Mam na imię Asia i jestem studenką', font_small, 'white', 45, 270)
    draw_text('1. roku mamematyki stosowanej na PWR.', font_small, 'white', 25, 310)
    draw_text('Gra powstała w ramach wykonania', font_small, 'white', 50, 390)
    draw_text('projektu na zajęcia z programowania.', font_small, 'white', 40, 430)
    draw_text('Mam nadzieję, że Ci się spodoba!', font_small, 'white', 50, 470)
    while running:
        for event in pygame.event.get():
            if back_button.check_click():
                running = False
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        back_button.draw()
        pygame.display.update()


def menu():
    while True:
        clock.tick(FPS)
        window.fill('black')
        for event in pygame.event.get():
            if start_button.check_click():
                game()
            elif rules_button.check_click():
                rules()
            elif settings_button.check_click():
                settings()
            elif best_scores_button.check_click():
                best_scores()
            elif about_button.check_click():
                about()
            elif exit_button.check_click():
                pygame.quit()
                sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        draw_text('MENU', font_menu, 'white', 100, 70)
        start_button.draw()
        rules_button.draw()
        settings_button.draw()
        best_scores_button.draw()
        about_button.draw()
        exit_button.draw()
        pygame.display.update()


menu()