import pygame as pg
from SettingsTiled import *
from tilemap import *
import math
vector = pg.math.Vector2


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((tilesize, tilesize))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.pos = vector(x, y)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.direction = "Right"
        self.last_update = 0
        self.current_frame = 0
        self.arrow_loop = 0
        self.cooldown = 0
        self.living = True
        self.load_images()


    def load_images(self):
        self.moving_right = [
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(21, 85, 32, 31), (48, 47)),
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(82, 85, 36, 31), (54, 47)),
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(146, 85, 35, 31), (53, 47)),
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(211, 85, 32, 31), (48, 47)),
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(275, 85, 28, 31), (42, 47)),
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(337, 85, 28, 31), (42, 47)),
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(402, 85, 30, 31), (45, 47)),
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(467, 85, 32, 31), (48, 47)),
        ]
        for image in self.moving_right:
            image.set_colorkey(black)

        self.moving_left = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(21, 85, 32, 31), (48, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(82, 85, 36, 31), (48, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(146, 85, 35, 31), (48, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(211, 85, 32, 31), (48, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(275, 85, 28, 31), (48, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(337, 85, 28, 31), (48, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(402, 85, 30, 31), (48, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(467, 85, 32, 31), (48, 47)), True, False),
        ]
        for image in self.moving_left:
            image.set_colorkey(black)

        self.idle_right = [
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(22, 16, 28, 37), (42, 56)),
            pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(86, 15, 28, 38), (42, 57)),
        ]
        for image in self.idle_right:
            image.set_colorkey(black)

        self.idle_left = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(22, 16, 28, 37), (42, 56)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(86, 15, 28, 38), (42, 57)), True, False),
        ]
        for image in self.idle_left:
            image.set_colorkey(black)

        self.single_arrow = [
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(22, 16, 28, 37), (42, 56)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(88, 16, 27, 37), (41, 56)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(152, 11, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(216, 11, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(280, 6, 25, 47), (38, 71)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(344, 11, 33, 42), (50, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(408, 11, 28, 42), (42, 63)),  
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(472, 11, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(24, 75, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(88, 75, 25, 42), (38, 63)),
        ]
        for image in self.single_arrow:
            image.set_colorkey(black)

        self.single_arrow_L = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(22, 16, 28, 37), (42, 56)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(88, 16, 27, 37), (41, 56)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(152, 11, 25, 42), (38, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(216, 11, 25, 42), (38, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(280, 6, 25, 47), (38, 71)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(344, 11, 33, 42), (50, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(408, 11, 28, 42), (42, 63)),  True, False), 
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(472, 11, 25, 42), (38, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(24, 75, 25, 42), (38, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(88, 75, 25, 42), (38, 63)), True, False),
        ]
        for image in self.single_arrow_L:
            image.set_colorkey(black)

        self.held_arrow = [
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(216, 11, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(280, 6, 25, 47), (38, 71)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(344, 11, 33, 42), (50, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(408, 11, 28, 42), (42, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(472, 11, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(24, 75, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(88, 75, 25, 42), (38, 63)),
        ]
        for image in self.held_arrow:
            image.set_colorkey(black)

        self.held_arrow_L = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(216, 11, 25, 42), (38, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(280, 6, 25, 47), (38, 71)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(344, 11, 33, 42), (50, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(408, 11, 28, 42), (42, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(472, 11, 25, 42), (38, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(24, 75, 25, 42), (38, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(88, 75, 25, 42), (38, 63)), True, False),
        ]
        for image in self.held_arrow_L:
            image.set_colorkey(black)

        self.high_single_arrow = [
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(22, 80, 28, 37), (42, 56)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(88, 80, 27, 37), (41, 56)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(152, 75, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(215, 75, 27, 41), (41, 62)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(280, 74, 26, 43), (39, 65)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(343, 70, 27, 47), (41, 71)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(407, 74, 30, 43), (45, 65)),  
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(471, 74, 27, 43), (41, 65)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(23, 138, 26, 43), (39, 65)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(87, 138, 27, 43), (41, 65)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(151, 140, 27, 41), (41, 62)),
        ]
        for image in self.high_single_arrow:
            image.set_colorkey(black)

        self.high_single_arrow_L = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(22, 80, 28, 37), (42, 56)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(88, 80, 27, 37), (41, 56)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(152, 75, 25, 42), (38, 63)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(215, 75, 27, 41), (41, 62)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(280, 74, 26, 43), (39, 65)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(343, 70, 27, 47), (41, 71)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(407, 74, 30, 43), (45, 65)),  True, False), 
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(471, 74, 27, 43), (41, 65)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(23, 138, 26, 43), (39, 65)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(87, 138, 27, 43), (41, 65)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(151, 140, 27, 41), (41, 62)), True, False),
        ]
        for image in self.high_single_arrow_L:
            image.set_colorkey(black)

        self.high_held_arrow = [
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(280, 74, 26, 43), (39, 65)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(343, 70, 27, 47), (41, 71)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(407, 74, 30, 43), (45, 65)),  
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(471, 74, 27, 43), (41, 65)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(23, 138, 26, 43), (39, 65)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(87, 138, 27, 43), (41, 65)),
            pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(151, 140, 27, 41), (41, 62)),
        ]
        for image in self.high_held_arrow:
            image.set_colorkey(black)

        self.high_held_arrow_L = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(280, 74, 26, 43), (39, 65)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(343, 70, 27, 47), (41, 71)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(407, 74, 30, 43), (45, 65)),   True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(471, 74, 27, 43), (41, 65)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(23, 138, 26, 43), (39, 65)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(87, 138, 27, 43), (41, 65)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_high_firing_spritesheet.get_image(151, 140, 27, 41), (41, 62)), True, False),
        ]
        for image in self.high_held_arrow_L:
            image.set_colorkey(black)










            self.low_single_arrow = [
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(22, 208, 28, 37), (42, 56)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(85, 212, 28, 33), (42, 50)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(149, 214, 28, 31), (42, 47)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(215, 214, 27, 31), (41, 47)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(279, 209, 25, 36), (38, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(343, 209, 25, 36), (38, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(407, 204, 25, 41), (38, 62)),  
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(471, 209, 33, 36), (50, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(23, 273, 28, 36), (42, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(87, 273, 25, 36), (38, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(151, 273, 25, 36), (38, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(215, 273, 25, 36), (38, 54)),
        ]
        for image in self.low_single_arrow:
            image.set_colorkey(black)

        self.low_single_arrow_L = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(22, 208, 28, 37), (42, 56)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(85, 212, 28, 33), (42, 50)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(149, 214, 28, 31), (42, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(215, 214, 27, 31), (41, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(279, 209, 25, 36), (38, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(343, 209, 25, 36), (38, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(407, 204, 25, 41), (38, 62)),  True, False), 
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(471, 209, 33, 36), (50, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(23, 273, 28, 36), (42, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(87, 273, 25, 36), (38, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(151, 273, 25, 36), (38, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(215, 273, 25, 36), (38, 54)), True, False),
        ]
        for image in self.low_single_arrow_L:
            image.set_colorkey(black)

        self.low_held_arrow = [
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(343, 209, 25, 36), (38, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(407, 204, 25, 41), (38, 62)),  
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(471, 209, 33, 36), (50, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(23, 273, 28, 36), (42, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(87, 273, 25, 36), (38, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(151, 273, 25, 36), (38, 54)),
            pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(215, 273, 25, 36), (38, 54)),
        ]
        for image in self.low_held_arrow:
            image.set_colorkey(black)

        self.low_held_arrow_L = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(343, 209, 25, 36), (38, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(407, 204, 25, 41), (38, 62)),  True, False), 
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(471, 209, 33, 36), (50, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(23, 273, 28, 36), (42, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(87, 273, 25, 36), (38, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(151, 273, 25, 36), (38, 54)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_low_firing_spritesheet.get_image(215, 273, 25, 36), (38, 54)), True, False),
        ]
        for image in self.low_held_arrow_L:
            image.set_colorkey(black)

        self.dying = [
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(22, 80, 28, 37), (42, 56)),
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(85, 84, 28, 33), (42, 50)),  
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(149, 86, 28, 31), (42, 47)),
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(213, 86, 28, 31), (42, 47)),
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(276, 87, 28, 31), (42, 47)),
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(340, 87, 28, 31), (42, 47)),
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(404, 89, 29, 28), (44, 42)),
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(466, 102, 37, 15), (56, 23)),
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(17, 168, 42, 13), (63, 20)),
            pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(81, 170, 42, 11), (63, 17)),
        ]
        for image in self.dying:
            image.set_colorkey(black)

        self.dying_L = [
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(22, 80, 28, 37), (42, 56)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(85, 84, 28, 33), (42, 50)),  True, False), 
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(149, 86, 28, 31), (42, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(213, 86, 28, 31), (42, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(276, 87, 28, 31), (42, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(340, 87, 28, 31), (42, 47)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(404, 89, 29, 28), (44, 42)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(466, 102, 37, 15), (56, 23)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(17, 168, 42, 13), (63, 20)), True, False),
            pg.transform.flip(pg.transform.smoothscale(self.game.player_death_spritesheet.get_image(81, 170, 42, 11), (63, 17)), True, False),
        ]
        for image in self.dying_L:
            image.set_colorkey(black)

    def jump(self):
        self.rect.y += 1
        collision = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.y -= 1
        if collision:
            self.vel.y = -15
    
    def EnemyCollision(self):
        collision = pg.sprite.spritecollide(self, self.game.enemiesA, False)
        if collision:
            if self.vel.y > 1:
                self.vel.y = -5
                collision[0].kill()
                self.game.score += self.game.multiplier*50
                self.game.multiplier *= 2
            else:
                self.living = False
        collision = pg.sprite.spritecollide(self, self.game.enemiesB, False)
        if collision:
            if self.vel.y > 1:
                self.vel.y = -5
                collision[0].kill()
                self.game.score += self.game.multiplier*100
                self.game.multiplier *= 2
            else:
                self.living = False


    def CoinCollision(self):
        collision = pg.sprite.spritecollide(self, self.game.coins, True)
        if collision:
            self.game.score += 25


    def WallCollision(self, direction):
        if direction == 'x':
            collision = pg.sprite.spritecollide(self, self.game.walls, False)
            if collision:
                if self.vel.x > 0:
                    self.pos.x = collision[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = collision[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x

        elif direction == 'y':
            collision = pg.sprite.spritecollide(self, self.game.walls, False)
            if collision:
                if self.vel.y > 0:
                    self.pos.y = collision[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = collision[0].rect.bottom
                self.vel.y = 0
                self.acc.y = 0
                self.rect.y = self.pos.y
                self.game.multiplier = 1

    def shoot(self, high, low):
        self.arrow = Arrow(self, self.rect.x, self.rect.y + 10, high, low)
        self.game.all_sprites.add(self.arrow)
        self.game.arrows.add(self.arrow)

    def ShootCollide(self):
        collision = pg.sprite.groupcollide(self.game.arrows, self.game.enemiesA, True, True)
        if collision:
            self.game.score += 100
        collision = pg.sprite.groupcollide(self.game.arrows, self.game.enemiesB, True, True)
        if collision:
            self.game.score += 250
        pg.sprite.groupcollide(self.game.arrows, self.game.walls, True, False)

    def update(self):
        now = pg.time.get_ticks()
        if self.living:
            self.acc.x = 0
            self.acc.y = Player_Gravity
            
            keys = pg.key.get_pressed()

            if keys[pg.K_SPACE]:
                keys = pg.key.get_pressed()
                if keys[pg.K_RIGHT]:
                    self.direction = "Right"
                if keys[pg.K_LEFT]:
                    self.direction = "Left"
                if now - self.last_update > 150:
                    self.last_update = now
                    if self.direction == "Right":
                        if self.arrow_loop == 0:
                            self.current_frame = (self.current_frame + 1) % len(self.single_arrow)
                            if (self.current_frame + 1) % (len(self.single_arrow)) == 9:
                                self.shoot(False, False)
                                self.arrow_loop = 1
                                self.current_frame = 0
                            self.image = self.single_arrow[self.current_frame]
                        if self.arrow_loop == 1:
                            self.current_frame = (self.current_frame + 1) % len(self.held_arrow)
                            if (self.current_frame + 1) %  len(self.held_arrow) == 6:
                                self.shoot(False, False)
                            self.image = self.held_arrow[self.current_frame]
                    else:
                        if self.arrow_loop == 0:
                            self.current_frame = (self.current_frame + 1) % len(self.single_arrow_L)
                            if (self.current_frame + 1) % (len(self.single_arrow_L)) == 9:
                                self.shoot(False, False)
                                self.arrow_loop = 1
                                self.current_frame = 0
                            self.image = self.single_arrow_L[self.current_frame]
                        else:
                            self.current_frame = (self.current_frame + 1) % len(self.held_arrow_L)
                            if (self.current_frame + 1) %  len(self.held_arrow_L) == 6:
                                self.shoot(False, False)
                            self.image = self.held_arrow_L[self.current_frame]


                    bottom = self.rect.bottom
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom


            elif keys[pg.K_r]:
                keys = pg.key.get_pressed()
                if keys[pg.K_RIGHT]:
                    self.direction = "Right"
                if keys[pg.K_LEFT]:
                    self.direction = "Left"
                if now - self.last_update > 150:
                    self.last_update = now
                    if self.direction == "Right":
                        if self.arrow_loop == 0:
                            self.current_frame = (self.current_frame + 1) % len(self.high_single_arrow)
                            if (self.current_frame + 1) % (len(self.high_single_arrow)) == 10:
                                self.shoot(True, False)
                                self.arrow_loop = 1
                                self.current_frame = 0
                            self.image = self.high_single_arrow[self.current_frame]
                        if self.arrow_loop == 1:
                            self.current_frame = (self.current_frame + 1) % len(self.high_held_arrow)
                            if (self.current_frame + 1) %  len(self.high_held_arrow) == 6:
                                self.shoot(True, False)
                            self.image = self.high_held_arrow[self.current_frame]
                    else:
                        if self.arrow_loop == 0:
                            self.current_frame = (self.current_frame + 1) % len(self.high_single_arrow_L)
                            if (self.current_frame + 1) % (len(self.high_single_arrow_L)) == 10:
                                self.shoot(True, False)
                                self.arrow_loop = 1
                                self.current_frame = 0
                            self.image = self.high_single_arrow_L[self.current_frame]
                        else:
                            self.current_frame = (self.current_frame + 1) % len(self.high_held_arrow_L)
                            if (self.current_frame + 1) %  len(self.high_held_arrow_L) == 6:
                                self.shoot(True, False)
                            self.image = self.high_held_arrow_L[self.current_frame]


                    bottom = self.rect.bottom
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            elif keys[pg.K_t]:
                keys = pg.key.get_pressed()
                if keys[pg.K_RIGHT]:
                    self.direction = "Right"
                if keys[pg.K_LEFT]:
                    self.direction = "Left"
                if now - self.last_update > 150:
                    self.last_update = now
                    if self.direction == "Right":
                        if self.arrow_loop == 0:
                            self.current_frame = (self.current_frame + 1) % len(self.low_single_arrow)
                            if (self.current_frame + 1) % (len(self.low_single_arrow)) == 11:
                                self.shoot(False, True)
                                self.arrow_loop = 1
                                self.current_frame = 0
                            self.image = self.low_single_arrow[self.current_frame]
                        if self.arrow_loop == 1:
                            self.current_frame = (self.current_frame + 1) % len(self.low_held_arrow)
                            if (self.current_frame + 1) %  len(self.low_held_arrow) == 6:
                                self.shoot(False, True)
                            self.image = self.low_held_arrow[self.current_frame]
                    else:
                        if self.arrow_loop == 0:
                            self.current_frame = (self.current_frame + 1) % len(self.low_single_arrow_L)
                            if (self.current_frame + 1) % (len(self.low_single_arrow_L)) == 11:
                                self.shoot(False, True)
                                self.arrow_loop = 1
                                self.current_frame = 0
                            self.image = self.low_single_arrow_L[self.current_frame]
                        else:
                            self.current_frame = (self.current_frame + 1) % len(self.low_held_arrow_L)
                            if (self.current_frame + 1) %  len(self.low_held_arrow_L) == 6:
                                self.shoot(False, True)
                            self.image = self.low_held_arrow_L[self.current_frame]


                    bottom = self.rect.bottom
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            elif keys[pg.K_LEFT]:
                self.acc.x = -Player_Acceleration
                self.direction = "Left"
                self.arrow_loop = 0 
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.moving_left)
                    bottom = self.rect.bottom
                    self.image = self.moving_left[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                
            elif keys[pg.K_RIGHT]:
                self.acc.x = Player_Acceleration
                self.direction = "Right"
                self.arrow_loop = 0 
                if now - self.last_update > 100:
                    self.last_update = now
                    self.current_frame = (self.current_frame + 1) % len(self.moving_right)
                    bottom = self.rect.bottom
                    self.image = self.moving_right[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom

            else:
                self.arrow_loop = 0 
                if now - self.last_update > 250:
                    self.last_update = now
                    if self.direction == "Right":
                        self.current_frame = (self.current_frame + 1) % len(self.idle_right)
                        bottom = self.rect.bottom
                        self.image = self.idle_right[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                    else:
                        self.current_frame = (self.current_frame + 1) % len(self.idle_left)
                        bottom = self.rect.bottom
                        self.image = self.idle_left[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom



            # Apply friction
            self.acc.x += self.vel.x * Player_Friction
            # Equations of motion
            self.vel.x += self.acc.x
            self.pos.x += self.vel.x + 0.5 * self.acc.x
            self.rect.x = self.pos.x
            self.WallCollision('x')


            # Equations of motion
            self.vel.y += self.acc.y
            self.pos.y += self.vel.y + 0.5 * self.acc.y
            self.rect.y = self.pos.y
            self.WallCollision('y')

            self.EnemyCollision()
            self.CoinCollision()
            self.ShootCollide()
        else:
            self.acc.x = 0
            self.acc.y = Player_Gravity

            if now - self.last_update > 150:
                self.last_update = now
                if self.direction == "Right":
                    self.current_frame = (self.current_frame + 1) % len(self.dying)
                    bottom = self.rect.bottom
                    self.image = self.dying[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    if (self.current_frame + 1) % len(self.dying) == 9:
                        self.current_frame = (self.current_frame + 1) % len(self.dying)
                        bottom = self.rect.bottom
                        self.image = self.dying[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                        self.game.playing = False
                else:
                    self.current_frame = (self.current_frame + 1) % len(self.dying_L)
                    bottom = self.rect.bottom
                    self.image = self.dying_L[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    if (self.current_frame + 1) % len(self.dying) == 9:
                        self.current_frame = (self.current_frame + 1) % len(self.dying_L)
                        bottom = self.rect.bottom
                        self.image = self.dying_L[self.current_frame]
                        self.rect = self.image.get_rect()
                        self.rect.bottom = bottom
                        self.game.playing = False

                if (self.current_frame + 1) % len(self.dying) == 9:
                    self.game.playing = False
                
                # Apply friction
                self.acc.x += self.vel.x * Player_Friction
                # Equations of motion
                self.vel.x += self.acc.x
                self.pos.x += self.vel.x + 0.5 * self.acc.x
                self.rect.x = self.pos.x
                #self.WallCollision('x')


                # Equations of motion
                self.vel.y += self.acc.y
                self.pos.y += self.vel.y + 0.5 * self.acc.y
                self.rect.y = self.pos.y
                #self.WallCollision('y')

                #self.EnemyCollision()
                #self.ShootCollide()



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((tilesize, tilesize))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Enemy_Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.enemy_walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

class enemiesA(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.enemiesA, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.enemyA_spritesheet.get_image(8, 8, 16, 16)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = -1
        self.platform = []

        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.pos = vector(x, y)

    def load_images(self):
        self.moving_left = [
            pg.transform.smoothscale(self.game.enemyA_spritesheet.get_image(8, 104, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemyA_spritesheet.get_image(40, 104, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemyA_spritesheet.get_image(72, 104, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemyA_spritesheet.get_image(104, 104, 16, 12), (32, 24)),
        ]
        for image in self.moving_left:
            image.set_colorkey(black)

        self.moving_right = [
            pg.transform.smoothscale(self.game.enemyA_spritesheet.get_image(8, 40, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemyA_spritesheet.get_image(40, 40, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemyA_spritesheet.get_image(72, 40, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemyA_spritesheet.get_image(104, 40, 16, 12), (32, 24)),
        ]
        for image in self.moving_right:
            image.set_colorkey(black)

    def EnemyCollision(self):
        collision = pg.sprite.spritecollide(self, self.game.enemiesA, False)
        if collision:
            if collision[0] != self:
                if self.vel.x > 0:
                    self.pos.x = collision[1].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = collision[1].rect.right
                self.direction *= -1
                collision[1].direction *= -1
                self.rect.x = self.pos.x


    def WallCollision(self, direction):
        if direction == 'x':
            collision = pg.sprite.spritecollide(self, self.game.enemy_walls, False)
            if collision:
                if self.vel.x > 0:
                    self.pos.x = collision[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = collision[0].rect.right
                self.direction *= -1
                self.rect.x = self.pos.x

        elif direction == 'y':
            collision = pg.sprite.spritecollide(self, self.game.enemy_walls, False)
            if collision:
                if self.vel.y > 0:
                    self.pos.y = collision[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = collision[0].rect.bottom
                self.vel.y = 0
                self.acc.y = 0
                self.rect.y = self.pos.y


    def update(self):
        now = pg.time.get_ticks()

        self.acc.y = Player_Gravity
        self.acc.x = Player_Acceleration / 6 * self.direction * self.game.enemyMod

        if now - self.last_update > 250:
            if self.direction < 0:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_left)
                bottom = self.rect.bottom
                self.image = self.moving_left[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            elif self.direction > 0:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_right)
                bottom = self.rect.bottom
                self.image = self.moving_right[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom




        # Apply friction
        self.acc.x += self.vel.x * Player_Friction
        # Equations of motion
        self.vel.x += self.acc.x
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.x = self.pos.x
        self.WallCollision('x')


        # Equations of motion
        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y = self.pos.y
        self.WallCollision('y')

        self.EnemyCollision()

class enemiesB(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.enemiesB, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.enemyB_spritesheet.get_image(8, 8, 16, 16)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = -1
        self.platform = []

        self.vel = vector(0, 0)
        self.acc = vector(0, 0)
        self.pos = vector(x, y)


    def load_images(self):
        self.moving_right = [
            pg.transform.smoothscale(self.game.enemyB_spritesheet.get_image(41, 33, 17, 21), (26, 32)),
            pg.transform.smoothscale(self.game.enemyB_spritesheet.get_image(73, 38, 17, 15), (26, 23)),
            pg.transform.smoothscale(self.game.enemyB_spritesheet.get_image(107, 38, 15, 21), (23, 32)),
        ]
        for image in self.moving_right:
            image.set_colorkey(black)

        self.moving_left = [
            pg.transform.smoothscale(self.game.enemyB_spritesheet.get_image(38, 97, 17, 21), (26, 32)),
            pg.transform.smoothscale(self.game.enemyB_spritesheet.get_image(70, 102, 17, 15), (26, 23)),
            pg.transform.smoothscale(self.game.enemyB_spritesheet.get_image(102, 102, 15, 21), (23, 32)),
        ]
        for image in self.moving_left:
            image.set_colorkey(black)



    def WallCollision(self, direction):
        if direction == 'x':
            collision = pg.sprite.spritecollide(self, self.game.enemy_walls, False)
            if collision:
                if self.vel.x > 0:
                    self.pos.x = collision[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = collision[0].rect.right
                self.direction *= -1
                self.rect.x = self.pos.x

        elif direction == 'y':
            collision = pg.sprite.spritecollide(self, self.game.enemy_walls, False)
            if collision:
                if self.vel.y > 0:
                    self.pos.y = collision[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = collision[0].rect.bottom
                self.vel.y = 0
                self.acc.y = 0
                self.rect.y = self.pos.y


    def update(self):
        now = pg.time.get_ticks()

        self.acc.y = 0
        self.acc.x = Player_Acceleration / 6 * self.direction * self.game.enemyMod

        if now - self.last_update > 250:
            if self.direction < 0:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_left)
                bottom = self.rect.bottom
                self.image = self.moving_left[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            elif self.direction > 0:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_right)
                bottom = self.rect.bottom
                self.image = self.moving_right[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom




        # Apply friction
        self.acc.x += self.vel.x * Player_Friction
        # Equations of motion
        self.vel.x += self.acc.x
        self.pos.x += self.vel.x + 0.5 * self.acc.x
        self.rect.x = self.pos.x
        self.WallCollision('x')


class Arrow(pg.sprite.Sprite):
    def __init__(self, player, x, y, high, low):
        pg.sprite.Sprite.__init__(self)
        self.direction = player.direction

        self.image = pg.image.load('Pixel Art Trees\Archer\Arrow.png').convert()
        self.image = pg.transform.scale(self.image, (20, 10))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.acc = vector(0, 0)
        self.vel = vector(0, 0)
        if low:
            self.pos = vector(x + 25, y)
        else:
            self.pos = vector(x, y)
        self.rect.y = y
        self.rect.x = x

        if self.direction == "Right" and high:
            self.vel.x = 20
        elif self.direction == "Left" and high:
            self.vel.x = -20
        elif self.direction == "Right":
            self.vel.x = 20
        else:
            self.vel.x = -20

        if high:
            self.vel.y = -math.sqrt(60)
        else:
            self.vel.y = 0

    def update(self):
        self.acc.y = Player_Gravity

        #self.vel.x += self.acc.x
        self.pos.x += self.vel.x# + 0.5 * self.acc.x
        self.rect.x = self.pos.x

        self.vel.y += self.acc.y
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.rect.y = self.pos.y

        self.image = pg.transform.rotate(self.image, -math.tan(self.vel.y / self.vel.x))

        # kill if it moves off the top of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.coins, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.coin_spritesheet.get_image(1, 0, 14, 16)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_images(self):
        self.coin = [
            self.game.coin_spritesheet.get_image(1, 0, 14, 16),
            self.game.coin_spritesheet.get_image(19, 0, 10, 16),
            self.game.coin_spritesheet.get_image(37, 0, 6, 16),
            self.game.coin_spritesheet.get_image(51, 0, 10, 16),
            self.game.coin_spritesheet.get_image(65, 0, 13, 16),
        ]
        for image in self.coin:
            image.set_colorkey(black)

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.coin)
            self.image = self.coin[self.current_frame]