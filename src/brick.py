"""
    The Brick type of WorldObject that customizes the behavior.
"""

import pygame

from src.worldobject import WorldObject


class Brick(WorldObject):

    def __init__(self, rect, color):

        super().__init__()

        self.strength = 1 # require this many hits before removing brick
        self.rect = pygame.Rect(rect)
        self.color = color
        self.value = 1

    # draw the WorldObject to the screen
    def draw_wo(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    # this handles 'hammering' at the brick to weaken/break it (based on the self.strength
    def add_collision(self):
        self.strength -= 1

    # informs the caller that the brick is dead and should be removed
    def should_remove(self):
        return self.strength <= 0