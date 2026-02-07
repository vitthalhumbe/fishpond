import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

FPS = 60

BACKGROUND_COLOR = (0, 84, 119)



FISH_COUNT = 50      # for testing, TODO : change it later
SHARK_COUNT = 1      # it should be one always... not planned for multple sharks.

FISH_DNA = {
    "max_speed": 5.0,
    "vision_radius": 40,
    "separation_weight": 2.0,
    "alignment_weight": 1.0,
    "cohesion_weight": 1.0,
    "fear_weight": 0.0
}


SHARK_DNA = {
    "max_speed": 10,
    "vision_radius": 300,
    "vision_angle": 0.0             # 0.5 = 60 degree dot product threshold.
}

