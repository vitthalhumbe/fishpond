import pygame
import numpy as np

from variables import *

import math

class Fish:
    def __init__(self, x, y, image=None, dna=None):
        self.position = np.array([float(x), float(y)])
        self.velocity = np.random.uniform(-1, 1, 2)
        self.accelaration = np.array([0.0, 0.0])
        self.image = image
        
        self.isAlive = True
        self.time_alive = 0
        self.cohesion_bonus = 0
        self.danger_score=0
        self.fitness = 0

        if dna is not None:
            self.dna = dna
        else:
            self.dna = np.array([4.0, 100.0, 2.5, 1.0, 1.0, 10.0])

    def update(self, all_fish, sharks):
        if not self.isAlive: return
        self.time_alive += 1
        separation = self.cal_separation(all_fish) * self.dna[2]
        alignment  = self.cal_alignment(all_fish)  * self.dna[3]
        cohesion   = self.cal_cohesion(all_fish)   * self.dna[4]
        
        fear = np.array([0.0, 0.0])
        current_danger_distance = 0
        for shark in sharks:
            fear_vector, distance = self.cal_fear(shark.position)
            fear += fear_vector
            current_danger_distance += distance
        fear *= self.dna[5]
        
        if len(sharks) > 0:
            avg_distance = current_danger_distance / len(sharks)
            self.danger_score += avg_distance
        self.accelaration += separation + alignment + cohesion + fear
        self.velocity += self.accelaration
        speed = np.linalg.norm(self.velocity)
        if speed > self.dna[0]:
            self.velocity = (self.velocity / speed) * self.dna[0]

        self.position += self.velocity
        self.accelaration = np.array([0.0, 0.0])
        self.edges()

    def limit_force(self, force):
        max_force = 0.1
        magnitude = np.linalg.norm(force)
        if magnitude > max_force:
            force = (force / magnitude) * max_force
        return force

    def cal_separation(self, all_fish):
        steering = np.array([0.0, 0.0])
        count = 0
        personal_space = self.dna[1] / 2
        
        for other in all_fish:
            if not other.isAlive: continue
            
            diff = self.position - other.position
            dist_sq = np.dot(diff, diff)
            
            if 0 < dist_sq < (personal_space**2):
                dist = np.sqrt(dist_sq)
                diff /= dist 
                steering += diff
                count += 1
                
        if count > 0:
            steering /= count
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * self.dna[0]
                steering -= self.velocity
                steering = self.limit_force(steering)
        return steering

    def cal_alignment(self, all_fish):
        steering = np.array([0.0, 0.0])
        count = 0
        
        for other in all_fish:
            if not other.isAlive: continue
            
            dist_sq = np.sum((self.position - other.position)**2)
            if 0 < dist_sq < (self.dna[1]**2):
                steering += other.velocity
                count += 1
                
        if count > 0:
            steering /= count
            if np.linalg.norm(steering) > 0:
                steering = (steering / np.linalg.norm(steering)) * self.dna[0]
                steering -= self.velocity
                steering = self.limit_force(steering) 
        return steering

    def cal_cohesion(self, all_fish):
        steering = np.array([0.0, 0.0])
        count = 0
        
        for other in all_fish:
            if not other.isAlive: continue
            
            dist_sq = np.sum((self.position - other.position)**2)
            if 0 < dist_sq < (self.dna[1]**2):
                steering += other.position
                count += 1
                
        if count > 0:
            self.cohesion_bonus += 1
            steering /= count
            vec_to_center = steering - self.position
            if np.linalg.norm(vec_to_center) > 0:
                vec_to_center = (vec_to_center / np.linalg.norm(vec_to_center)) * self.dna[0]
                steering = vec_to_center - self.velocity
                steering = self.limit_force(steering) 
            else:
                steering = np.array([0.0, 0.0])
        return steering

    def cal_fear(self, shark_pos):
        flee = self.position - shark_pos
        dist_sq = np.dot(flee, flee)
        distance = np.sqrt(dist_sq)
        
        if dist_sq < ((self.dna[1] + 50)**2):
            if distance > 0:
                flee_vec = (flee / distance) * self.dna[0]
            else:
                flee_vec = np.array([0.0, 0.0])
            steer = flee_vec - self.velocity
            
            max_fear_force = 0.5 
            magnitude = np.linalg.norm(steer)
            if magnitude > max_fear_force:
                steer = (steer / magnitude) * max_fear_force
            return (steer, distance)
            
        return (np.array([0.0, 0.0]), distance)
        
    def edges(self):
        if self.position[0] > SCREEN_WIDTH: self.position[0] = 0
        if self.position[0] < 0: self.position[0] = SCREEN_WIDTH
        if self.position[1] > SCREEN_HEIGHT: self.position[1] = 0
        if self.position[1] < 0: self.position[1] = SCREEN_HEIGHT

    def draw(self, screen):
        if not self.isAlive: return
        angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))
        
        if self.image:
            rotated_img = pygame.transform.rotate(self.image, -angle)
            rect = rotated_img.get_rect(center=(self.position[0], self.position[1]))
            screen.blit(rotated_img, rect)
        else:
            pygame.draw.circle(screen, (0, 255, 255), self.position.astype(int), 3)
    def calculate_fitness(self, max_time):
        w1 = 0.5
        w2 = 0.2

        time = self.time_alive / max_time if max_time > 0 else 0
        cohesion = self.cohesion_bonus / max_time if max_time > 0 else 0
        danger = (self.danger_score / self.time_alive) / 500.0 if self.time_alive> 0 else 0

        self.fitness = time + (w1 * cohesion) + (w2 * danger)
        return self.fitness
    
