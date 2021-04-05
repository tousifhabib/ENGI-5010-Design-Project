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
FPS = 60
TITLE = "Tilemap Demo"
#BackColor = darkGray
FONT = 'arial'
ENEMY_SPRITESHEET = 'Slimes/Slime_Medium_Blue.png'
PLAYER_RUNNING_SPRITESHEET = 'Archer/Idle and running.png'
PLAYER_FIRING_SPRITESHEET = 'Archer/Normal Attack.png'

tilesize = 16
GRIDWIDTH = WIDTH / tilesize
GRIDHEIGHT = HEIGHT / tilesize

#Player Settings
Player_Gravity = 0.8
Player_Acceleration = 1
Player_Friction = -0.2






enemy_left = []


idle_frames_R = [pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00000.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00001.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00002.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00003.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00004.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00005.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00006.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00007.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00008.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00009.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00010.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00011.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00012.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00013.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00014.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00015.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00016.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00017.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00018.png"), (30, 60)),
                pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00019.png"), (30, 60)),
]

idle_frames_L = [pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00000.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00001.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00002.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00003.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00004.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00005.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00006.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00007.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00008.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00009.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00010.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00011.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00012.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00013.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00014.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00015.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00016.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00017.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00018.png"), (30, 60)), True, False),
                pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00019.png"), (30, 60)), True, False),
]

jumping_frames_R = [pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00000.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00001.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00002.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00003.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00004.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00005.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00006.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00007.png"), (30, 60)),
]

jumping_frames_L = [pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00000.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00001.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00002.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00003.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00004.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00005.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00006.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardJump/CharaWizardJump_00007.png"), (30, 60)), True, False),
]

walking_frames_R = [pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00000.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00001.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00002.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00003.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00004.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00005.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00006.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00007.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00008.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00009.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00010.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00011.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00012.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00013.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00014.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00015.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00016.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00017.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00018.png"), (30, 60)),
                    pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00019.png"), (30, 60)),
        ]

walking_frames_L = [pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00000.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00001.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00002.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00003.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00004.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00005.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00006.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00007.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00008.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00009.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00010.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00011.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00012.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00013.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00014.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00015.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00016.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00017.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00018.png"), (30, 60)), True, False),
                    pg.transform.flip(pg.transform.smoothscale(pg.image.load("Forest/BlueWizard/2BlueWizardWalk/Chara_BlueWalk00019.png"), (30, 60)), True, False),
]