import pygame 
import sys
import numpy as np
from variables import *
from agents import Fish, Shark
from genetic_algorithm import Evolution

def main() :

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fish POND | Simulating Prey VS preditor")
    clock =pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)
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
    evolution = Evolution(FISH_COUNT)

    fishes = []
    sharks = []
    dead_fishes = []        # stats purpose

    frames_ended = 0  # counting number of time alive



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
        frames_ended += 1
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False
        
        alive_fishes = []

        
        for shark in sharks:
            shark.update(fishes)
        
        for fish in fishes:
            fish.update(fishes, sharks)

            if fish.isAlive:
                alive_fishes.append(fish)
            else:
                dead_fishes.append(fish)
        
        fishes = alive_fishes

        if len(fishes) == 0:
            new_population = evolution.next_generation(dead_fishes, frames_ended)

            dead_fishes.clear()
            sharks.clear()
            frames_ended = 0

            for i in range(FISH_COUNT):
                x = np.random.randint(0, SCREEN_WIDTH)
                y = np.random.randint(0, SCREEN_HEIGHT)
                new_fish = Fish(x, y, fish_img, dna=new_population[i])
                fishes.append(new_fish)

            for _ in range(SHARK_COUNT):
                x = np.random.randint(0, SCREEN_WIDTH)
                y = np.random.randint(0, SCREEN_HEIGHT)
                sharks.append(Shark(x, y, image=shark_img)) 

        screen.fill(BACKGROUND_COLOR)

        for fish in fishes:
            fish.draw(screen)
        
        for shark in sharks:
            shark.draw(screen)

        stats_text = font.render(f"Gen: {evolution.generation_count} | Alive : {len(fishes)} | Time : {frames_ended}", True, (255, 255, 255))
        screen.blit(stats_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()
    sys.exit()
    

    # quit
    



if __name__ == '__main__':
    print("hello from GAME")
    main()  