class Shark:
    def __init__(self, x, y, image=None):
        self.position = np.array([float(x), float(y)])
        self.velocity = np.array([2.0, 0.0])
        self.accelaration = np.array([0.0, 0.0])
        self.image = image
        
        self.dna = np.array(list(SHARK_DNA.values())) 
        
        self.wander_angle = 0.0

    def update(self, all_fish):
        target = self.find_target(all_fish)
        
        if target:
            desired = target.position - self.position
            dist = np.linalg.norm(desired)
            
            if dist < 50: 
                target.isAlive = False
            
            if dist > 0:
                desired = (desired / dist) * self.dna[0]
            
            steer = desired - self.velocity
            
            
            max_force = 0.1 
            if np.linalg.norm(steer) > max_force:
                steer = (steer / np.linalg.norm(steer)) * max_force
            
            self.accelaration += steer
        else:
            current_speed = np.linalg.norm(self.velocity)
            if current_speed > 0:
                heading = self.velocity / current_speed
            else:
                heading = np.array([1.0, 0.0])
            
            circle_center = self.position + (heading * 100)
            self.wander_angle += np.random.uniform(-0.2, 0.2)
            displacement = np.array([math.cos(self.wander_angle), math.sin(self.wander_angle)]) * 50
            wander_target = circle_center + displacement
            desired = wander_target - self.position
            if np.linalg.norm(desired) > 0:
                desired = (desired / np.linalg.norm(desired)) * 2.0 
                
            steer = desired - self.velocity
            max_force = 0.1
            if np.linalg.norm(steer) > max_force:
                 steer = (steer / np.linalg.norm(steer)) * max_force
                 
            self.accelaration += steer
        self.velocity += self.accelaration
        speed = np.linalg.norm(self.velocity)
        if speed > self.dna[0]:
            self.velocity = (self.velocity / speed) * self.dna[0]
            
        self.position += self.velocity
        self.accelaration = np.array([0.0, 0.0]) 
        self.edges()
        
    def find_target(self, all_fish):
        closest_dist = float('inf')
        target = None
        heading = self.velocity.copy()
        if np.linalg.norm(heading) > 0:
            heading /= np.linalg.norm(heading)
        
        for fish in all_fish:
            if not fish.isAlive: continue
            
            to_fish = fish.position - self.position
            dist_sq = np.sum(to_fish**2)
            if dist_sq < (self.dna[1]**2):
                dist = np.sqrt(dist_sq)
                
                # 2. Check Vision Cone
                to_fish_norm = to_fish / dist
                dot = np.dot(heading, to_fish_norm)
                
                if dot > self.dna[2]: 
                    if dist < closest_dist:
                        closest_dist = dist
                        target = fish
        return target

    def edges(self):
        if self.position[0] > SCREEN_WIDTH: self.position[0] = 0
        if self.position[0] < 0: self.position[0] = SCREEN_WIDTH
        if self.position[1] > SCREEN_HEIGHT: self.position[1] = 0
        if self.position[1] < 0: self.position[1] = SCREEN_HEIGHT

    def draw(self, screen):
        angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0]))
        pygame.draw.circle(screen, (50, 50, 50), self.position.astype(int), int(self.dna[1]), 1)
        
        if self.image:
            rotated_img = pygame.transform.rotate(self.image, -angle)
            rect = rotated_img.get_rect(center=(self.position[0], self.position[1]))
            screen.blit(rotated_img, rect)
        else:
            pygame.draw.circle(screen, (255, 0, 0), self.position.astype(int), 10)