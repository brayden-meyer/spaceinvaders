import pygame
from Invader import Invader


class Octopus(Invader):
    POINTS = 10
    COLOR = (255, 0, 255)

    def __init__(self, location):
        super().__init__()

        # Load image
        self.image = pygame.image.load("res/images/octopus_0.png")
        self.rect = self.image.get_rect()
        # Colorize
        self.image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.image.fill(Octopus.COLOR + (0,), None, pygame.BLEND_RGBA_ADD)

        self.rect.center = location

