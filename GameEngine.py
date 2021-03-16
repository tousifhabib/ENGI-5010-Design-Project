import pygame as pg
import random
from Settings import *
from Sprites import *
from os import path
import math

class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.timer = 600
        self.running = True
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, "img")
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.background1 = pg.image.load('img/Background.jpg').convert()
        self.background1 = pg.transform.scale(self.background1, (screen_width, screen_height))
        self.backgroundPosition1 = vector(0, 0)
        self.background2 = pg.image.load('img/Background.jpg').convert()
        self.background2 = pg.transform.scale(self.background2, (screen_width, screen_height))
        self.backgroundPosition2 = vector(screen_width, 0)


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
            self.timer -= (1/60)
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
        # Update background
        if self.player.acceleration.x > 0:
            if self.player.position.x > (screen_width * 65) / 100:
                self.backgroundPosition1.x -= 1
                self.backgroundPosition2.x -= 1
                if self.backgroundPosition1.x < -screen_width:
                    self.backgroundPosition1.x += (2*screen_width)
                if self.backgroundPosition2.x < -screen_width:
                    self.backgroundPosition2.x += (2*screen_width)

        elif self.player.acceleration.x < 0:
            if self.player.position.x < (screen_width * 35) / 100:
                self.backgroundPosition1.x += 1
                self.backgroundPosition2.x += 1
        # Game Over Check
        if self.player.position.y > screen_height or self.timer <= 0:
            self.playing = False

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
        self.screen.blit(self.background1, self.backgroundPosition1)
        self.screen.blit(self.background2, self.backgroundPosition2)  
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.player.position.x), 12, WHITE, screen_width - 40, 20)
        self.draw_text(str(self.backgroundPosition1.x), 12, WHITE, screen_width - 40, 40)
        self.draw_text(str(self.backgroundPosition2.x), 12, WHITE, screen_width - 40, 60)
        self.draw_text(str(int(self.timer)), 12, WHITE, screen_width - 40, 80)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(SPLASH)
        self.draw_text(TITLE, 48, WHITE, screen_width / 2, screen_height / 4)
        self.draw_text("Use the arrow keys to move and jump!", 22, WHITE, screen_width / 2, screen_height / 2)
        self.draw_text("Press any key to start", 22, WHITE, screen_width / 2, screen_height * 3 / 4)
        pg.display.flip()
        self.wait()
        
    def show_go_screen(self):
        # game over/continue
        if self.running == True:
            self.screen.fill(SPLASH)
            self.draw_text("Game Over", 48, WHITE, screen_width / 2, screen_height / 4)
            pg.display.flip()
            self.timer = 600
            pg.time.delay(1000)
            self.draw_text("Press any key to try again", 22, WHITE, screen_width / 2, screen_height * 3 / 4)
            pg.display.flip()
            pg.event.clear()
            self.wait()

    def draw_text(self, text, size, colour, x, y):
        #Add text to screen
        font = pg.font.Font(self.font_name, size)
        ScreenText = font.render(text, True, colour)
        text_rect = ScreenText.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(ScreenText, text_rect)

    def wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pg.KEYUP:
                    waiting = False

game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pg.quit()
