"""
    This handles all the paddle settings and behavior
"""
import pygame
from settings import BLACK
from settings import WIDTH, HEIGHT, PAD_WIDTH, PAD_HEIGHT, \
    PADDLE_START_POSITION_OFFSET


class Paddle(pygame.sprite.Sprite):
    """ Paddle is derived from a sprite """

    def __init__(self, color, width, height):
        """ Initialization of paddle """
        super().__init__()

        # Pass in the color of the paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle as a rectangle.
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

        # Set starting location for paddle in the bottom center of screen
        self.rect.x = (WIDTH/2) - (PAD_WIDTH/2)
        self.rect.y = HEIGHT - PAD_HEIGHT - PADDLE_START_POSITION_OFFSET

    def move_left(self, pixels):
        """ Move paddle left by pixels """
        self.rect.x -= pixels
        # Check that the paddle is not going too far (off the screen)
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self, pixels):
        """ Move paddle right by pixels """
        self.rect.x += pixels
        # Check that the paddle is not going too far (off the screen)
        if self.rect.x > WIDTH - PAD_WIDTH:
            self.rect.x = WIDTH - PAD_WIDTH

    def move_by_mouse(self, mouse_position):
        """ Move paddle to mouse_position """
        self.rect.centerx = mouse_position
        # Check that the paddle is not going too far (off the screen)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
