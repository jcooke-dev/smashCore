"""
    This handles all the paddle settings and behavior and is a type of WorldObject.
"""

import pygame

import constants
from src.worldobject import WorldObject


class Paddle(WorldObject, pygame.sprite.Sprite):
    """ Paddle is derived from a sprite """

    def __init__(self, color, width, height):
        """ Initialization of paddle """
        super().__init__()

        # Pass in the color of the paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLACK)
        self.image.set_colorkey(constants.BLACK)

        # Draw the paddle as a rectangle.
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

        # Set starting location for paddle in the bottom center of screen
        self.rect.x = (constants.WIDTH/2) - (constants.PAD_WIDTH/2)
        self.rect.y = constants.HEIGHT - constants.PAD_HEIGHT - constants.PADDLE_START_POSITION_OFFSET

        self.commanded_pos_x = 0

    # update the WorldObject's pos, vel, acc, etc. (and possibly GameState)
    def update_wo(self, gs, ps):
        self.move_to_x(self.commanded_pos_x)

    # draw the WorldObject to the screen
    def draw_wo(self, screen):
        pygame.draw.rect(screen, constants.RED, self.rect, 0, 7)

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

