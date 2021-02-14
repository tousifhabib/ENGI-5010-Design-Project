# game options/settings
TITLE = "Platformer"
screen_width = 500
screen_height = 500
FPS = 60

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

# Platform position and size list
platform_list = [
    (0, screen_height-10, 20000, 10),
    (100, screen_height - 100, 200, 10),
    (300, screen_height - 200, 200, 10),
    (400, screen_height - 300, 200, 10),
    (500, screen_height - 400, 200, 10)
    ]