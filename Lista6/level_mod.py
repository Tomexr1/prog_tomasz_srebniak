import pygame, constants, utils, mob_mod, player_mod, menu, stats, explosion, aiming_mob_mod, boss_mod, bullets
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
        self.background = pygame.image.load("graphics/out3.png").convert()
        self.background = pygame.transform.scale(self.background,
                    (constants.WIDTH, constants.WIDTH*self.background.get_height()/self.background.get_width()))
        self.starting_position = -1 * self.background.get_height()
        print(self.starting_position)
        self.background_y = self.starting_position
        self.scrolling = True
        self.mob_time = pygame.time.get_ticks()
        self.player_lives = 3
        self.paused_timer = 0
        self.boats_spawned = 0
        self.boat_hp = 3
        self.boat_turrets = pygame.sprite.Group()
        self.boats = pygame.sprite.Group()
        self.boss_spawned = False
        self.boss = pygame.sprite.Group()
        self.boss_hp = 100
        self.boss_down_timer = 0
        self.rocket_explosions = pygame.sprite.Group()
        self.kamikaze_spawned = 0
        self.kamikaze = pygame.sprite.Group()
        self.number_of_spawns = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

    def update(self):
        self.bullets.add(self.player.bullets)
        self.all_sprites.add(self.player.bullets)
        self.mob_bullets.add(mob_mod.bullets_group)
        self.all_sprites.add(mob_mod.bullets_group)
        self.all_sprites.add(bullets.explosions)
        self.rocket_explosions.add(bullets.explosions)
        self.mob_bullets.add(aiming_mob_mod.boat_missiles_group)
        self.all_sprites.add(aiming_mob_mod.boat_missiles_group)
        self.mob_bullets.add(boss_mod.bullets_group)
        self.all_sprites.add(boss_mod.bullets_group)
        self.all_sprites.add(player_mod.smoke_group)

        self.all_sprites.update()

        self.hits()
        self.lives_update()
        self.player_pos()

        if pygame.key.get_pressed()[pygame.K_p]:
            self.paused()

        if (pygame.time.get_ticks() - self.boss_down_timer > 2000) and (self.boss_down_timer != 0):
            self.end_of_game()

    def paused(self):
        pygame.mixer.music.pause()
        paused_time = pygame.time.get_ticks()
        utils.draw_text(self.screen, "Zatrzymano", 30, 400, 120)
        utils.draw_text(self.screen, "Naciśnij [p] aby wznowić", 18, 400, 250)
        utils.draw_text(self.screen, "Naciśnij [ESC] aby wyjść do menu", 18, 400, 300)
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
                        self.empty_groups()
                        stats.kills = 0
                        stats.time = 0

            pygame.display.update()
            self.clock.tick(15)

    def draw(self):
        self.all_sprites.draw(self.screen)
        self.mob_draw()
        self.add_kamikaze()
        self.boat_spawn()
        self.boss_spawn()

        self.draw_hud()
        self.draw_boss_hp()

    def add_mob1(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[0] == 0):
            mob = mob_mod.Mob(400, 0, 0, 3, target_y=120, shoot_delay=1500, shooting='tap')
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.mob_time = now
            self.number_of_spawns[0] += 1

    def add_mob2(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[1] < 7):
            mob = mob_mod.Mob(constants.WIDTH, 400, -2, 4, move_type=1, shooting='no', type='left')
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.mob_time = now
            self.number_of_spawns[1] += 1

    def add_mob3(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[2] < 7):
            mob = mob_mod.Mob(0, 100, 4, 4, move_type=1, shooting='no', type='right')
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.mob_time = now
            self.number_of_spawns[2] += 1

    def add_mob4(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[3] == 0):
            mob1 = mob_mod.Mob(200, -20, 0, 1, target_y=100, shoot_delay=2100, shooting='burst')
            mob2 = mob_mod.Mob(400, -20, 0, 1, target_y=100, shooting='cone')
            mob3 = mob_mod.Mob(600, -20, 0, 1, target_y=100, shoot_delay=1900, shooting='burst')
            self.all_sprites.add(mob1)
            self.mobs.add(mob1)
            self.all_sprites.add(mob2)
            self.mobs.add(mob2)
            self.all_sprites.add(mob3)
            self.mobs.add(mob3)
            self.mob_time = now
            self.number_of_spawns[3] += 1

    def add_mob5(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[4] == 0):
            mob1 = mob_mod.Mob(700, -20, -1, 2, target_y=100, shooting='shoot_circle')
            self.all_sprites.add(mob1)
            self.mobs.add(mob1)
            mob2 = mob_mod.Mob(10, -20, 1, 2, target_y=100, shooting='shoot_circle')
            self.all_sprites.add(mob2)
            self.mobs.add(mob2)
            self.mob_time = now
            self.number_of_spawns[4] += 1

    def add_mob6(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[5] < 7):
            mob1 = mob_mod.Mob(0, 70, 4, 4, move_type=1, shooting='no', type='right')
            self.all_sprites.add(mob1)
            self.mobs.add(mob1)
            mob2 = mob_mod.Mob(constants.WIDTH, 450, -3, 4, move_type=1, shooting='no', type='left')
            self.all_sprites.add(mob2)
            self.mobs.add(mob2)
            self.mob_time = now
            self.number_of_spawns[5] += 1

    def add_mob7(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[6] == 0):
            mob1 = mob_mod.Mob(700, -20, -1, 2, target_y=100, shooting='shoot_circle')
            self.all_sprites.add(mob1)
            self.mobs.add(mob1)
            mob2 = mob_mod.Mob(10, -20, 1, 2, target_y=100, shooting='shoot_circle')
            self.all_sprites.add(mob2)
            self.mobs.add(mob2)
            mob3 = mob_mod.Mob(350, -20, 0, 1, target_y=100, shoot_delay=1300, shooting='burst')
            self.all_sprites.add(mob3)
            self.mobs.add(mob3)
            self.mob_time = now
            self.number_of_spawns[6] += 1

    def add_mob8(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[7] < 7):
            mob1 = mob_mod.Mob(-100, 70, 4, 4, move_type=1, shooting='no', type='right')
            self.all_sprites.add(mob1)
            self.mobs.add(mob1)
            mob2 = mob_mod.Mob(constants.WIDTH, 450, -3, 4, move_type=1, shooting='no', type='left')
            self.all_sprites.add(mob2)
            self.mobs.add(mob2)
            self.mob_time = now
            self.number_of_spawns[7] += 1

    def add_mob9(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[8] < 7):
            mob = mob_mod.Mob(constants.WIDTH, 400, -2, 4, move_type=1, shooting='no', type='left')
            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.mob_time = now
            self.number_of_spawns[1] += 1

    def add_mob10(self, spawn_rate=100):
        now = pygame.time.get_ticks()
        if (now - self.mob_time > spawn_rate) and (self.number_of_spawns[9] == 0):
            mob1 = mob_mod.Mob(700, -20, -1, 2, target_y=200, shooting='shoot_circle')
            self.all_sprites.add(mob1)
            self.mobs.add(mob1)
            mob2 = mob_mod.Mob(200, -20, 1, 2, target_y=100, shoot_delay=1000, shooting='burst')
            self.all_sprites.add(mob2)
            self.mobs.add(mob2)
            self.number_of_spawns[9] += 1

    def mob_draw(self):
        if -9250 < self.starting_position:
            self.add_mob1()
        if -8500 < self.starting_position < -8100:
            self.add_mob2(700)
        if -7300 < self.starting_position < -6900:
            self.add_mob3(1400)
        if -6500 < self.starting_position < -6400:
            self.add_mob4(1400)
        if -4500 < self.starting_position < -4480:
            self.add_mob5()
        if -3800 < self.starting_position < -3400:  # umierają w -3108
            self.add_mob6(700)
        if -3120 < self.starting_position < -3000:
            self.add_mob7()
        if -2700 < self.starting_position < -2400:
            self.add_mob8(700)
        if -1700 < self.starting_position < -1400:
            self.add_mob9(700)
        if -1500 < self.starting_position:
            self.add_mob10()

    def add_kamikaze(self):
        if self.starting_position > -7500:
            if self.kamikaze_spawned == 0:
                mob = mob_mod.Mob(0, 300, 4, -1, type='kamikazeright')
                self.all_sprites.add(mob)
                self.kamikaze.add(mob)
                self.kamikaze_spawned = 1
        if self.starting_position > -4700:
            if self.kamikaze_spawned == 1:
                mob = mob_mod.Mob(800, 50, -4, 1, type='kamikazeleft')
                self.all_sprites.add(mob)
                self.kamikaze.add(mob)
                self.kamikaze_spawned = 2
        if self.starting_position > -3100:
            if self.kamikaze_spawned == 2:
                mob = mob_mod.Mob(0, 300, 4, -2, type='kamikazeright')
                self.all_sprites.add(mob)
                self.kamikaze.add(mob)
                self.kamikaze_spawned = 3
        if self.starting_position > -1500:
            if self.kamikaze_spawned == 3:
                mob = mob_mod.Mob(800, 50, -4, 2, type='kamikazeleft')
                self.all_sprites.add(mob)
                self.kamikaze.add(mob)
                self.kamikaze_spawned = 4

    def hits(self):
        mob_hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in mob_hits:
            stats.kills += 20
            sound = pygame.mixer.Sound("music/explosion.wav")
            sound.play()
            sound.set_volume(0.1)

            expl = explosion.Explosion(hit.rect.center, 50)
            self.all_sprites.add(expl)

        kamikaze_hits = pygame.sprite.groupcollide(self.kamikaze, self.bullets, True, True)
        for hit in kamikaze_hits:
            stats.kills += 100
            sound = pygame.mixer.Sound("music/explosion.wav")
            sound.play()
            sound.set_volume(0.1)

            expl = explosion.Explosion(hit.rect.center, 45)
            self.all_sprites.add(expl)

    def boat_spawn(self):
        if self.starting_position > -5600:  # -5600
            if self.boats_spawned == 0:
                boat_body = aiming_mob_mod.BoatBody(650, -50, 100)
                self.boats.add(boat_body)
                self.all_sprites.add(boat_body)
                boat = aiming_mob_mod.Boat(650, -30, 100+20)
                self.boat_turrets.add(boat)
                self.all_sprites.add(boat)
                self.boats_spawned += 1
            elif self.boats_spawned == 1:
                hits = pygame.sprite.groupcollide(self.boats, self.bullets, False, True)
                for hit in hits:
                    self.boat_hp -= 1
                    sound = pygame.mixer.Sound("music/impact.wav")
                    sound.play()
                    sound.set_volume(0.5)
                    if (self.boat_hp <= 0) and (len(self.boat_turrets) > 0):
                        self.boat_turrets.sprites()[0].kill()
                        self.boats.sprites()[0].kill()
                        sound = pygame.mixer.Sound("music/explosion.wav")
                        sound.play()
                        sound.set_volume(0.1)
                        expl = explosion.Explosion(hit.rect.center, 50)
                        self.all_sprites.add(expl)
                        stats.kills += 200
                        self.boat_hp = 3

        if self.starting_position > -2000:  # drugi boat
            if (self.boats_spawned == 1) and (len(self.boat_turrets) == 0):
                boat_body = aiming_mob_mod.BoatBody(650, -50, 100)
                self.boats.add(boat_body)
                self.all_sprites.add(boat_body)
                boat = aiming_mob_mod.Boat(650, -30, 100+20)
                self.boat_turrets.add(boat)
                self.all_sprites.add(boat)
                self.boats_spawned += 1
            elif self.boats_spawned == 2:
                hits = pygame.sprite.groupcollide(self.boats, self.bullets, False, True)
                for hit in hits:
                    self.boat_hp -= 1
                    sound = pygame.mixer.Sound("music/impact.wav")
                    sound.play()
                    sound.set_volume(0.5)
                    if (self.boat_hp <= 0) and (len(self.boat_turrets) > 0):
                        self.boat_turrets.sprites()[0].kill()
                        self.boats.sprites()[0].kill()
                        sound = pygame.mixer.Sound("music/explosion.wav")
                        sound.play()
                        sound.set_volume(0.1)
                        expl = explosion.Explosion(hit.rect.center, 100)
                        self.all_sprites.add(expl)
                        stats.kills += 200

    def boss_spawn(self):
        if self.starting_position > -900:
            if not self.boss_spawned:
                self.kill_mobs()
                sound = pygame.mixer.Sound("music/warning.wav")
                sound.play()
                boss = boss_mod.Boss(330, -250)
                self.all_sprites.add(boss)
                self.boss.add(boss)
                self.boss_spawned = True
            elif self.boss_spawned:
                hits = pygame.sprite.groupcollide(self.boss, self.bullets, False, True)
                for hit in hits:
                    self.boss_hp -= 1
                    sound = pygame.mixer.Sound("music/impact.wav")
                    sound.play()
                    sound.set_volume(0.5)
                    if self.boss_hp <= 0:
                        self.boss.sprites()[0].kill()
                        sound = pygame.mixer.Sound("music/DeathFlash.flac")
                        sound.play()
                        sound.set_volume(2)
                        expl = explosion.Explosion(hit.rect.center, 200)
                        self.all_sprites.add(expl)
                        stats.kills += 2000
                        self.boss_down_timer = pygame.time.get_ticks()

    def draw_boss_hp(self):
        if self.boss_spawned:
            hp1 = pygame.image.load('graphics/hp1.png').convert_alpha()
            hp1 = pygame.transform.scale(hp1, (5, 10))
            hp0 = pygame.image.load('graphics/hp0.png').convert_alpha()
            hp0 = pygame.transform.scale(hp0, (5, 10))
            for i in range(self.boss_hp):
                # self.screen.blit(hp1, (150 + i * 25, 10))
                self.screen.blit(hp1, (150 + i * 5, 7))
            for i in range(100 - self.boss_hp):
                # self.screen.blit(hp0, (150 + (self.boss_hp + i) * 25, 10))
                self.screen.blit(hp0, (150 + (self.boss_hp + i) * 5, 7))

    def kill_mobs(self):
        for mob in self.mobs:
            expl = explosion.Explosion(mob.rect.center, 100)
            self.all_sprites.add(expl)
            mob.kill()
        for mob in self.boat_turrets:
            expl = explosion.Explosion(mob.rect.center, 100)
            self.all_sprites.add(expl)
            mob.kill()
        for mob in self.boats:
            mob.kill()
        sound = pygame.mixer.Sound("music/explosion.wav")
        sound.play()
        sound.set_volume(0.1)

    def player_pos(self):
        aiming_mob_mod.player_position = [self.player.rect.centerx, self.player.rect.centery]
        boss_mod.player_position = [self.player.rect.centerx, self.player.rect.centery]

    def lives_update(self):
        if not self.player.invulnerable:
            bullet_hits = pygame.sprite.spritecollide(self.player, self.mob_bullets, True)
            if bullet_hits:
                self.player.update()
                self.player.kill()
                self.player = player_mod.Player()
                self.all_sprites.add(self.player)
                self.player_lives -= 1
                expl = explosion.Explosion(bullet_hits[0].rect.center, 100)
                self.all_sprites.add(expl)
                sound = pygame.mixer.Sound("music/explosion.wav")
                sound.play()
                sound.set_volume(0.1)

            collision_mobs = pygame.sprite.spritecollide(self.player, self.mobs, True)  # z mobami
            if collision_mobs:
                self.player.update()
                self.player.kill()
                self.player = player_mod.Player()
                self.all_sprites.add(self.player)
                self.player_lives -= 1
                expl = explosion.Explosion(collision_mobs[0].rect.center, 100)
                self.all_sprites.add(expl)
                sound = pygame.mixer.Sound("music/explosion.wav")
                sound.play()
                sound.set_volume(0.1)

            collision_boss = pygame.sprite.spritecollide(self.player, self.boss, False)  # z bossem
            if collision_boss:
                self.player.update()
                self.player.kill()
                self.player = player_mod.Player()
                self.all_sprites.add(self.player)
                self.player_lives -= 1
                expl = explosion.Explosion(collision_boss[0].rect.center, 100)
                self.all_sprites.add(expl)
                sound = pygame.mixer.Sound("music/explosion.wav")
                sound.play()
                sound.set_volume(0.1)

            # z eksplozjami
            collision_explosions = pygame.sprite.spritecollide(self.player, self.rocket_explosions, False)
            if collision_explosions:
                self.player.update()
                self.player.kill()
                self.player = player_mod.Player()
                self.all_sprites.add(self.player)
                self.player_lives -= 1
                expl = explosion.Explosion(collision_explosions[0].rect.center, 100)
                self.all_sprites.add(expl)
                sound = pygame.mixer.Sound("music/explosion.wav")
                sound.play()
                sound.set_volume(0.1)

            if self.boats_spawned == 1:
                collisions = pygame.sprite.spritecollide(self.player, self.boats, False)  # z łodzią 1
                if collisions:
                    self.boat_hp -= 1
                    self.player.update()
                    self.player.kill()
                    self.player = player_mod.Player()
                    self.all_sprites.add(self.player)
                    self.player_lives -= 1
                    expl = explosion.Explosion(collisions[0].rect.center, 100)
                    self.all_sprites.add(expl)
                    sound = pygame.mixer.Sound("music/explosion.wav")
                    sound.play()
                    sound.set_volume(0.1)
                    if (self.boat_hp <= 0) and (len(self.boat_turrets) > 0):
                        self.boat_turrets.sprites()[0].kill()
                        self.boats.sprites()[0].kill()
                        sound = pygame.mixer.Sound("music/explosion.wav")
                        sound.play()
                        sound.set_volume(0.1)
                        expl = explosion.Explosion(collisions[0].rect.center, 50)
                        self.all_sprites.add(expl)
                        stats.kills += 200

        if self.player_lives == 1:
            self.player.smoke = True
        if self.player_lives <= 0:
            self.lost()

    def end_of_game(self):
        self.empty_groups()
        menu.won()
        stats.kills = 0
        stats.time = 0
        self.running = False

    def lost(self):
        self.empty_groups()
        menu.lost()
        stats.kills = 0
        stats.time = 0
        self.running = False

    def draw_hud(self):
        utils.draw_text(self.screen, str(stats.kills), 50, constants.WIDTH/2 + 10, 10,
                        constants.SCORE_RED)
        utils.draw_text(self.screen, 'Czas: ' + str(round(stats.time / 1000)) + 's', 20, 730, 10, constants.SCORE_RED)
        heart_img = pygame.image.load("graphics/heart.png").convert_alpha()
        heart_img = pygame.transform.scale(heart_img, (30, 30))
        for i in range(self.player_lives):
            self.screen.blit(heart_img, (20 + i * 40, 10))

    def empty_groups(self):
        mob_mod.bullets_group.empty()
        aiming_mob_mod.boat_missiles_group.empty()
        boss_mod.bullets_group.empty()
        bullets.explosions.empty()
        player_mod.smoke_group.empty()
