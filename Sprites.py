# Sprite classes for platform game
import pygame as pg
from Settings import *
import random

vector = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()
    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width // 6, height // 7))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, Game):
        pg.sprite.Sprite.__init__(self)
        self.Game = Game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idle_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.position = vector(screen_width / 2, screen_height / 2)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)

    def load_images(self):
        self.idle_frames = [self.Game.spritesheet.get_image(1,1,377,410),
                            self.Game.spritesheet.get_image(380,1,377,410),
                            self.Game.spritesheet.get_image(759,1,377,410),
                            self.Game.spritesheet.get_image(1138,1,377,410),
                            self.Game.spritesheet.get_image(1517,1,377,410)]

        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
        self.walking_frames_r = [self.Game.spritesheet.get_image(1896,1,410,431), 
                                 self.Game.spritesheet.get_image(2308,1,410,431),
                                 self.Game.spritesheet.get_image(1,434,410,431),
                                 self.Game.spritesheet.get_image(413,434,410,431),
                                 self.Game.spritesheet.get_image(825,434,410,431)]
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame, True, False))
        self.jumping_frames = [self.Game.spritesheet.get_image(688, 439, 402, 436),
                               self.Game.spritesheet.get_image(688, 877, 402, 436),
                               self.Game.spritesheet.get_image(1092, 439, 402, 436)]
        for frame in self.jumping_frames:
            frame.set_colorkey(BLACK)
        


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
            self.position.y = collisionCheck[0].rect.bottom + 60

    def update(self):
        self.animate()
        self.acceleration = vector(0, 0.8)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acceleration.x = -player_acceleration
            if self.acceleration.x < 0:
                while self.position.x < (screen_width * 35) / 100:
                    self.position.x -= self.velocity.x
                    for plat in self.Game.platforms:
                        plat.rect.x -= int(self.velocity.x)
                        self.position.x += 0.01
                    for enemy in self.Game.enemiesA:
                        enemy.position.x += -int(self.velocity.x)
                    for enemy in self.Game.enemiesB:
                        enemy.position.x += -int(self.velocity.x)

        if keys[pg.K_RIGHT]:
            self.acceleration.x = player_acceleration
            if self.acceleration.x > 0:
                while self.position.x > (screen_width * 65) / 100:
                    self.position.x -= self.velocity.x
                    for plat in self.Game.platforms:
                        plat.rect.x -= int(self.velocity.x)
                        self.position.x -= 0.01
                    for enemy in self.Game.enemiesA:
                        enemy.position.x += -int(self.velocity.x)
                    for enemy in self.Game.enemiesB:
                        enemy.position.x += -int(self.velocity.x)

        # Apply friction
        self.acceleration.x += self.velocity.x * player_friction
        # Equations of motion
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration

        self.rect.midbottom = self.position
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.velocity.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.velocity.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image(1,2414,860,302)
        self.image = pg.transform.scale(self.image, (200, 20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class enemiesA(pg.sprite.Sprite):
    def __init__(self, x, y, Game):
        pg.sprite.Sprite.__init__(self)
        self.Game = Game
        self.image = pg.image.load('img/LittleBadGuy.png').convert()
        self.image = pg.transform.scale(self.image, (40, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.position = vector(x, y)

    def update(self):

        self.acceleration = vector(0, 0.8)
        self.acceleration.x = player_acceleration / 5



        # Apply friction
        self.acceleration.x += self.velocity.x * player_friction
        # Equations of motion
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration

        self.rect.midbottom = self.position

class enemiesB(pg.sprite.Sprite):
    def __init__(self, x, y, Game):
        pg.sprite.Sprite.__init__(self)
        self.Game = Game
        self.image = pg.Surface((15, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        self.position = vector(x, y)
        self.turntracker = 0
        self.switchDirection = 0

    def update(self):

        self.acceleration = vector(0, 0)

        if self.turntracker >= 200:
            self.switchDirection = 1
        if self.turntracker <= 0:
            self.switchDirection = 0

        if self.switchDirection == 0:
            self.acceleration.x = player_acceleration / 3
        else:
            self.acceleration.x = -player_acceleration / 3



        # Apply friction
        self.acceleration.x += self.velocity.x * player_friction
        # Equations of motion
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.1:
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration
        self.turntracker += self.velocity.x + 0.5 * self.acceleration.x

        self.rect.midbottom = self.position