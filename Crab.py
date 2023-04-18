import pygame
from Invader import Invader


class Crab(Invader):
    POINTS = 20
    COLOR = (0, 255, 255)

    def __init__(self, location):
        super().__init__()

        # Load image
        self.image = pygame.image.load("res/images/crab_0.png")
        self.rect = self.image.get_rect()
        # Colorize
        self.image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        self.image.fill(Crab.COLOR + (0,), None, pygame.BLEND_RGBA_ADD)

        self.rect.center = location

