"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: The Brick type of WorldObject, with customized behavior.
"""

import pygame
import constants
from worldobject import WorldObject

class Brick(WorldObject):
    """
    Brick to be lined up in rows and columns for the board
    They disappear when hit
    They have a size, color, and point value
    """

    def __init__(self, rect: pygame.rect, color: pygame.color, value: int = 1,
                 image: pygame.image = None,
                 strength: int = 1, bonus: int = 0) -> None:
        """
        Initializes a Brick object.

        :param rect: The rectangle representing the brick's position and size.
        :param color: The RGB color of the brick.
        :param value: The score value of the brick.
        """
        super().__init__()

        self.rect: pygame.rect = pygame.Rect(rect)
        self.color: pygame.color = color
        self.value: int = value
        self.image: pygame.image = image
        self.strength: int = strength  # Number of hits required to break the brick
        self.bonus = bonus

    def _add_strength_indicator(self, screen: pygame.Surface) -> None:
        if self.bonus > 0:
            self.font_strength = pygame.font.SysFont("Courier",
                                                     self.rect.height - 20,
                                                     True)
            text_surface = self.font_strength.render(str(self.strength), True,
                                                     constants.BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def draw_wo(self, screen: pygame.Surface) -> None:
        """
        Draws the brick to the screen.

        :param screen:
        :return:
        """
        if self.image is None:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            screen.blit(self.image, self.rect)
        self._add_strength_indicator(screen)

    def add_collision(self) -> None:
        """
        Reduces the brick's strength when it's hit.

        :return:
        """
        self.strength -= 1

    def should_score(self) -> bool:
        return True

    def should_remove(self) -> bool:
        """
        Returns True if the brick should be removed (strength <= 0).

        :return: bool indicating whether Brick should be removed
        """
        return self.strength <= 0
