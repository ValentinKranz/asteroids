import pygame
import random
import math
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_IRREGULARITY, ASTEROID_POINTS
from logger import  log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = self.generate_polygon()

    def generate_polygon(self, irregularity = ASTEROID_IRREGULARITY, points = ASTEROID_POINTS):
        shape = []
        angle_step = 360 / points
        
        for i in range(points):
            angle = math.radians(i * angle_step)
            offset = random.uniform(1 - irregularity, 1 + irregularity)
            r = self.radius * offset
            x = math.cos(angle) * r
            y = math.sin(angle) * r
            shape.append((x, y))

        return shape

    def draw(self, screen):
        poly = [(self.position.x + px, self.position.y + py) for px, py in self.points]
        pygame.draw.polygon(screen, "white", poly, LINE_WIDTH)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        new_asteroid_one_vector = self.velocity.rotate(random_angle)
        new_asteroid_two_vector = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid_one = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_two = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_one.velocity = new_asteroid_one_vector * 1.2
        new_asteroid_two.velocity = new_asteroid_two_vector * 1.2