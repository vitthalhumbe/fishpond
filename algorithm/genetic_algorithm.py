import random
import copy

class Evolution:
    def __init__(self, population_size):
        self.population_size = population_size
        self.generation_count = 1

    def next_generation(self, dead_population, max_sim_time):
        pass

    def tournament_selection(self, population):
        pass

    def crossover(self, parent1, parent2):
        pass

    def mutation(self, dna):
        pass