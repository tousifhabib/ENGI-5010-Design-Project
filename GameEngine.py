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
        self.player = Player()
        self.all_sprites.add(self.player)
        platform1 = Platform(0, screen_height - 40, screen_width, 40)
        platform2 = Platform(100, screen_height - 200, 200, 20)
        platform3 = Platform(200, screen_height - 100, 200, 20)
        platform4 = Platform(300, screen_height - 350, 200, 20)
        self.all_sprites.add(platform1, platform2, platform3, platform4)
        self.platforms.add(platform1, platform2, platform3, platform4)
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
        if collision:
            self.player.position.y = collision[0].rect.top
            self.player.velocity.y = 0

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

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