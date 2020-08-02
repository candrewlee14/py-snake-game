import pygame.freetype
from food import *
from player import Player
from sys import exit

successes, failures = pygame.init()
print("Initializing pygame: {0} successes and {1} failures.".format(successes, failures))

if int(CELL_SIZE) != CELL_SIZE:
    print("Problem! Bad number of cells")

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)
bigfont = pygame.font.SysFont(None, 60)


start = True
def main():
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
        uncrashed &= head.right <= SCREEN_SIZE
        uncrashed &= head.left >= 0
        uncrashed &= head.bottom <= SCREEN_SIZE
        uncrashed &= head.top >= 0
        #if it crashed, set player as dead and show game over text
        if not uncrashed:
            player.alive = False
            game_over_img = bigfont.render('Game Over', True, RED)
            game_over_rect = game_over_img.get_rect()
            pygame.draw.rect(game_over_img, RED, game_over_rect, 3)
            screen.blit(game_over_img, (SCREEN_SIZE/2 -game_over_img.get_width() / 2, SCREEN_SIZE/2 - game_over_img.get_height() / 2))
            instructions_img = font.render('Press R to Restart, E to End', True, RED)
            screen.blit(instructions_img, (SCREEN_SIZE/2 - instructions_img.get_width() / 2, SCREEN_SIZE/2 + game_over_img.get_height()))
        screen.blit(score_img, (20, 20))
        player.draw(screen)
        food.draw(screen)
        pygame.display.update()

#restart unless user quits or presses E after dying
while start:
    main()

print("Exited the game loop. Game will quit...")
