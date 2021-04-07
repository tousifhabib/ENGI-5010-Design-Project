#ENGI 5010 Project
import pygame as pg
import sys
from os import path

from pygame.constants import MOUSEBUTTONUP
from SettingsTiled import *
from SpritesTiled import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.timer = 100
        self.score = 0
        self.multiplier = 1
        self.victory = False
        self.enemyMod = 1
        self.font_name = pg.font.match_font(FONT)
        self.load_data()

    def load_data(self):
        Folder = path.dirname(__file__)
        img_Folder = path.join(Folder, 'Pixel Art Trees')                
        map_Folder = path.join(Folder, 'Working on Tile Maps')
        self.Map = Tilemap(path.join(map_Folder, 'CuteTree.tmx'))
        self.map_img = self.Map.make_map()
        self.map_img = pg.transform.scale(self.map_img, (2*self.Map.width, 2*self.Map.height))
        self.map_img.set_colorkey(black)
        self.map_rect = self.map_img.get_rect()
        self.BG1 = pg.image.load('Pixel Art Trees/FreeCuteTileset/BG1.png')
        self.BG1 = pg.transform.smoothscale(self.BG1, (640, 384))
        self.BG2 = pg.image.load('Pixel Art Trees/FreeCuteTileset/BG2.png')
        self.BG2 = pg.transform.smoothscale(self.BG2, (640, 384))
        self.BG3 = pg.image.load('Pixel Art Trees/FreeCuteTileset/BG3.png')
        self.BG3 = pg.transform.smoothscale(self.BG3, (640, 384))
        
        self.enemyA_spritesheet = Spritesheet(path.join(img_Folder, ENEMYA_SPRITESHEET))
        self.enemyB_spritesheet = Spritesheet(path.join(img_Folder, ENEMYB_SPRITESHEET))
        self.player_running_spritesheet = Spritesheet(path.join(img_Folder, PLAYER_RUNNING_SPRITESHEET))
        self.player_firing_spritesheet = Spritesheet(path.join(img_Folder, PLAYER_FIRING_SPRITESHEET))
        self.player_high_firing_spritesheet = Spritesheet(path.join(img_Folder, PLAYER_HIGH_FIRING_SPRITESHEET))
        self.player_low_firing_spritesheet = Spritesheet(path.join(img_Folder, PLAYER_LOW_FIRING_SPRITESHEET))
        self.player_death_spritesheet = Spritesheet(path.join(img_Folder, PLAYER_DEATH_SPRITESHEET))
        self.coin_spritesheet = Spritesheet(path.join(img_Folder, COIN_SPRITESHEET))
                     

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemiesA = pg.sprite.Group()
        self.enemiesB = pg.sprite.Group()
        self.enemy_walls = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        
        for obj in self.Map.tmxdata.objects:
            if obj.name == 'Player':
                self.player = Player(self, 2*obj.x, 2*obj.y)
            if obj.name == 'Wall':
                Obstacle(self, 2*obj.x, 2*obj.y, 2*obj.width, 2*obj.height)
            if obj.name == 'EnemyA':
                enemiesA(self, 2*obj.x, 2*obj.y)
            if obj.name == 'EnemyB':
                enemiesB(self, 2*obj.x, 2*obj.y)
            if obj.name == 'Enemy Wall':
                Enemy_Obstacle(self, 2*obj.x, 2*obj.y, 2*obj.width, 2*obj.height)
            if obj.name == 'Coin':
                Coin(self, 2*obj.x, 2*obj.y)


        self.camera = Camera(self.Map.width, self.Map.height)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.timer -= (4/FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        if self.player.pos.y > HEIGHT:
            self.playing = False
        if self.timer <= 0:
            self.playing = False
        if self.player.pos.x > 10000:
            self.victory = True
            self.playing = False

    def draw_grid(self):
        for x in range(0, WIDTH, tilesize):
            pg.draw.line(self.screen, lightGray, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, tilesize):
            pg.draw.line(self.screen, lightGray, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BackColor)
        #self.draw_grid()
        self.screen.blit(self.BG1, (0, 0))
        self.screen.blit(self.BG2, (0, 0))
        self.screen.blit(self.BG3, (0, 0))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for s in self.all_sprites:
            self.screen.blit(s.image, self.camera.apply(s))
        self.draw_text(str(self.score), 12, black, WIDTH - 20, 0)
        self.draw_text(str(int(self.timer)), 12, black, WIDTH - 20, 15)

        pg.display.flip()
    
    def draw_text(self, text, size, colour, x, y):
        #Add text to screen
        font = pg.font.Font(self.font_name, size)
        ScreenText = font.render(text, True, colour)
        text_rect = ScreenText.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(ScreenText, text_rect)

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:     
                if event.key == pg.K_UP:
                    self.player.jump()

    def show_start_screen(self):
        self.start = pg.image.load('Pixel Art Trees/FreeCuteTileset/Mockup2x.png')
        self.start = pg.transform.scale(self.start, (640, 384))
        self.screen.blit(self.start, (0, 0))
        self.back_border = pg.Surface((110, 60))
        self.back_border.fill(black)
        self.screen.blit(self.back_border, (WIDTH / 2 - 55, 80))
        self.back = pg.Surface((100, 50))
        self.back.fill(red)
        self.screen.blit(self.back, (WIDTH / 2 - 50, 85))
        self.draw_text("Settings", 16, black, WIDTH/2, 100)
        self.draw_text(TITLE, 24, black, WIDTH / 2, 5)
        self.draw_text("Use the arrow keys to move and jump!", 16, black, WIDTH / 2, 30)
        self.draw_text("Press any key to start...", 16, black, WIDTH / 2, 45)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    waiting = False
                elif event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    if (WIDTH / 2 - 55) < pos[0] < (WIDTH / 2 + 55):
                        if 80 < pos[1] < 140:
                            self.settings()
                            self.start = pg.image.load('Pixel Art Trees/FreeCuteTileset/Mockup2x.png')
                            self.start = pg.transform.scale(self.start, (640, 384))
                            self.screen.blit(self.start, (0, 0))
                            self.back_border = pg.Surface((110, 60))
                            self.back_border.fill(black)
                            self.screen.blit(self.back_border, (WIDTH / 2 - 55, 80))
                            self.back = pg.Surface((100, 50))
                            self.back.fill(red)
                            self.screen.blit(self.back, (WIDTH / 2 - 50, 85))
                            self.draw_text("Settings", 16, black, WIDTH/2, 100)
                            self.draw_text(TITLE, 24, black, WIDTH / 2, 5)
                            self.draw_text("Use the arrow keys to move and jump!", 16, black, WIDTH / 2, 30)
                            self.draw_text("Press any key to start...", 16, black, WIDTH / 2, 45)
                            pg.display.flip()

            

    def settings(self):
        self.screen.fill(black)
        self.start = pg.image.load('Pixel Art Trees/FreeCuteTileset/Mockup2x.png')
        self.start = pg.transform.scale(self.start, (640, 384))
        self.screen.blit(self.start, (0, 0))
        self.draw_text("Select Enemy Speed modifier:", 22, black, WIDTH/2, 5)

        self.one_back = pg.Surface((110, 70))
        self.one_back.fill(black)
        self.screen.blit(self.one_back, (WIDTH/2 - 145, 55))
        self.two_back = pg.Surface((110, 70))
        self.two_back.fill(black)
        self.screen.blit(self.two_back, (WIDTH/2 + 20, 55))
        self.four_back = pg.Surface((110, 70))
        self.four_back.fill(black)
        self.screen.blit(self.four_back, (WIDTH/2 - 145, 135))
        self.eight_back = pg.Surface((110, 70))
        self.eight_back.fill(black)
        self.screen.blit(self.eight_back, (WIDTH/2 + 20, 135))

        self.one = pg.Surface((100, 60))
        self.one.fill(red)
        self.screen.blit(self.one, (WIDTH/2 - 140, 60))
        self.two = pg.Surface((100, 60))
        self.two.fill(red)
        self.screen.blit(self.two, (WIDTH/2 + 25, 60))
        self.four = pg.Surface((100, 60))
        self.four.fill(red)
        self.screen.blit(self.four, (WIDTH/2 - 140, 140))
        self.eight = pg.Surface((100, 60))
        self.eight.fill(red)
        self.screen.blit(self.eight, (WIDTH/2 + 25, 140))

        self.draw_text("1x", 16, black, WIDTH/2 - 90, 80)
        self.draw_text("2x", 16, black, WIDTH/2 + 75, 80)
        self.draw_text("4x", 16, black, WIDTH/2 - 90, 160)
        self.draw_text("8x", 16, black, WIDTH/2 + 75, 160)
        pg.display.flip()

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                elif event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    if (WIDTH/2 - 140) < pos[0] < (WIDTH/2 - 30):
                        if 60 < pos[1] < 120:
                            self.enemyMod = 1
                            waiting = False
                        elif 140 < pos[1] < 200:
                            self.enemyMod = 2
                            waiting = False
                    elif (WIDTH/2 + 25) < pos[0] < (WIDTH/2 + 135):
                        if 60 < pos[1] < 120:
                            self.enemyMod = 4
                            waiting = False
                        elif 140 < pos[1] < 200:
                            self.enemyMod = 8
                            waiting = False



    def show_go_screen(self):
        self.end = pg.image.load('Pixel Art Trees/FreeCuteTileset/Mockup2x.png')
        self.end = pg.transform.scale(self.start, (640, 384))
        self.screen.blit(self.start, (0, 0))
        self.draw_text("Your Score: " + str(self.score), 22, black, WIDTH/2, 5)
        self.draw_text("Select new speed?", 22, black, WIDTH/2, 25)

        self.one_back = pg.Surface((110, 70))
        self.one_back.fill(black)
        self.screen.blit(self.one_back, (WIDTH/2 - 145, 55))
        self.two_back = pg.Surface((110, 70))
        self.two_back.fill(black)
        self.screen.blit(self.two_back, (WIDTH/2 + 20, 55))
        self.four_back = pg.Surface((110, 70))
        self.four_back.fill(black)
        self.screen.blit(self.four_back, (WIDTH/2 - 145, 135))
        self.eight_back = pg.Surface((110, 70))
        self.eight_back.fill(black)
        self.screen.blit(self.eight_back, (WIDTH/2 + 20, 135))

        self.one = pg.Surface((100, 60))
        self.one.fill(red)
        self.screen.blit(self.one, (WIDTH/2 - 140, 60))
        self.two = pg.Surface((100, 60))
        self.two.fill(red)
        self.screen.blit(self.two, (WIDTH/2 + 25, 60))
        self.four = pg.Surface((100, 60))
        self.four.fill(red)
        self.screen.blit(self.four, (WIDTH/2 - 140, 140))
        self.eight = pg.Surface((100, 60))
        self.eight.fill(red)
        self.screen.blit(self.eight, (WIDTH/2 + 25, 140))

        self.draw_text("1x", 16, black, WIDTH/2 - 90, 80)
        self.draw_text("2x", 16, black, WIDTH/2 + 75, 80)
        self.draw_text("4x", 16, black, WIDTH/2 - 90, 160)
        self.draw_text("8x", 16, black, WIDTH/2 + 75, 160)
        pg.display.flip()

        self.timer = 100
        self.score = 0

        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                elif event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    if (WIDTH/2 - 140) < pos[0] < (WIDTH/2 - 30):
                        if 60 < pos[1] < 120:
                            self.enemyMod = 1
                            waiting = False
                        elif 140 < pos[1] < 200:
                            self.enemyMod = 2
                            waiting = False
                    elif (WIDTH/2 + 25) < pos[0] < (WIDTH/2 + 135):
                        if 60 < pos[1] < 120:
                            self.enemyMod = 4
                            waiting = False
                        elif 140 < pos[1] < 200:
                            self.enemyMod = 8
                            waiting = False



# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()