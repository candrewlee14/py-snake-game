import random
from settings import *

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.relocate([])

    def relocate(self, xy_list):
        #relocates food to unoccupied cell
        open_cells = ALL_CELLS.difference(set(xy_list))
        self.rect.topleft = random.choice(tuple(open_cells)) #more efficient than random.sample for sets
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
