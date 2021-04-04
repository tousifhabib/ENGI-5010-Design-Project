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
        self.attacking = False
        self.current_frame = 0
        self.last_update = 0
        self.direction = 1
        self.load_images()
        self.image = self.idle_frames_r[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.position = vector(screen_width / 2, screen_height / 2)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        

    def load_images(self):
        self.idle_frames_r = [self.Game.spritesheet.get_image(1,1,377,410),
                            self.Game.spritesheet.get_image(380,1,377,410),
                            self.Game.spritesheet.get_image(759,1,377,410),
                            self.Game.spritesheet.get_image(1138,1,377,410),
                            self.Game.spritesheet.get_image(1517,1,377,410)]
        self.idle_frames_l = []
        for frame in self.idle_frames_r:
            frame.set_colorkey(BLACK)            
            self.idle_frames_l.append(pg.transform.flip(frame, True, False))

        for frame in self.idle_frames_r:
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
        self.jumping_frames_r = [self.Game.spritesheet.get_image(973,907,392,472),
                                 self.Game.spritesheet.get_image(1367,907,392,472),
                                 self.Game.spritesheet.get_image(1761,907,392,472),
                                 self.Game.spritesheet.get_image(2155,907,392,472),
                                 self.Game.spritesheet.get_image(1,1381,392,472)]
        self.jumping_frames_l = []
        for frame in self.jumping_frames_r:
            frame.set_colorkey(BLACK)
            self.jumping_frames_l.append(pg.transform.flip(frame, True, False))

        self.die_frames_l = []
        self.die_frames_r = [self.Game.spritesheet.get_image(2695,458,380,425),
                             self.Game.spritesheet.get_image(2695,885,380,425),
                             self.Game.spritesheet.get_image(2931,1312,380,425),
                             self.Game.spritesheet.get_image(2357,1739,380,425)]
        for frame in self.die_frames_r:
            frame.set_colorkey(BLACK)
            self.die_frames_l.append(pg.transform.flip(frame, True, False))
        


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

    def shoot(self):
        self.bullet = Bullet(self.direction, self.rect.midtop, self.rect.top)
        self.Game.all_sprites.add(self.bullet)
        self.Game.bullets.add(self.bullet)

    def attack(self):        
      # If attack frame has reached end of sequence, return to base frame      
      if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
 
      # Check direction for correct animation to display  
      if self.direction == "RIGHT":
             self.image = attack_ani_R[self.attack_frame]
      elif self.direction == "LEFT":
             self.correction()
             self.image = attack_ani_L[self.attack_frame] 
 
      # Update the current attack frame  
      self.attack_frame += 1

    def update(self):
        self.animate()
        self.acceleration = vector(0, 0.8)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.direction = 0
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
            self.direction = 1
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
        if self.velocity.y != 0:
            self.jumping = True
        else:
            self.jumping = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.velocity.x > 0:
                    if self.direction != 1:
                        self.direction = 1
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    if self.direction != 0:
                        self.direction = 0
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_r)
                bottom = self.rect.bottom
                if self.direction == 1:
                    self.image = self.idle_frames_r[self.current_frame]
                else:
                    self.image = self.idle_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        
        #show jump animation
        if self.jumping:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames_r)
                bottom = self.rect.bottom
                if self.direction == 1:
                    self.image = self.jumping_frames_r[self.current_frame]
                else:
                    self.image = self.jumping_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)


    def kill_animation(self):
        
        for x in range(4):
            now = pg.time.get_ticks()
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.die_frames_l)
                bottom = self.rect.bottom
                if self.velocity.x > 0:
                    self.image = self.die_frames_r[self.current_frame]
                else:
                    self.image = self.die_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Bullet(pg.sprite.Sprite):
    def __init__(self,direction, x, y):
        pg.sprite.Sprite.__init__(self)
        self.direction = direction
        
        self.image = pg.image.load('img/fireball.png').convert()
        self.image = pg.transform.scale(self.image, (15,15))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.midtop = x
        self.speed_x = 5
        self.speed_y = 1

    def update(self):
        if self.direction == 1:
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x
        else:
            self.rect.y += self.speed_y
            self.rect.x -= self.speed_x
        # kill if it moves off the top of the screen
        if self.rect.bottom > screen_height:
            self.kill()
        


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
        self.mask = pg.mask.from_surface(self.image)
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
        self.image = pg.image.load('img/enemiesB.png').convert()
        self.image = pg.transform.scale(self.image, (40, 40))
        #self.image.set_colorkey(BLACK)
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