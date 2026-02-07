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

    stats_history = []
    MAX_GEN_TIME = 60 * FPS

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
        time_left = (MAX_GEN_TIME - frames_ended) / FPS
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

        if len(fishes) == 0 or frames_ended >= MAX_GEN_TIME:

            for survivor in fishes:
                survivor.isAlive = False # Mark as done
                dead_fishes.append(survivor)

            best_fit = 0
            total_fit = 0
            for f in dead_fishes:
                fit = f.calculate_fitness(frames_ended) # Use actual time elapsed
                if fit > best_fit: best_fit = fit
                total_fit += fit

            avg_fit = total_fit / len(dead_fishes) if len(dead_fishes) > 0 else 0
            stats_history.append((best_fit, avg_fit))
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
        draw_live_graph(screen, stats_history, SCREEN_WIDTH - 220, 10, 200, 100)
        for fish in fishes:
            fish.draw(screen)
        
        for shark in sharks:
            shark.draw(screen)

        timer_color = (255, 255, 255)
        if time_left < 10: timer_color = (255, 50, 50) # Red warning
        timer_text = font.render(f"Time: {time_left:.1f}s | Gen: {evolution.generation_count} | Fish Alive : {len(fishes)}", True, timer_color)
        screen.blit(timer_text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)


    pygame.quit()
    sys.exit()
    

    # quit
    

# THIS IS AI GENERATED : 
def draw_live_graph(screen, data, x, y, w, h):
    # Background Box
    s = pygame.Surface((w, h))
    s.set_alpha(150) 
    s.fill((0, 0, 0))
    screen.blit(s, (x, y))
    
    # Border
    pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h), 1)
    
    if len(data) < 2: return

    # 1. Unpack Data
    best_scores = [d[0] for d in data]
    avg_scores  = [d[1] for d in data]
    
    # Normalize based on the highest BEST score (so both fit in scale)
    max_val = max(best_scores)
    if max_val == 0: max_val = 1
    
    # 2. Draw BEST Line (Green)
    best_points = []
    for i, val in enumerate(best_scores):
        px = x + (i / max(1, len(data)-1)) * w
        py = (y + h) - (val / max_val) * h
        best_points.append((px, py))
    pygame.draw.lines(screen, (0, 255, 0), False, best_points, 2)
    
    # 3. Draw AVG Line (Red)
    avg_points = []
    for i, val in enumerate(avg_scores):
        px = x + (i / max(1, len(data)-1)) * w
        py = (y + h) - (val / max_val) * h
        avg_points.append((px, py))
    pygame.draw.lines(screen, (255, 50, 50), False, avg_points, 2)
        
    # Labels
    font = pygame.font.SysFont("Arial", 12)
    label_best = font.render(f"Best: {best_scores[-1]:.2f}", True, (0, 255, 0))
    label_avg  = font.render(f"Avg: {avg_scores[-1]:.2f}", True, (255, 50, 50))
    
    screen.blit(label_best, (x + 5, y + 5))
    screen.blit(label_avg, (x + 5, y + 20))

if __name__ == '__main__':
    print("hello from GAME")
    main()  