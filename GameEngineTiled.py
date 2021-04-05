#ENGI 5010 Project
import pygame as pg
import sys
from os import path
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
        self.font_name = pg.font.match_font(FONT)
        self.load_data()

    def load_data(self):
        Folder = path.dirname(__file__)
        img_Folder = path.join(Folder, 'Pixel Art Trees')
        map_Folder = path.join(Folder, 'Working on Tile Maps')
        #self.Map = Map(path.join(Folder, 'map.txt'))
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
        
        self.enemy_spritesheet = Spritesheet(path.join(img_Folder, ENEMY_SPRITESHEET))
        self.player_running_spritesheet = Spritesheet(path.join(img_Folder, PLAYER_RUNNING_SPRITESHEET))
        self.player_firing_spritesheet = Spritesheet(path.join(img_Folder, PLAYER_FIRING_SPRITESHEET))
        

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemiesA = pg.sprite.Group()
        self.enemy_walls = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        #for row, tiles in enumerate(self.Map.Map):
            #for col, tile in enumerate(tiles):
                #if tile == '1':
                    #Wall(self, col, row)
                #if tile == 'P':
                    #self.player = Player(self, col, row)
        
        for obj in self.Map.tmxdata.objects:
            if obj.name == 'Player':
                self.player = Player(self, 2*obj.x, 2*obj.y)
            if obj.name == 'Wall':
                Obstacle(self, 2*obj.x, 2*obj.y, 2*obj.width, 2*obj.height)
            if obj.name == 'EnemyA':
                enemiesA(self, 2*obj.x, 2*obj.y)
            if obj.name == 'Enemy Wall':
                Enemy_Obstacle(self, 2*obj.x, 2*obj.y, 2*obj.width, 2*obj.height)


        self.camera = Camera(self.Map.width, self.Map.height)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
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

                if event.key == pg.K_SPACE:
                    self.player.shoot()

            

    def show_start_screen(self):
        self.start = pg.image.load('Pixel Art Trees/FreeCuteTileset/Mockup2x.png')
        self.start = pg.transform.scale(self.start, (640, 384))
        self.screen.blit(self.start, (0, 0))
        self.draw_text(TITLE, 48, black, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Use the arrow keys to move and jump!", 22, black, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to start", 22, black, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait()

    def show_go_screen(self):
        pass

    def wait(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()