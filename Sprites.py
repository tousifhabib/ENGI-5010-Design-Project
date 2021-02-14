# Sprite classes for platform game
import pygame as pg
from Settings import *

vector = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, Game):
        pg.sprite.Sprite.__init__(self)
        self.Game = Game
        self.image = pg.Surface((30, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width/2, screen_height/2)
        self.position = vector(screen_width/2, screen_height/2)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

    def jump(self):
        # jump only if standing on platform
        self.rect.x += 1
        collisionCheck = pg.sprite.spritecollide(self, self.Game.platforms, False)
        self.rect.x -= 1
        if collisionCheck:
            self.velocity.y = -15

    def duck(self):
        self.rect.x += 1
        collisionCheck = pg.sprite.spritecollide(self, self.Game.platforms, False)
        self.rect.x -= 1
        if collisionCheck and self.position.y < screen_width - 10:
            self.position.y += 50

    def update(self):
        self.acceleration = vector(0, 0.8)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acceleration.x = -player_acceleration
            if self.velocity.x < 0:
                while self.position.x <= (screen_width * 35) / 100:
                    self.position.x -= int(self.velocity.x)
                    for plat in self.Game.platforms:
                        plat.rect.x -= int(self.velocity.x)
        if keys[pg.K_RIGHT]:
            self.acceleration.x = player_acceleration
            if self.velocity.x > 0:
                while self.position.x >= (screen_width * 65) / 100:
                    self.position.x -= int(self.velocity.x)
                    for plat in self.Game.platforms:
                        plat.rect.x -= int(self.velocity.x)
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
