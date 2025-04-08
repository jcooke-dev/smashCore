"""
    The Brick type of WorldObject that customizes the behavior.
"""

import pygame

from src.worldobject import WorldObject

class Brick(WorldObject):

    def __init__(self, rect, color, value=1, image=None):
        """
        Initializes a Brick object.

        Args:
            rect (pygame.Rect): The rectangle representing the brick's position and size.
            color (tuple): The RGB color of the brick.
            value (int): The score value of the brick.
        """
        super().__init__()

        self.strength = 1  # Number of hits required to break the brick
        self.rect = pygame.Rect(rect)
        self.color = color
        self.value = value
        self.image = image

    def draw_wo(self, screen):
        """Draws the brick to the screen."""
        if self.image is None:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            screen.blit(self.image.convert_alpha(), self.rect)

    def add_collision(self):
        """Reduces the brick's strength when it's hit."""
        self.strength -= 1

    def should_remove(self):
        """Returns True if the brick should be removed (strength <= 0)."""
        return self.strength <= 0
