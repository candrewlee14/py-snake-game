import pygame
from numpy import arange

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
HEAD_COLOR = (160,160,250)
FPS = 60
SCREEN_SIZE = 720
NUMBER_OF_CELLS_ACROSS = 60
CELL_SIZE = (SCREEN_SIZE / NUMBER_OF_CELLS_ACROSS)
MOVEEVENT, t = pygame.USEREVENT + 1, 50
ALL_CELLS = set()
for x in arange(0, float(SCREEN_SIZE) - CELL_SIZE, CELL_SIZE):
    for y in arange(0, float(SCREEN_SIZE) - CELL_SIZE, CELL_SIZE):
        ALL_CELLS.add((x,y))
