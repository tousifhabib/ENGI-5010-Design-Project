import pygame as pg
import random
from Settings import *


class Game:
    def __init__(self):
        # Initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def newGame(self):
        # Starts new game
        self.all_sprites = pg.sprite.Group()

    def consoleRunner(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game loop update
        self.all_sprites.update()

    def events(self):
        # Game loop events
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT():
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game loop draw
        self.screen.fill(YELLOW)
        self.all_sprites.draw(self.screen)
        # After drawing flip display
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_game_over_screen(self):
        pass


game = Game()
game.show_start_screen()
while game.running:
    game.newGame()
    game.show_game_over_screen()

pg.quit()