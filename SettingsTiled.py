import pygame as pg

#Important Colors
darkGray = (40, 40, 40)
lightGray = (100, 100, 100)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

#Game settings
WIDTH = 640   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 384  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 240
TITLE = "Super Cool Side Scroller"
#BackColor = darkGray
FONT = 'arial'
ENEMYA_SPRITESHEET = 'Slimes/Slime_Medium_Blue.png'
ENEMYB_SPRITESHEET = 'Slimes/Flying enemy.png'
PLAYER_RUNNING_SPRITESHEET = 'Archer/Idle and running.png'
PLAYER_FIRING_SPRITESHEET = 'Archer/Normal Attack.png'
PLAYER_HIGH_FIRING_SPRITESHEET = 'Archer/High Attack.png'
PLAYER_LOW_FIRING_SPRITESHEET = 'Archer/Low Attack.png'
PLAYER_DEATH_SPRITESHEET = 'Archer/Death.png'
COIN_SPRITESHEET = 'MonedaD.png'

tilesize = 16
GRIDWIDTH = WIDTH / tilesize
GRIDHEIGHT = HEIGHT / tilesize

#Player Settings
Player_Gravity = 0.8
Player_Acceleration = 1
Player_Friction = -0.3




