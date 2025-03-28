"""
    The Ball type of WorldObject that customizes the behavior.
"""

import pygame
from random import randrange as rnd

import constants
from src.worldobject import WorldObject


class Ball(WorldObject):

    def __init__(self):

        super().__init__()

        # general world object properties
        self.can_react = True # can this object react to collisions with other objects?

        # ball settings
        self.ball_radius = 15.0
        self.ball_speed = 6.0
        ball_rect = int(self.ball_radius * 2 ** 0.5)
        ball_x = rnd(ball_rect, constants.WIDTH - ball_rect)
        ball_y = constants.HEIGHT / 2.0
        self.rect = pygame.Rect(ball_x, ball_y, ball_rect, ball_rect)
        self.dx, self.dy = 1.0, -1.0
        self.mouse_position = 0 # unused with this ball

    # update the WorldObject's pos, vel, acc, etc. (and possibly GameState)
    def update_wo(self, gs):

        # ball collision wall left/right
        if self.rect.centerx < self.ball_radius or self.rect.centerx > constants.WIDTH - self.ball_radius:
            self.dx = -self.dx
        # ball collision wall top
        if self.rect.centery < self.ball_radius:
            self.dy = -self.dy

        # # DEBUG and bounce off just below the bottom
        # if self.rect.centery > constants.HEIGHT + (8 * self.ball_radius):
        #     self.dy = -self.dy

        self.rect.x += self.ball_speed * self.dx
        self.rect.y += self.ball_speed * self.dy

        # win, game over
        if self.rect.top > constants.HEIGHT: # + (10 * self.ball_radius):
        # if self.rect.top < 0:
            gs.game_over = True

    # draw the WorldObject to the screen
    def draw_wo(self, screen):
        pygame.draw.circle(screen, pygame.Color('white'), self.rect.center, self.ball_radius)

