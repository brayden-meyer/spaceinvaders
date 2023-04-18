import pygame

from Missile import Missile


class LaserCannon(pygame.sprite.Sprite):

    COLOR = (255, 255, 255)

    def __init__(self, location):
        super().__init__()

        # Load image
        self.image = pygame.image.load("res/images/laser_cannon.png")
        # Colorize
        self.image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.image.fill(LaserCannon.COLOR + (0,), None, pygame.BLEND_RGBA_ADD)

        self.rect = self.image.get_rect()

        self.rect.center = location

        self.points = 0

    def left(self):
        self.rect.centerx -= 5

    def right(self):
        self.rect.centerx += 5

    # Returns a Missile with this LaserCannon as the shooter, velocity up
    def shoot(self):
        return Missile(self, (0, -10))

