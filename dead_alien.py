import pygame  # type: ignore
from random import uniform
from math import sin, cos

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

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.death_y = self.y

        # Add small randomization for movement
        self.sway_strength = uniform(0.5, 2.0)
        self.sway_speed = uniform(0.02, 0.07)
        self.phase = uniform(0, 2 * 3.14159)

    def update(self):
        """Move the dead alien down and sway back and forth."""

        # Constant downward velocity
        self.y += self.settings.dead_alien_speed

        # Make alien slowly sway more as it falls
        dy = self.y - self.death_y
        sway_decay = min(1 + 0.005 * dy, 2)
        self.x += self.sway_strength * sway_decay * sin(self.sway_speed * dy + self.phase)
        self.x += 0.2 * cos(0.5 * self.sway_speed * dy + self.phase)
        self.rect.y = self.y
        self.rect.x = self.x