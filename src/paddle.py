"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: The Paddle type of WorldObject, with customized behavior.
"""

import pygame
import constants
from worldobject import WorldObject


class Paddle(WorldObject, pygame.sprite.Sprite):
    """ The Paddle object used to keep the ball in play """

    def __init__(self, color, width, height, image = None):
        """
        Initialization of paddle

        :param color:
        :param width:
        :param height:
        :param image:
        """
        super().__init__()

        # Set starting location for paddle in the bottom center of screen
        self.rect = pygame.Rect([((constants.WIDTH/2) - (width/2)), (constants.HEIGHT - height - constants.PADDLE_START_POSITION_OFFSET), width, height])
        self.color = color
        self.image = image

        self.commanded_pos_x = 0

    def update_wo(self, gs, ps):
        """
        Update the Paddle's pos

        :param gs: GameState
        :param ps: PlayerState
        :return:
        """
        self.move_to_x(self.commanded_pos_x)

    def draw_wo(self, screen):
        """
        Draw the Paddle to the screen

        :param screen:
        :return:
        """
        if self.image is None:
            pygame.draw.rect(screen, self.color, self.rect, 0, 7)
        else:
            paddle_scale = pygame.transform.scale(self.image,
                                                  [constants.PAD_WIDTH + 5,
                                                   constants.PAD_HEIGHT + 5])
            screen.blit(paddle_scale.convert_alpha(),
                        (self.rect.x - 2.2, self.rect.y - 1.1))


    def move_left(self, pixels):
        """
        Incremental Paddle movement to the left (likely used for KB control)

        :param pixels: how far to move
        :return:
        """
        self.rect.x -= pixels
        # Check that the paddle is not going too far (off the screen)
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self, pixels):
        """
        Incremental Paddle movement to the right (likely used for KB control)

        :param pixels: how far to move
        :return:
        """
        self.rect.x += pixels
        # Check that the paddle is not going too far (off the screen)
        if self.rect.x > constants.WIDTH - constants.PAD_WIDTH:
            self.rect.x = constants.WIDTH - constants.PAD_WIDTH

    def move_to_x(self, posx):
        """
        Absolute Paddle position setting (based on mouse position)

        :param posx: posx movement command
        :return:
        """
        self.rect.centerx = posx
        # Check that the paddle is not going too far (off the screen)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > constants.WIDTH:
            self.rect.right = constants.WIDTH

