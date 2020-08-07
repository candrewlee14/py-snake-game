
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ate_food = False
        self.alive = True
        self.body_list = [
                pygame.Rect(0,0, CELL_SIZE, CELL_SIZE),
                pygame.Rect(0,CELL_SIZE, CELL_SIZE, CELL_SIZE),
                pygame.Rect(0,CELL_SIZE*2, CELL_SIZE, CELL_SIZE)
            ]
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.velocity = [CELL_SIZE, 0]

    def change_direction(self, key):
        head_pos= self.body_list[-1].topleft
        neck_pos= self.body_list[-2].topleft
        x_change = neck_pos[0] - head_pos[0] 
        y_change = neck_pos[1] - head_pos[1]
        if key == pygame.K_RIGHT:
            if x_change <= 0:
                self.velocity = [CELL_SIZE,0]
        if key == pygame.K_LEFT:
            if x_change >= 0:
                self.velocity = [-1*CELL_SIZE,0]
        if key == pygame.K_UP:
            if y_change >= 0:
                self.velocity = [0, -1*CELL_SIZE]
        if key == pygame.K_DOWN:
            if y_change <= 0:
                self.velocity = [0,CELL_SIZE]

    def update(self):
        if self.alive:
            tail = self.body_list[0].copy()
            for i in range(len(self.body_list)-1):
                self.body_list[i] = self.body_list[i+1].copy()
            self.body_list[-1].move_ip(*self.velocity)
            if self.ate_food:
                self.body_list.insert(0, tail)
            self.ate_food = False
    
    def draw(self, screen):
        for item in self.body_list[-1]:
            pygame.draw.rect(screen, WHITE, item)
        pygame.draw.rect(screen, HEAD_COLOR, self.body_list[-1])
