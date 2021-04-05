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
        self.invulnerable = 0
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
            pg.transform.flip(pg.transform.smoothscale(self.game.player_running_spritesheet.get_image(86, 15, 28, 38), (42, 56)), True, False),
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
        ]
        for image in self.single_arrow:
            image.set_colorkey(black)

        self.held_arrow = [
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(24, 203, 25, 42), (38, 42)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(88, 198, 25, 47), (38, 47)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(152, 203, 33, 42), (50, 42)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(216, 203, 28, 42), (42, 42)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(280, 203, 25, 42), (38, 42)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(344, 203, 25, 42), (38, 42)),
        ]
        for image in self.held_arrow:
            image.set_colorkey(black)

        self.end_arrow = [
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(88, 75, 25, 42), (38, 63)),
            pg.transform.smoothscale(self.game.player_firing_spritesheet.get_image(1152, 80, 27, 37), (41, 56)),
        ]



    def jump(self):
        now = pg.time.get_ticks()
        self.rect.y += 1
        collision = pg.sprite.spritecollide(self, self.game.walls, False)
        self.rect.y -= 1
        if collision:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(jumping_frames_R)
                bottom = self.rect.bottom
                self.image = jumping_frames_R[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
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
                self.game.playing = False

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

    def update(self):
        now = pg.time.get_ticks()
        self.acc.x = 0
        self.acc.y = Player_Gravity
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -Player_Acceleration
            self.direction = "Left"
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_left)
                bottom = self.rect.bottom
                self.image = self.moving_left[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        if keys[pg.K_RIGHT]:
            self.acc.x = Player_Acceleration
            self.direction = "Right"
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_right)
                bottom = self.rect.bottom
                self.image = self.moving_right[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #if keys[pg.K_SPACE]:
            #if now - self.last_update > 350:
                #self.last_update = now
                #self.current_frame = (self.current_frame + 1) % len(self.single_arrow)
                #bottom = self.rect.bottom
                #self.image = self.single_arrow[self.current_frame]
                #self.rect = self.image.get_rect()
                #self.rect.bottom = bottom

        if now - self.last_update > 450:
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
        self.image = self.game.enemy_spritesheet.get_image(8, 8, 16, 16)
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
            pg.transform.smoothscale(self.game.enemy_spritesheet.get_image(8, 104, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemy_spritesheet.get_image(40, 104, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemy_spritesheet.get_image(72, 104, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemy_spritesheet.get_image(104, 104, 16, 12), (32, 24)),
        ]
        for image in self.moving_left:
            image.set_colorkey(black)

        self.moving_right = [
            pg.transform.smoothscale(self.game.enemy_spritesheet.get_image(8, 40, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemy_spritesheet.get_image(40, 40, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemy_spritesheet.get_image(72, 40, 16, 12), (32, 24)),
            pg.transform.smoothscale(self.game.enemy_spritesheet.get_image(104, 40, 16, 12), (32, 24)),
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
        self.acc.x = Player_Acceleration / 6 * self.direction

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

class Arrow(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.arrows, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = pg.Rect(x, y, 5, 2)
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y