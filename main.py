import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, ASTEROID_SCORE_POINT
from logger import log_state, log_event
from player import Player
from asteroids import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()

    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        
        for asteroid in asteroids:
            if asteroid.damaging:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    print("Game over!")
                    print(f"Score: {player.score}")
                    sys.exit()
             
        for asteroid in asteroids:
            if asteroid.shootable:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event(f"asteroid_shot: +{ASTEROID_SCORE_POINT} points")
                        player.score += asteroid.score_point
                        asteroid.explode()
                        asteroid.split()
                        shot.kill()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        
        score_surface = font.render(f"Score: {player.score}", True, "white")
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
