"""
    The Ball type of WorldObject that customizes the behavior.
"""

import pygame
from pygame import Vector2

import constants
import random as rnd

import src.paddle
from src.worldobject import WorldObject
from gamestates import GameStates
from motionmodels import MotionModels


class Ball(WorldObject, pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        # general world object properties
        self.can_react = True  # can this object react to collisions with other objects?
        # ball settings
        self.radius = constants.BALL_RADIUS
        self.ball_rect = int(self.radius * 2 ** 0.5)

        # SIMPLE_1 motion model defaults
        self.x = x - self.radius
        self.y = y
        self.dx = rnd.choice([1, -1])
        self.dy = -1
        self.speed = constants.BALL_SPEED_SIMPLE
        self.rect = pygame.Rect(self.x, self.y, self.ball_rect, self.ball_rect)

        # VECTOR motion models defaults
        self.vPos = Vector2(x - self.radius, y)
        self.vVelUnit = Vector2(1.0, 0.0)
        self.vVelUnit = self.vVelUnit.rotate(rnd.choice([-45.0, -135.0]))
        self.speedV = constants.BALL_SPEED_VECTOR
        self.vVel = self.vVelUnit * self.speedV
        self.vAccUnit = Vector2(0.0, 1.0)
        self.vAcc = self.vAccUnit * constants.WORLD_GRAVITY_ACC

        self.rect = pygame.Rect(self.vPos.x, self.vPos.y, self.ball_rect, self.ball_rect)

        # these flags act as indicators that the ball is primed for collision with the specific item
        self.primed_collision_wall_left = True
        self.primed_collision_wall_right = True
        self.primed_collision_wall_top = True

        self.mouse_position = 0  # unused with this ball

    # update the WorldObject's pos, vel, acc, etc. (and possibly GameState)
    def update_wo(self, gs, ps):

        if gs.cur_state == GameStates.PLAYING:

            ##############################################################
            # perform the wall collision detection and overall position
            # update for the SIMPLE_1 model
            ##############################################################
            if gs.motion_model == MotionModels.SIMPLE_1:

                # ball collision wall left/right
                if self.rect.centerx < self.radius or self.rect.centerx > constants.WIDTH - self.radius:
                    self.dx = -self.dx
                # ball collision wall top
                if self.rect.centery < self.radius:
                    self.dy = -self.dy

                self.rect.x += self.speed * self.dx
                self.rect.y += self.speed * self.dy

                self.x = self.rect.x
                self.y = self.rect.y

            ##############################################################
            # perform the wall collision detection and overall position
            # update for the VECTOR models
            ##############################################################
            elif (gs.motion_model == MotionModels.VECTOR_1) or (gs.motion_model == MotionModels.VECTOR_2):

                # ball collision wall left
                if self.primed_collision_wall_left and (self.vPos.x < self.radius):
                    self.primed_collision_wall_left = False
                    self.vVelUnit.x = -self.vVelUnit.x
                    self.vVel.x = -self.vVel.x
                # reset the latch allowing collision detection since the ball has moved fully away
                if self.vPos.x >= self.radius:
                    self.primed_collision_wall_left = True

                # ball collision wall right
                if self.primed_collision_wall_right and (self.vPos.x > (constants.WIDTH - self.radius)):
                    self.primed_collision_wall_right = False
                    self.vVelUnit.x = -self.vVelUnit.x
                    self.vVel.x = -self.vVel.x
                # reset the latch allowing collision detection since the ball has moved fully away
                if self.vPos.x <= (constants.WIDTH - self.radius):
                    self.primed_collision_wall_right = True

                # ball collision wall top
                if self.primed_collision_wall_top and (self.vPos.y < self.radius):
                    self.primed_collision_wall_top = False
                    self.vVelUnit.y = -self.vVelUnit.y
                    self.vVel.y = -self.vVel.y
                # reset the latch allowing collision detection since the ball has moved fully away
                if self.vPos.y >= self.radius:
                    self.primed_collision_wall_top = True

                # apply gravity, if selected
                if gs.motion_model == MotionModels.VECTOR_2:
                    self.vVel += self.vAcc * gs.tick_time * 1.0
                    self.vVelUnit = self.vVel.normalize()

                self.vPos += self.vVel * gs.tick_time * 1.0

                self.rect.x = self.vPos.x
                self.rect.y = self.vPos.y

                self.x = self.rect.x
                self.y = self.rect.y

        else:
            self.move_by_mouse(self.mouse_position)

        # decrements lives everytime ball goes below the window and resets its position to
        # above the paddle. Prompts for SPACEBAR key to continue the game
        if self.rect.top > constants.HEIGHT:
            ps.lives -= 1
            self.reset_position()
            gs.cur_state = GameStates.READY_TO_LAUNCH

            # Displays game_over menu if user loses all of their lives
            if ps.lives <= 0:
                gs.cur_state = GameStates.GAME_OVER

    # draw the WorldObject to the screen
    def draw_wo(self, screen):
        pygame.draw.circle(screen, constants.WHITE, self.rect.center, self.radius)

    def reset_position(self):

        # SIMPLE_1 motion model defaults
        self.rect.center = self.mouse_position, (constants.HEIGHT - constants.PAD_HEIGHT -
                                                 constants.PADDLE_START_POSITION_OFFSET - (constants.BALL_RADIUS * 3))
        self.dx = rnd.choice([1, -1])
        self.dy = -1

        # VECTOR motion models defaults
        self.vPos = Vector2(self.mouse_position, (constants.HEIGHT - constants.PAD_HEIGHT -
                                                 constants.PADDLE_START_POSITION_OFFSET - (constants.BALL_RADIUS * 3)))
        self.rect.center = (self.vPos.x, self.vPos.y)

        self.vVelUnit = Vector2(1.0, 0.0)
        self.vVelUnit = self.vVelUnit.rotate(rnd.choice([-45.0, -135.0]))
        self.vVel = self.vVelUnit * self.speedV
        self.vAccUnit = Vector2(0.0, 1.0)
        self.vAcc = self.vAccUnit * constants.WORLD_GRAVITY_ACC

    #Function to detect collisions
    def detect_collision(self, wo, gs):

        ##############################################################
        # determine how/which direction to bounce after collision under
        # the SIMPLE_1 model
        ##############################################################
        if gs.motion_model == MotionModels.SIMPLE_1:

            if self.dx > 0:  # checks for horizontal ball collision
                x_delta = self.rect.right - wo.rect.left
            else:
                x_delta = wo.rect.right - self.rect.left

            if self.dy > 0:  # checks for vertical ball collision
                y_delta = self.rect.bottom - wo.rect.top
            else:
                y_delta = wo.rect.bottom - self.rect.top

            if abs(x_delta - y_delta) < 10:
                self.dx, self.dy = -self.dx, -self.dy
            elif x_delta > y_delta:  # vertical collision
                self.dy = -self.dy
            elif y_delta > x_delta:  # horizontal collision
                self.dx = -self.dx

        ##############################################################
        # determine how/which direction to bounce after collision under
        # the VECTOR models
        ##############################################################
        elif (gs.motion_model == MotionModels.VECTOR_1) or (gs.motion_model == MotionModels.VECTOR_2):

            if self.vVelUnit.x > 0:  # checks for horizontal ball collision
                x_delta = self.rect.right - wo.rect.left
            else:
                x_delta = wo.rect.right - self.rect.left

            if self.vVelUnit.y > 0:  # checks for vertical ball collision
                y_delta = self.rect.bottom - wo.rect.top
            else:
                y_delta = wo.rect.bottom - self.rect.top

            if abs(x_delta - y_delta) < 10:
                self.vVelUnit.x = -self.vVelUnit.x
                self.vVel.x = -self.vVel.x
                self.vVelUnit.y = -self.vVelUnit.y
                self.vVel.y = -self.vVel.y
            # TODO check - this logic seems backwards, but works?
            elif x_delta > y_delta:  # vertical collision
            # elif y_delta > x_delta:  # vertical collision
                self.vVelUnit.y = -self.vVelUnit.y
                self.vVel.y = -self.vVel.y
            # TODO check - this logic seems backwards, but works?
            elif y_delta > x_delta:  # horizontal collision
            # elif x_delta > y_delta:  # horizontal collision
                self.vVelUnit.x = -self.vVelUnit.x
                self.vVel.x = -self.vVel.x

            # add an impulse to the ball's velocity when striking the paddle, just like with brick breaking
            if isinstance(wo, src.paddle.Paddle) and (gs.motion_model == MotionModels.VECTOR_2):
                self.speedV += constants.PADDLE_IMPULSE
                self.vVel = self.vVelUnit * self.speedV


    def move_by_mouse(self, mouse_position):
        """ Move ball_x to mouse_position """
        self.rect.centerx = mouse_position
        self.vPos.x = self.rect.centerx
        self.vPos.y = self.rect.centery

        # Check that the paddle is not going too far (off the screen)
        if self.rect.left < (constants.PAD_WIDTH // 2) - self.radius:
            self.rect.left = (constants.PAD_WIDTH // 2) - self.radius
        if self.rect.right > constants.WIDTH - (constants.PAD_WIDTH // 2) + self.radius:
            self.rect.right = constants.WIDTH - (constants.PAD_WIDTH // 2) + self.radius
