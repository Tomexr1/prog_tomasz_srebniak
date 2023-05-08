import pygame, constants, text, mob_mod, player_mod, menu


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

    def update(self):
        self.bullets.add(self.player.bullets)
        self.all_sprites.add(self.player.bullets)
        self.mob_bullets.add(mob_mod.bullets_group)
        self.all_sprites.add(mob_mod.bullets_group)

        self.all_sprites.update()

        self.hits()
        self.lives_update()

        if pygame.key.get_pressed()[pygame.K_p]:
            self.paused()

    def paused(self):
        print("paused")
        text.draw_text(self.screen, "Zatrzymano", 30, 400, 120)
        text.draw_text(self.screen, "Naciśnij [p] aby wznowić", 18, 400, 250)
        text.draw_text(self.screen, "Naciśnij [ESC] aby wyjść z gry", 18, 400, 300)
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = False
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        pause = False
                        self.kill_all_sprites()

            pygame.display.update()
            self.clock.tick(15)

    def draw(self):
        self.all_sprites.draw(self.screen)
        self.mob_draw()

    def add_mob(self, spawn_time=100):
        now = pygame.time.get_ticks()
        if now - self.mob_time > spawn_time:
            mob = mob_mod.Mob(constants.WIDTH/2 + 10, 100, constants.WIDTH/2, 100)
            mob2 = mob_mod.Mob(constants.WIDTH / 4, 100, constants.WIDTH / 2, 100)
            mob3 = mob_mod.Mob(constants.WIDTH / 4 * 3, 100, constants.WIDTH / 2, 100)
            mob4 = mob_mod.Mob(constants.WIDTH / 3 * 2, 100, constants.WIDTH / 2, 100)
            self.all_sprites.add(mob2)
            self.mobs.add(mob2)
            self.all_sprites.add(mob3)
            self.mobs.add(mob3)
            self.all_sprites.add(mob4)
            self.mobs.add(mob4)

            self.all_sprites.add(mob)
            self.mobs.add(mob)
            self.mob_time = now

    def mob_draw(self):
        if -5800 < self.starting_position < -5791:
            self.add_mob()

    def hits(self):
        mob_hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        for hit in mob_hits:
            pass

    def lives_update(self):
        bullet_hits = pygame.sprite.spritecollide(self.player, self.mob_bullets, True)
        for hit in bullet_hits:
            self.player.update()
            self.player.kill()
            self.player = player_mod.Player()
            self.all_sprites.add(self.player)
            self.player_lives -= 1
            print(self.player_lives)

        collision = pygame.sprite.spritecollide(self.player, self.mobs, True)
        for hit in collision:
            self.player.update()
            self.player.kill()
            self.player = player_mod.Player()
            self.all_sprites.add(self.player)
            self.player_lives -= 1
            print(self.player_lives)

        if self.player_lives == 0:
            self.running = False

    def end_of_game(self):
        menu.won()
        Level.running = False

    def kill_all_sprites(self):
        self.all_sprites.empty()
        self.mobs.empty()
        self.bullets.empty()
        self.mob_bullets.empty()
        mob_mod.bullets_group.empty()
        self.player.bullets.empty()
