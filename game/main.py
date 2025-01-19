from game_logic import *
import random

playerOneChar = Player(SCREEN_WIDTH//2,SCREEN_HEIGHT//2 + 100, 75, 25)


running = True
while running:  #this is the game loop
        li = [300,800, 1000]
        playerOneChar.set_target(random.choice(li))
        playerOneChar.move_character()
        screen.fill((0,0,0))
        draw_court()
        draw_text(f"Player 1: {firstPlayerScore}", font, WHITE, 10, margin + 15)
        draw_text(f"Player 2: {secondPlayerScore}", font, WHITE, SCREEN_HEIGHT + 425, margin + 15)
        playerOneChar.draw()
        
        for event in pygame.event.get(): #checks for game events
            if event.type == pygame.QUIT: #if the exit button is being clicked we will exit the while loop
                running = False

        pygame.display.flip()

        clock.tick(60)  

pygame.quit()
