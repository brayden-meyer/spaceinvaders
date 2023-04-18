import pygame
from pygame.locals import *
from GameState import GameState
from InvaderGroup import InvaderGroup
from LaserCannon import LaserCannon


class SpaceInvaders:
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    ORIGIN = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):
        pygame.init()
        # pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.game_state = None

        # Initialize display
        pygame.display.set_caption("Space Invaders")
        pygame.display.set_icon(pygame.image.load("res/images/app_icon.png"))
        self.screen = pygame.display.set_mode(SpaceInvaders.SCREEN_SIZE)

        # Load music and sounds
        pygame.mixer.music.load("res/music/title_theme.ogg")
        self.explosion_sound = pygame.mixer.Sound("res/sounds/explosion.wav")

        # Load images
        self.logo = pygame.image.load("res/images/title.png")
        self.logo = pygame.transform.scale(self.logo, [int(0.2 * s) for s in self.logo.get_size()])

        # Load font
        self.font = pygame.font.Font("res/fonts/bit5x5.ttf", 16)

        # Sprite groups
        self.sprites = pygame.sprite.Group()
        self.invaders = None
        self.player_missile = pygame.sprite.Group()

        # Sprites
        self.laser_cannon = None

    def title(self):
        self.game_state = GameState.TITLE
        # pygame.mixer.music.play(-1)  # -1 -> infinite repeat

        # Logo scaling variables
        logo_scale_bounds = (1, 1.15)
        logo_scale_factor = 0.01
        logo_scale = logo_scale_bounds[0]

        # Render font
        prompt_text = self.font.render("PRESS ENTER TO PLAY", True, SpaceInvaders.WHITE)

        # Title screen loop
        while self.game_state == GameState.TITLE:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_state = GameState.QUIT
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_state = GameState.QUIT
                    if event.key == K_RETURN or event.key == K_KP_ENTER:
                        # pygame.mixer.music.stop()
                        # self.explosion_sound.play()
                        self.play()

            # Black background
            self.screen.fill(SpaceInvaders.BLACK)

            # Draw and scale logo
            scaled_logo = pygame.transform.scale(self.logo, [int(logo_scale * s) for s in self.logo.get_size()])
            self.screen.blit(scaled_logo, centre_on_point((SpaceInvaders.ORIGIN[0], SpaceInvaders.ORIGIN[1] - 50), scaled_logo.get_size()))
            logo_scale += logo_scale_factor
            if not(logo_scale_bounds[0] < logo_scale < logo_scale_bounds[1]):
                logo_scale_factor = -logo_scale_factor

            # Draw font
            self.screen.blit(prompt_text, centre_on_point((SpaceInvaders.ORIGIN[0], SpaceInvaders.ORIGIN[1] + 100), prompt_text.get_size()))

            pygame.display.flip()
            self.clock.tick(SpaceInvaders.FPS)

        pygame.mixer.music.stop()

    def play(self):
        self.game_state = GameState.PLAYING

        # Create Laser Cannon
        self.laser_cannon = LaserCannon((SpaceInvaders.ORIGIN[0], SpaceInvaders.SCREEN_HEIGHT - 50))
        self.sprites.add(self.laser_cannon)

        # Create invaders and register event for invader update
        self.invaders = InvaderGroup((105, SpaceInvaders.ORIGIN[0] + 20))
        pygame.time.set_timer(USEREVENT, 500)

        # Game loop
        while self.game_state == GameState.PLAYING:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game_state = GameState.QUIT
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.game_state = GameState.QUIT
                if event.type == USEREVENT:
                    self.invaders.move(self.screen.get_rect())

            # Handle key presses
            keys = pygame.key.get_pressed()
            if any((keys[K_LEFT], keys[K_a])):
                self.laser_cannon.left()
            if any((keys[K_RIGHT], keys[K_d])):
                self.laser_cannon.right()
            if any((keys[K_UP], keys[K_SPACE], keys[K_w])) and len(self.player_missile.sprites()) == 0:
                self.player_missile.add(self.laser_cannon.shoot())

            # Handle player missile
            for missile in self.player_missile.sprites():
                if not missile.rect.colliderect(self.screen.get_rect()):
                    missile.kill()
                    continue

                # Move missile
                missile.update()

                # Try hit
                if missile.hit(self.invaders):
                    # self.explosion_sound.play()
                    pass

            # Win
            if len(self.invaders.sprites()) == 0:
              self.laser_cannon.kill()
              self.title()

            # Invader-LaserCannon game over collision
            for invader in self.invaders.sprites():
                if pygame.sprite.collide_mask(invader, self.laser_cannon):
                    self.laser_cannon.kill()
                    self.title()

            # Black background
            self.screen.fill(SpaceInvaders.BLACK)

            # Draw sprites
            self.sprites.draw(self.screen)
            self.invaders.draw(self.screen)
            self.player_missile.draw(self.screen)

            # Draw HUD
            points_text = self.font.render(f"POINTS: {self.laser_cannon.points}", True, SpaceInvaders.WHITE)
            self.screen.blit(points_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(SpaceInvaders.FPS)

# Utility centre function for non-sprites
def centre_on_point(point, size):
    x, y = point
    width, height = size
    return x - width/2, y - height/2


# Initialize SpaceInvaders game and start title screen
game = SpaceInvaders()
game.title()

