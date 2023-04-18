import pygame
from Squid import Squid
from Crab import Crab
from Octopus import Octopus


class InvaderGroup(pygame.sprite.Group):
    def __init__(self, location):
        super().__init__()

        self.speed = 20
        start_x = location[0]
        start_y = location[1]
        # Generate 5 rows of invaders
        self.rows = []
        for row_number, invader_type in enumerate((Octopus, Octopus, Crab, Crab, Squid)):
            row_invaders = []
            for i in range(7):
                invader = invader_type((start_x + 65*i, start_y - 65*row_number))
                row_invaders.append(invader)
                self.add(invader)

    # Move invaders horizontally and reverse at bounds
    def move(self, bounds):
        reverse = False
        down = False
        for invader in self.sprites():
            invader.rect.centerx += self.speed
            if not invader.rect.colliderect(bounds) and not down:
                self.down()
                reverse = True
                down = True
        if reverse:
            self.speed = -self.speed
        down = False

    # Move all invaders down 1 row, closer to the player / LaserCannon
    def down(self):
        for invader in self.sprites():
            invader.rect.centery += 60

