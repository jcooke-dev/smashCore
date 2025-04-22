"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: The Obstacle type of WorldObject, with customized behavior.
"""
import pygame
import constants
from worldobject import WorldObject


class Obstacle(WorldObject):
    """
    Obstacle to be placed on the board
    They have a size, color
    """

    def __init__(self, rect: pygame.rect, color: pygame.color,
                 image: pygame.image = None, text: str = "") -> None:
        """
        Initializes an Obstacle object.

        :param rect: The rectangle representing the brick's position and size.
        :param color: The RGB color of the brick.
        :param value: The score value of the brick.
        """
        super().__init__()

        self.rect: pygame.rect = pygame.Rect(rect)
        self.color: pygame.color = color
        self.image: pygame.image = image
        self.text: str = text

    def draw_wo(self, screen: pygame.Surface) -> None:
        """
        Draws the obstacle to the screen.
        If text was present then it is printed on to obstacle

        :param screen:
        :return:
        """
        if self.image is None:
            pygame.draw.rect(screen, self.color, self.rect)
        else:
            screen.blit(self.image, self.rect)
        if self.text.strip != "":
            font_text = pygame.font.SysFont("Courier",
                                                     self.rect.height - 20,
                                                     True)
            text_surface = font_text.render(self.text, True,
                                                     constants.BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
