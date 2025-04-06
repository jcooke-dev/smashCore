"""
    This handles all the paddle settings and behavior and is a type of WorldObject.
"""

import pygame
import constants
from worldobject import WorldObject


class Paddle(WorldObject, pygame.sprite.Sprite):
    """ Paddle is derived from a sprite """

    def __init__(self, color, width, height, image = None):
        """ Initialization of paddle """
        super().__init__()

        # Set starting location for paddle in the bottom center of screen
        self.rect = pygame.Rect([((constants.WIDTH/2) - (width/2)), (constants.HEIGHT - height - constants.PADDLE_START_POSITION_OFFSET), width, height])
        self.color = color
        self.image = image

        self.commanded_pos_x = 0

    # update the WorldObject's pos, vel, acc, etc. (and possibly GameState)
    def update_wo(self, gs, ps):
        self.move_to_x(self.commanded_pos_x)

    # draw the WorldObject to the screen
    def draw_wo(self, screen):
        if self.image is None:
            pygame.draw.rect(screen, self.color, self.rect, 0, 7)
        else:
            paddle_scale = pygame.transform.scale(self.image,
                                                  [constants.PAD_WIDTH + 5,
                                                   constants.PAD_HEIGHT + 5])
            screen.blit(paddle_scale.convert_alpha(),
                        (self.rect.x - 2.2, self.rect.y - 1.1))


    # incremental Paddle movement (likely used for KB control)
    def move_left(self, pixels):
        """ Move paddle left by pixels """
        self.rect.x -= pixels
        # Check that the paddle is not going too far (off the screen)
        if self.rect.x < 0:
            self.rect.x = 0

    # incremental Paddle movement (likely used for KB control)
    def move_right(self, pixels):
        """ Move paddle right by pixels """
        self.rect.x += pixels
        # Check that the paddle is not going too far (off the screen)
        if self.rect.x > constants.WIDTH - constants.PAD_WIDTH:
            self.rect.x = constants.WIDTH - constants.PAD_WIDTH

    # absolute Paddle position setting (based on mouse position)
    def move_to_x(self, posx):
        """ Move paddle to mouse_position """
        self.rect.centerx = posx
        # Check that the paddle is not going too far (off the screen)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > constants.WIDTH:
            self.rect.right = constants.WIDTH

