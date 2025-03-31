"""
    The Ball type of WorldObject that customizes the behavior.
"""

import pygame

import constants
import random as rnd
from src.worldobject import WorldObject


class Ball(WorldObject, pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        # general world object properties
        self.can_react = True  # can this object react to collisions with other objects?
        # ball settings
        self.radius = constants.BALL_RADIUS
        self.speed = constants.BALL_SPEED
        self.x = x - self.radius
        self.y = y
        self.ball_rect = int(self.radius * 2 ** 0.5)
        self.dx = rnd.choice([1, -1])
        self.dy = -1
        self.rect = pygame.Rect(self.x, self.y, self.ball_rect, self.ball_rect)
        self.mouse_position = 0  # unused with this ball

    # update the WorldObject's pos, vel, acc, etc. (and possibly GameState)
    def update_wo(self, gs):

        # ball collision wall left/right
        if self.rect.centerx < self.radius or self.rect.centerx > constants.WIDTH - self.radius:
            self.dx = -self.dx
        # ball collision wall top
        if self.rect.centery < self.radius:
            self.dy = -self.dy

        # # DEBUG and bounce off just below the bottom
        # if self.rect.centery > constants.HEIGHT + (8 * self.ball_radius):
        #     self.dy = -self.dy
        if gs.game_start:
            self.rect.x += self.speed * self.dx
            self.rect.y += self.speed * self.dy

            self.x = self.rect.x
            self.y = self.rect.y
        else:
            self.move_by_mouse(self.mouse_position)

        # win, game over
        # if self.rect.top > constants.HEIGHT:
        #     constants.START_LIVES -= 1
        #     self.reset_position()
        #     if constants.START_LIVES <= 0:
        #         gs.game_over = True

    # draw the WorldObject to the screen
    def draw_wo(self, screen):
        pygame.draw.circle(screen, constants.WHITE, self.rect.center, self.radius)

    def reset_position(self):
        self.rect.center = self.mouse_position, (constants.HEIGHT - constants.PAD_HEIGHT -
                                                 constants.PADDLE_START_POSITION_OFFSET - (constants.BALL_RADIUS * 3))
        self.dx = rnd.choice([1, -1])
        self.dy = -1

    #Function to detect collisions      
    def detect_collision(self, hitbox):
        if self.dx > 0:  # checks for horizontal ball collision
            x_delta = self.rect.right - hitbox.left
        else:
            x_delta = hitbox.right - self.rect.left

        if self.dy > 0:  # checks for vertical ball collision
            y_delta = self.rect.bottom - hitbox.top
        else:
            y_delta = hitbox.bottom - self.rect.top

        # Collision type
        if abs(x_delta - y_delta) < 10:
            self.dx, self.dy = -self.dx, -self.dy
        elif x_delta > y_delta:  # vertical collision
            self.dy = -self.dy
        elif y_delta > x_delta:  # horizontal collision
            self.dx = -self.dx

    def move_by_mouse(self, mouse_position):
        """ Move ball_x to mouse_position """
        self.rect.centerx = mouse_position
        # Check that the paddle is not going too far (off the screen)
        if self.rect.left < (constants.PAD_WIDTH // 2) - self.radius:
            self.rect.left = (constants.PAD_WIDTH // 2) - self.radius
        if self.rect.right > constants.WIDTH - (constants.PAD_WIDTH // 2) + self.radius:
            self.rect.right = constants.WIDTH - (constants.PAD_WIDTH // 2) + self.radius
