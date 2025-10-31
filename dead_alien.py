import pygame  # type: ignore

from pygame.sprite import Sprite  # type: ignore


class Dead_Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the dead alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the dead alien image and set its rect attribute.
        self.image = pygame.image.load('images/dead_alien.jpg')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact verticle position.
        self.y = float(self.rect.y)

    def update(self):
        """Move the dead alien down."""
        self.y += self.settings.dead_alien_speed
        self.rect.y = self.y