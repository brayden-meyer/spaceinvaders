import pygame


class Missile(pygame.sprite.Sprite):

    COLOR = (255, 0, 0)
    SIZE = (3, 10)

    def __init__(self, shooter, velocity):
        super().__init__()

        self.shooter = shooter
        self.velocity = velocity

        self.image = pygame.Surface(Missile.SIZE)
        self.image.fill((255, 255, 255, 0))
        self.image.set_colorkey((255, 255, 255, 0))

        pygame.draw.rect(self.image, Missile.COLOR, (0, 0, *Missile.SIZE))
        # print(shooter.rect.center)

        # Bottom of missile at top of shooter
        self.rect = self.image.get_rect()
        self.rect.midbottom = shooter.rect.midtop

    def update(self):
        # Move missile
        self.rect.move_ip(self.velocity)

    # Returns true if hit was successful
    def hit(self, group):
        # Check collisions
        for sprite in group.sprites():
            if pygame.sprite.collide_mask(self, sprite):
                self.shooter.points += sprite.POINTS
                group.remove(sprite)
                self.kill()
                return True
        return False

