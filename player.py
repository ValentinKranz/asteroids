import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH

class Player(CircleShape):
    def __init__(self, x, y, radius = PLAYER_RADIUS):
        super().__init__(x, y, radius)
        self.rotation = 0

    def triangle(self):
        #A player will look like a triangle, even though we'll use a circle to represent its hitbox. The math of drawing a triangle can be a bit tricky, so we've written the method for you
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
