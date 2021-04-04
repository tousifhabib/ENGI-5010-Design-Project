# game options/settings
TITLE = "Platformer"
screen_width = 500
screen_height = 500
FPS = 60
SPRITESHEET = "spritesheet-2.png"
FONT_NAME = 'arial'

# Player properties
player_acceleration = 0.85
player_friction = -0.22
player_gravity = 100

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SPLASH = (0, 155, 155)

# Platform position and size list
platform_list = [
    (0, screen_height - 10),
    (200, screen_height - 10),
    (400, screen_height - 10),
    (600, screen_height - 10),
    (800, screen_height - 10),
    (1000, screen_height - 10),
    (1200, screen_height - 10),
    
    (100, screen_height - 120),
    (300, screen_height - 220),
    (400, screen_height - 320),
    (500, screen_height - 420),
    (750, screen_height - 220),
    
]


enemy_listA = [
    (100, screen_height - 300),
    (320, screen_height - 300),
    (340, screen_height - 300),
    (360, screen_height - 300),
    (380, screen_height - 300),
    (400, screen_height - 300),
    (420, screen_height - 300),
    (440, screen_height - 300),
    (460, screen_height - 300),
    (480, screen_height - 300)
]

enemy_listB = [
    (100, screen_height - 380),
    (320, screen_height - 380)
]