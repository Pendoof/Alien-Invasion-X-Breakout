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
        self.original_image = pygame.image.load('images/dead_alien.jpg')
        self.image = self.original_image
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.death_y = self.y

        # Frame-based lifetime
        self.lifetime_frames = int(120 + uniform(-1, 1) * 60)
        self.frames_alive = 0

        # Explosion effect
        self.exploding = False
        self.explosion_duration = 30
        self.explosion_frame = 0

        # Add small randomization for movement
        self.sway_strength = uniform(0.5, 2.0)
        self.sway_speed = uniform(0.02, 0.07)
        self.phase = uniform(0, 2 * 3.14159)

    def check_edges(self):
        """Return True if alien is at edge or bottom of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0) or (self.rect.bottom >= screen_rect.bottom)
    
    def update(self):
        """Move the dead alien down and sway back and forth."""
        if not self.exploding:
            # Constant downward velocity
            self.y += self.settings.dead_alien_speed

            # Make alien slowly sway more as it falls
            dy = self.y - self.death_y
            sway_decay = min(1 + 0.005 * dy, 2)
            self.x += self.sway_strength * sway_decay * sin(self.sway_speed * dy + self.phase)
            self.x += 0.2 * cos(0.5 * self.sway_speed * dy + self.phase)
            self.rect.y = self.y
            self.rect.x = self.x

            # Remove alien after lifetime
            self.frames_alive += 1
            if self.frames_alive >= self.lifetime_frames or self.check_edges():
                self.exploding = True
                self.explosion_frame = 0
        else:
            # ship explodes doubling in size
            self.explosion_frame += 1
            scale_factor = 1 + self.explosion_frame / self.explosion_duration
            new_width = int(self.original_image.get_width() * scale_factor)
            new_height = int(self.original_image.get_height() * scale_factor)
            self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
            self.rect = self.image.get_rect(center=self.rect.center)

            if self.explosion_frame >= self.explosion_duration:
                self.kill()  # remove sprite after explosion
