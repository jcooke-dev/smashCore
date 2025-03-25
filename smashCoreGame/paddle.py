"""
    This handles all the paddle settings and behavior
"""
import pygame
import settings


class Paddle(pygame.sprite.Sprite):
    """ Paddle is derived from a sprite """

    def __init__(self, color, width, height):
        """ Initialization of paddle """
        super().__init__()

        # Pass in the color of the paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(settings.BLACK)
        self.image.set_colorkey(settings.BLACK)

        # Draw the paddle as a rectangle.
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def move_left(self, pixels):
        """ Move paddle left by pixels
            Check that the paddle is not going too far (off the screen)
        """
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self, pixels):
        """ Move paddle right by pixels
            Check that the paddle is not going too far (off the screen)
        """
        self.rect.x += pixels
        if self.rect.x > settings.WIDTH - settings.PAD_WIDTH:
            self.rect.x = settings.WIDTH - settings.PAD_WIDTH

    def move_by_mouse(self, mouse_position):
        self.rect.centerx = mouse_position
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > settings.WIDTH - settings.PAD_WIDTH:
            self.rect.x = settings.WIDTH - settings.PAD_WIDTH
