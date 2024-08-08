import pygame
import sys
import json
from os.path import join
from os import remove, execv, makedirs
from random import choice
from statistics import mean

# Color settings
BG_COLOR = 'black'
TEXT_COLOR = 'white'
TITLE_COLOR = 'yellow'
TARGET_COLOR = 'red'

default_settings = {
    'timer': 30,
    'ui_details': True,
    'num_of_targets': 3,
    'base_score': 100,
    'bonus_interval': 1000,
    'edge': 4
}

makedirs('data', exist_ok=True)


def load_settings():
    try:
        with open(join('data/custom_settings.json'), 'r') as file:
            custom_settings = json.load(file)
            return custom_settings
    except FileNotFoundError:  # default settings
        return default_settings


settings = load_settings()

TIMER = settings['timer']  # Time for each round (seconds)
UI_DETAILS = settings['ui_details']  # False for minimal ingame display
NUM_OF_TARGETS = settings['num_of_targets']  # max = 3
BASE_SCORE = settings['base_score']
BONUS_INTERVAL = settings['bonus_interval']  # miliseconds
EDGE = settings['edge']  # in range [2-7]

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
DIAMETER = (75, 75)
TARGET_DISTANCE = 85  # from center to center
BONUS = BASE_SCORE * 10  # fixed at 10x base score

GRID_TOPLEFT = (WINDOW_WIDTH / 2 - (EDGE / 2 - .5) * TARGET_DISTANCE,
                WINDOW_HEIGHT / 2 - (EDGE / 2 - .5) * TARGET_DISTANCE)
GRID_POS = []
for i in range(EDGE):
    for j in range(EDGE):
        x_pos = GRID_TOPLEFT[0] + TARGET_DISTANCE * j
        y_pos = GRID_TOPLEFT[1] + TARGET_DISTANCE * i
        GRID_POS.append((x_pos, y_pos))
