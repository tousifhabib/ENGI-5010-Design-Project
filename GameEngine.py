import pygame as pg
import random
from Settings import *
from Sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in platform_list:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        collision = pg.sprite.spritecollide(self.player, self.platforms, False)
        # Collision check
        if self.player.velocity.y > 0:
            if collision:
                self.player.position.y = collision[0].rect.top
                self.player.velocity.y = 0
                print(self.player.position.x)

        if self.player.velocity.x>0:
            if self.player.rect.x >= (screen_width * 55) / 100:
                self.player.position.x -= int(self.player.velocity.x)
                for plat in self.platforms:
                    plat.rect.x -= int((self.player.velocity.x))

        if self.player.velocity.x<0:
            if self.player.rect.x <= (screen_width*45) / 10:
                self.player.position.x -= int(self.player.velocity.x)
                for plat in self.platforms:
                    plat.rect.x -= int((self.player.velocity.x))

        # if self.player.velocity.x<0:
        #     if self.player.rect.bottom <= (self.player.position.x - screen_width) / 4:
        #         self.player.position.x -= int(self.player.velocity.x)
        #         for plat in self.platforms:
        #             plat.rect.x -= int(abs((self.player.velocity.x)))

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                if event.key == pg.K_DOWN:
                    self.player.duck()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pg.quit()