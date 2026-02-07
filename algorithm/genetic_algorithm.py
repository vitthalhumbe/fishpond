import random
import copy
import numpy as np

class Evolution:
    def __init__(self, population_size):
        self.population_size = population_size
        self.generation_count = 1

    def next_generation(self, dead_population, max_sim_time):
        print("Generation No. : ", self.generation_count)

        for fish in dead_population:
            fish.calculate_fitness(max_sim_time)
        
        dead_population.sort(key=lambda x:x.fitness, reverse=True)
        print("Best fitness : ", dead_population[0].fitness)
        print("best DNA : ", dead_population[0].dna)

        new_population = []

        new_population.append(dead_population[0].dna)
        new_population.append(dead_population[1].dna)
        # this was elitism 

        while len(new_population) < self.population_size:
            parent1 = self.tournament_selection(dead_population[:25])
            parent2 = self.tournament_selection(dead_population[:25])

            child_dna = self.crossover(parent1, parent2)
            child_dna = self.mutation(child_dna)
            new_population.append(child_dna)
        
        self.generation_count += 1
        return new_population


    # simply pick three random fishes, and then return fish with best fitness among them.
    def tournament_selection(self, population):
        cans = random.sample(population, 3)         # sleect three participents randomaly.
        cans.sort(key= lambda x: x.fitness, reverse=True)

        return cans[0]


    def crossover(self, parent1, parent2):
        splitPoint = random.randint(1, len(parent1.dna) - 2)
        child_dna = np.concatenate((parent1.dna[:splitPoint], parent2.dna[splitPoint:]))
        return child_dna

    def mutation(self, dna):
        # pure randomness added to one gene randomly for variations.
        mutation_rate = 0.05
        for i in range(len(dna)):
            if random.random() < mutation_rate:
                dna[i] += random.uniform(-0.1, 0.1)

                dna[i] = max(0.1, dna[i])           # no negative values here

        return dna