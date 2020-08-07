
from settings import *
from math import floor

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ate_food = False
        self.alive = True
        self.body_list = [
                pygame.Rect(0,0, CELL_SIZE, CELL_SIZE),
            ]
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.velocity = [CELL_SIZE, 0]
        #set line width as a bit smaller than the head size, but it must be odd so it line is centered (per pygame docs)
        self.line_width = floor((CELL_SIZE * .45)) * 2 + 1

    def move_tuple(self, topleft: tuple):
        return tuple([(a+b) % SCREEN_SIZE for a, b in zip(topleft, self.velocity)])

    def change_direction(self, key):
        head_pos= self.body_list[-1].topleft
        more_than_one = len(self.body_list) > 1
        x_change, y_change = 0, 0
        if more_than_one:
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
            self.body_list[-1].topleft = self.move_tuple(self.body_list[-1].topleft)
            if self.ate_food:
                self.body_list.insert(0, tail)
            self.ate_food = False
    
    def draw(self, screen):
        for i in range(0, len(self.body_list) - 1):
            difference = tuple([abs(a-b) for a, b in zip(self.body_list[i], self.body_list[i+1])])
            if difference[0] > CELL_SIZE or difference[1] > CELL_SIZE:
                continue
            pygame.draw.line(screen, 
                WHITE, 
                self.body_list[i].center,
                self.body_list[i+1].center, 
                self.line_width)
        pygame.draw.rect(screen, HEAD_COLOR, self.body_list[-1])
