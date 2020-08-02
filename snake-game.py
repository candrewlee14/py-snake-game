import pygame
import pygame.freetype
import random
from sys import exit

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

SCREEN_WIDTH_AND_HEIGHT = 720
NUMBER_OF_CELLS_ACROSS = 60 
CELL_WIDTH = (SCREEN_WIDTH_AND_HEIGHT / NUMBER_OF_CELLS_ACROSS)
if int(CELL_WIDTH) != CELL_WIDTH:
    print("Problem! Bad number of cells")

screen = pygame.display.set_mode((SCREEN_WIDTH_AND_HEIGHT, SCREEN_WIDTH_AND_HEIGHT))
clock = pygame.time.Clock()
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 24)
bigfont = pygame.font.SysFont(None, 60)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ate_food = False
        self.alive = True
        self.body_list = [
                pygame.Rect(0,0, CELL_WIDTH, CELL_WIDTH),
                pygame.Rect(0,CELL_WIDTH, CELL_WIDTH, CELL_WIDTH),
                pygame.Rect(0,CELL_WIDTH*2, CELL_WIDTH, CELL_WIDTH)
            ]
        self.image = pygame.Surface((CELL_WIDTH, CELL_WIDTH))
        self.velocity = [CELL_WIDTH, 0]

    def change_direction(self, key):
        if key == pygame.K_RIGHT:
            self.velocity = [CELL_WIDTH,0]
        if key == pygame.K_LEFT:
            self.velocity = [-1*CELL_WIDTH,0]
        if key == pygame.K_UP:
            self.velocity = [0, -1*CELL_WIDTH]
        if key == pygame.K_DOWN:
            self.velocity = [0,CELL_WIDTH]

    def update(self):
        if self.alive:
            tail = self.body_list[0].copy()
            for i in range(len(self.body_list)-1):
                self.body_list[i] = self.body_list[i+1].copy()
            self.body_list[-1].move_ip(*self.velocity)
            if self.ate_food:
                self.body_list.insert(0, tail)
            self.ate_food = False
    
    def draw(self):
        for item in self.body_list:
            pygame.draw.rect(screen, WHITE, item)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,CELL_WIDTH, CELL_WIDTH, CELL_WIDTH)
        self.image = pygame.Surface((CELL_WIDTH, CELL_WIDTH))
        self.relocate()

    def relocate(self):
        self.rect.x = random.randint(0, (float(SCREEN_WIDTH_AND_HEIGHT) / CELL_WIDTH)-1) * CELL_WIDTH
        self.rect.y = random.randint(0, (float(SCREEN_WIDTH_AND_HEIGHT) / CELL_WIDTH)-1) * CELL_WIDTH
    
    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)

start = True
def main():
    MOVEEVENT, t = pygame.USEREVENT + 1, 50
    pygame.time.set_timer(MOVEEVENT, t)

    food = Food()
    player = Player()
    score_img = font.render('1', True, WHITE)
    running = True
    while running:
        dt = clock.tick(FPS) / 1000 
        screen.fill(BLACK)

        for event in pygame.event.get():
            #moves the player every time this event ticks
            if event.type == MOVEEVENT:
                player.update()            
            if event.type == pygame.QUIT:
                running = False
                start = False
                exit()
            elif event.type == pygame.KEYDOWN:
                #R to restart game after dying
                if event.key == pygame.K_r and not player.alive:
                    start = True
                    return
                #E to end game after dying
                elif event.key == pygame.K_e and not player.alive:
                    start = False
                    exit()   
                #otherwise, change velocity direction of player with arrow keys          
                else:
                    player.change_direction(event.key)

        #if player runs into food, mark it as eating food, relocate food, and change score text
        if player.body_list[-1].center == food.rect.center:
            player.ate_food = True
            food.relocate()
            score_img = font.render(str(len(player.body_list)), True, WHITE)

        head = player.body_list[-1]
        uncrashed = True
        #check head is not hitting any body part
        for item in player.body_list[:-1]:
            uncrashed &= (item.center != head.center)
        #check head is not hitting any wall
        uncrashed &= head.right <= SCREEN_WIDTH_AND_HEIGHT
        uncrashed &= head.left >= 0
        uncrashed &= head.bottom <= SCREEN_WIDTH_AND_HEIGHT
        uncrashed &= head.top >= 0
        #if it crashed, set player as dead and show game over text
        if not uncrashed:
            player.alive = False
            game_over_img = bigfont.render('Game Over', True, RED)
            game_over_rect = game_over_img.get_rect()
            pygame.draw.rect(game_over_img, RED, game_over_rect, 3)
            screen.blit(game_over_img, (SCREEN_WIDTH_AND_HEIGHT/2 -game_over_img.get_width() / 2, SCREEN_WIDTH_AND_HEIGHT/2 - game_over_img.get_height() / 2))
            instructions_img = font.render('Press R to Restart, E to End', True, RED)
            screen.blit(instructions_img, (SCREEN_WIDTH_AND_HEIGHT/2 - instructions_img.get_width() / 2, SCREEN_WIDTH_AND_HEIGHT/2 + game_over_img.get_height()))
        screen.blit(score_img, (20, 20))
        player.draw()
        food.draw()
        pygame.display.update()

#restart unless user quits or presses E after dying
while start:
    main()

print("Exited the game loop. Game will quit...")
