# Sprite classes for platform game
import pygame as pg
from Settings import *
vector = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, screen_height/2)
        self.position = vector(screen_width/2, screen_height/2)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

    def update(self):
        self.acceleration = vector(0, 0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acceleration.x = -player_acceleration
        if keys[pg.K_RIGHT]:
            self.acceleration.x = player_acceleration
        if keys[pg.K_UP]:
            self.velocity.y = -10
        # Apply friction
        self.acceleration.x += self.velocity.x * player_friction
        # Equations of motion
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        self.rect.midbottom = self.position



class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
