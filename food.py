import random
from settings import *

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.relocate()

    def relocate(self):
        self.rect.x = random.randint(0, (float(SCREEN_SIZE) / CELL_SIZE)-1) * CELL_SIZE
        self.rect.y = random.randint(0, (float(SCREEN_SIZE) / CELL_SIZE)-1) * CELL_SIZE
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
