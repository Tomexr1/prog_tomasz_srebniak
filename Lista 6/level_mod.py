import pygame, constants, utils, mob_mod, player_mod, menu, stats, explosion, aiming_mob_mod, boss_mod
from sys import exit


class Level:
    def __init__(self, player, screen, clock):
        self.running = True
        self.player = player
        self.screen = screen
        self.clock = clock
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.mobs = pygame.sprite.Group()
        self.mob_bullets = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.background = pygame.image.load("out.png").convert()
        self.background = pygame.transform.scale(self.background,
                    (constants.WIDTH, constants.WIDTH*self.background.get_height()/self.background.get_width()))
        self.starting_position = -1 * self.background.get_height()
        self.background_y = self.starting_position
        self.scrolling = True
        self.mob_time = pygame.time.get_ticks()
        self.player_lives = 3
        self.paused_timer = 0
        self.boats_spawned = 0
        self.boat_hp = 3
        self.boat_turrets = pygame.sprite.Group()
        self.boats = pygame.sprite.Group()

    def update(self):
        self.bullets.add(self.player.bullets)
        self.all_sprites.add(self.player.bullets)
        self.mob_bullets.add(mob_mod.bullets_group)
        self.all_sprites.add(mob_mod.bullets_group)
        self.mob_bullets.add(aiming_mob_mod.boat_missiles_group)
        self.all_sprites.add(aiming_mob_mod.boat_missiles_group)

        self.all_sprites.update()

        self.hits()
        self.lives_update()
        self.player_pos()

        if pygame.key.get_pressed()[pygame.K_p]:
            self.paused()

    def paused(self):
        pygame.mixer.music.pause()
        paused_time = pygame.time.get_ticks()
        utils.draw_text(self.screen, "Zatrzymano", 30, 400, 120)
        utils.draw_text(self.screen, "Naciśnij [p] aby wznowić", 18, 400, 250)
        utils.draw_text(self.screen, "Naciśnij [ESC] aby wyjść z gry", 18, 400, 300)
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused_timer += pygame.time.get_ticks() - paused_time
                        pygame.mixer.music.unpause()
                        pause = False
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pause = False
                        mob_mod.bullets_group.empty()
                        aiming_mob_mod.boat_missiles_group.empty()
                        boss_mod.bullets_group.empty()

            pygame.display.update()
            self.clock.tick(15)

    def draw(self):
        self.all_sprites.draw(self.screen)
        # self.mob_draw()
        self.boat_spawn()
        self.draw_hud()

    def add_mob1(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if now - self.mob_time > spawn_rate:
            mob = mob_mod.Mob(400, 0, 0, 3, shoot_delay=1500, shooting='tap', type='flipper')
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.mob_time = now

    def add_mob2(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if now - self.mob_time > spawn_rate:
            mob = mob_mod.Mob(constants.WIDTH, 400, -2, 4, move_type=1, shooting='no', type='left')
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.mob_time = now

    def add_mob3(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if now - self.mob_time > spawn_rate:
            mob = mob_mod.Mob(0, 100, 4, 4, move_type=1, shooting='no', type='right')
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.mob_time = now

    def add_mob4(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if now - self.mob_time > spawn_rate:
            mob1 = mob_mod.Mob(200, -20, 0, 1, target_y=100, shooting='burst')
            mob2 = mob_mod.Mob(400, -20, 0, 1, target_y=100, shooting='cone')
            mob3 = mob_mod.Mob(600, -20, 0, 1, target_y=100, shooting='burst')
            self.all_sprites.add(mob1)
            self.mobs.add(mob1)
            self.all_sprites.add(mob2)
            self.mobs.add(mob2)
            self.all_sprites.add(mob3)
            self.mobs.add(mob3)
            self.mob_time = now

    def mob_draw(self):
        if -5800 < self.starting_position < -5780:
            self.add_mob1(700)
        if -5000 < self.starting_position < -4600:
            self.add_mob2(700)
        if -3800 < self.starting_position < -3400:
            self.add_mob3(1400)
        if -3000 < self.starting_position < -2900:
            self.add_mob4(1400)

    def hits(self):
        mob_hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in mob_hits:
            stats.kills += 1
            sound = pygame.mixer.Sound("music/explosion.wav")
            sound.play()
            sound.set_volume(0.1)

            expl = explosion.Explosion(hit.rect.center, 50)
            self.all_sprites.add(expl)

    def boat_spawn(self):
        if self.starting_position > -6000:  # do ustalenia
            if self.boats_spawned == 0:
                boat_body = aiming_mob_mod.BoatBody(200, 0, 100)
                self.boats.add(boat_body)
                self.all_sprites.add(boat_body)
                boat = aiming_mob_mod.Boat(200, 20, 100+20)
                self.boat_turrets.add(boat)
                self.all_sprites.add(boat)
                self.boats_spawned += 1
            elif self.boats_spawned == 1:
                hits = pygame.sprite.groupcollide(self.boats, self.bullets, False, True)
                for hit in hits:
                    self.boat_hp -= 1
                    if (self.boat_hp <= 0) and (len(self.boat_turrets) > 0):
                        self.boat_turrets.sprites()[0].kill()
                        self.boats.sprites()[0].kill()
                        sound = pygame.mixer.Sound("music/explosion.wav")
                        sound.play()
                        sound.set_volume(0.1)
                        expl = explosion.Explosion(hit.rect.center, 50)
                        self.all_sprites.add(expl)
                        stats.kills += 10
        # if self.starting_position < -6000:  # drugi boat
            # self.boats_spawned = 0
            # self.boat_hp = 100

    def boss_spawn(self):
        pass

    def draw_boss_hp(self):
        pass

    def player_pos(self):
        aiming_mob_mod.player_position = [self.player.rect.centerx, self.player.rect.centery]

    def lives_update(self):
        bullet_hits = pygame.sprite.spritecollide(self.player, self.mob_bullets, True)
        for hit in bullet_hits:
            self.player.update()
            self.player.kill()
            self.player = player_mod.Player()
            self.all_sprites.add(self.player)
            self.player_lives -= 1
            sound = pygame.mixer.Sound("music/explosion.wav")
            sound.play()
            sound.set_volume(0.1)
            print(self.player_lives)

        collision = pygame.sprite.spritecollide(self.player, self.mobs, True)
        for hit in collision:
            self.player.update()
            self.player.kill()
            self.player = player_mod.Player()
            self.all_sprites.add(self.player)
            self.player_lives -= 1
            expl = explosion.Explosion(hit.rect.center, 100)
            self.all_sprites.add(expl)
            sound = pygame.mixer.Sound("music/explosion.wav")
            sound.play()
            sound.set_volume(0.1)
            print(self.player_lives)

        if self.player_lives <= 0:
            self.running = False
            mob_mod.bullets_group.empty()
            aiming_mob_mod.boat_missiles_group.empty()
            boss_mod.bullets_group.empty()

    def end_of_game(self):
        menu.won()
        Level.running = False

    def draw_hud(self):
        utils.draw_text(self.screen, str(stats.kills), 50, constants.WIDTH/2 + 10, 10,
                        constants.SCORE_RED)
        utils.draw_text(self.screen, 'Czas: ' + str(round(stats.time / 1000)) + 's', 20, 730, 10, constants.SCORE_RED)
        utils.draw_text(self.screen, 'ŻYCIA: ', 30, 80, 10, constants.SCORE_RED)
        heart_img = pygame.image.load("heart.png").convert_alpha()
        heart_img = pygame.transform.scale(heart_img, (30, 30))
        for i in range(self.player_lives):
            self.screen.blit(heart_img, (140 + i * 40, 10))
