import pygame 
import sys
import numpy as np
from variables import *
from genetic import Fish, Shark


def main() :

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fish POND | Simulating Prey VS preditor")
    clock =pygame.time.Clock()

    # loading images/ all assets

    try:
        fish_img = pygame.image.load('fish.png').convert_alpha()
        shark_img = pygame.image.load('shark.png').convert_alpha()
        fish_img = pygame.transform.scale(fish_img, (32, 32))
        shark_img = pygame.transform.scale(shark_img, (128, 64))
        print("Images loaded")

    except Exception as e:
        print(f"Sorry: could not load image : {e}")
        fish_img = None
        shark_img = None
    # now create first generation aka spwan all agents.


    fishes = []
    sharks = []

    for _ in range(FISH_COUNT):
        x = np.random.randint(0, SCREEN_WIDTH)
        y = np.random.randint(0, SCREEN_HEIGHT)
        fishes.append(Fish(x, y, image=fish_img))
    
    for _ in range(SHARK_COUNT):
        x = np.random.randint(0, SCREEN_WIDTH)
        y = np.random.randint(0, SCREEN_HEIGHT)
        sharks.append(Shark(x, y, image=shark_img))

    # main while loop
    running = True
    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False
            
        
        for shark in sharks:
            shark.update(fishes)
        
        for fish in fishes:
            fish.update(fishes, sharks)

        screen.fill(BACKGROUND_COLOR)

        for fish in fishes:
            fish.draw(screen)
        
        for shark in sharks:
            shark.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()
    sys.exit()
    

    # quit
    



if __name__ == '__main__':
    print("hello from GAME")
    main()  