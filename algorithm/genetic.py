import pygame
import numpy as np


class Fish:
    def __init__(self, x, y, dna):
        self.position = np.array([float(x), float(y)])
        self.velocity = np.random.uniform(-1, 1, 2)
        self.accelaration = np.array([0.0, 0.0])
        self.dna = dna
        self.isAlive = True
        self.time_alive = 0
        self.danger_distance_cum_sum = 0

    def update(self, all_fish, shark_position):
        separation = self.cal_separation(all_fish) * self.dna[2]
        alignment  = self.cal_alignment(all_fish) * self.dna[3]
        cohesion   = self.cal_cohesion(all_fish) * self.dna[4]

        self.accelaration +=separation + alignment + cohesion

        self.velocity += self.accelaration

        speed = np.linalg.norm(self.velocity)
        if speed > self.dna[0]:
            self.velocity = (self.velocity / speed) * self.dna[0]

        self.position += self.velocity
        self.accelaration = np.array([0.0, 0.0])
    
    def cal_separation(self, all_fish):
        pass
    def cal_alignment(self, all_fish):
        pass
    def cal_cohesion(self, all_fish):
        pass

    def calculate_fitness(self, frames):
        pass




# [aggregation_range, turning speed, vision radius, cone angle]
class Shark:
    def __init__(self, x, y):
        self.position = np.array([float(x), float(y)])

    def update(self, all_fish):
        pass
        