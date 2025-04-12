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

from src.worldobject import WorldObject

class Brick(WorldObject):
    """
    Brick to be lined up in rows and columns for the board
    They disappear when hit
    They have a size, color, and point value
    """

    def __init__(self, rect: pygame.rect, color: pygame.color, value: int = 1, image: pygame.image = None) -> None:
        """
        Initializes a Brick object.

        :param rect: The rectangle representing the brick's position and size.
        :param color: The RGB color of the brick.
        :param value: The score value of the brick.
        """
        super().__init__()

        self.strength: int = 1  # Number of hits required to break the brick
        self.rect: pygame.rect = pygame.Rect(rect)
        self.color: pygame.color = color
        self.value: int = value
        self.image: pygame.image = image


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

    def add_collision(self) -> None:
        """
        Reduces the brick's strength when it's hit.

        :return:
        """
        self.strength -= 1

    def should_remove(self) -> bool:
        """
        Returns True if the brick should be removed (strength <= 0).

        :return: bool indicating whether Brick should be removed
        """
        return self.strength <= 0
