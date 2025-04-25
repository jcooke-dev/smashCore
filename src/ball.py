"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: The Ball type of WorldObject, with customized behavior.
"""

import random as rnd

import pygame
import constants
import paddle
from gamestate import GameState
from playerstate import PlayerState
from leaderboard import Leaderboard
from src import assets
from worldobject import WorldObject
from motionmodels import MotionModels


class Ball(WorldObject, pygame.sprite.Sprite):
    """ The ball object that collides with the paddle, walls, and bricks """

    def __init__(self, x: int, y: int, image=None) -> None:
        """
        Initialize ball with base values and primed for collisions

        :param x: x coordinate on the board
        :param y: y coordinate on the board
        :param image: if provided, draws the image, else a plain rect
        """
        super().__init__()

        # general world object properties
        self.can_react: bool = True #  allow object to react to collisions with other objects
        # ball settings
        self.radius: int = constants.BALL_RADIUS
        self.ball_rect: pygame.rect = self.radius * 2 ** 0.5
        self.image: pygame.image = image

        # SIMPLE_1 motion model defaults
        self.x: int = x - self.radius
        self.y: int = y
        self.dx: int = rnd.choice([1, -1])
        self.dy: int = -1
        self.speed: float = constants.BALL_SPEED_SIMPLE
        self.rect: pygame.rect.Rect = pygame.Rect(self.x, self.y, self.ball_rect, self.ball_rect)

        # VECTOR motion models defaults
        self.v_pos: pygame.Vector2 = pygame.Vector2(x - self.radius, y)
        self.v_vel_unit: pygame.Vector2 = pygame.Vector2(1.0, 0.0)
        self.v_vel_unit: pygame.Vector2 = self.v_vel_unit.rotate(rnd.choice([-45.0, -135.0]))
        self.speed_v: float = constants.BALL_SPEED_VECTOR
        self.v_vel: pygame.Vector2 = self.v_vel_unit * self.speed_v

        self.rect = pygame.Rect(self.v_pos.x, self.v_pos.y, self.ball_rect, self.ball_rect)

        # these flags act as indicators that the ball is primed for collision with the specific item
        self.primed_collision_wall_left: bool = True
        self.primed_collision_wall_right: bool = True
        self.primed_collision_wall_top: bool = True

        self.commanded_pos_x = 0

    def update_wo(self, gs: GameState, ps: PlayerState, lb: Leaderboard) -> None:
        """
        Update the WorldObject's pos, vel, acc, etc. (and possibly GameState)

        :param lb:
        :param gs: GameState
        :param ps: PlayerState
        :return:
        """
        if gs.cur_state == GameState.GameStateName.PLAYING:

            ##############################################################
            # perform the wall collision detection and overall position
            # update for the SIMPLE_1 model
            ##############################################################
            if gs.motion_model == MotionModels.SIMPLE_1:

                # ball collision wall left
                if self.rect.centerx < self.radius:
                    self.dx = -self.dx
                    assets.CHANNEL[3].play(assets.LEFT_WALL_SFX)
                # ball collision wall right
                if self.rect.centerx > constants.WIDTH - self.radius:
                    self.dx = -self.dx
                    assets.CHANNEL[4].play(assets.RIGHT_WALL_SFX)
                # ball collision wall top
                if self.rect.centery < self.radius:
                    self.dy = -self.dy
                    assets.CHANNEL[5].play(assets.TOP_WALL_SFX)

                self.rect.x += self.speed * self.dx
                self.rect.y += self.speed * self.dy

                self.x = self.rect.x
                self.y = self.rect.y

            ##############################################################
            # perform the wall collision detection and overall position
            # update for the VECTOR models
            ##############################################################
            elif gs.motion_model == MotionModels.VECTOR_1:

                # ball collision wall left
                if self.primed_collision_wall_left and (self.v_pos.x < self.radius):
                    self.primed_collision_wall_left = False
                    self.v_vel_unit.x = -self.v_vel_unit.x
                    self.v_vel.x = -self.v_vel.x
                    assets.CHANNEL[3].play(assets.LEFT_WALL_SFX)
                # reset the latch allowing collision detection since the ball has moved fully away
                if self.v_pos.x >= self.radius:
                    self.primed_collision_wall_left = True

                # ball collision wall right
                if self.primed_collision_wall_right and (self.v_pos.x > (constants.WIDTH - self.radius)):
                    self.primed_collision_wall_right = False
                    self.v_vel_unit.x = -self.v_vel_unit.x
                    self.v_vel.x = -self.v_vel.x
                    assets.CHANNEL[4].play(assets.RIGHT_WALL_SFX)
                # reset the latch allowing collision detection since the ball has moved fully away
                if self.v_pos.x <= (constants.WIDTH - self.radius):
                    self.primed_collision_wall_right = True

                # ball collision wall top
                if self.primed_collision_wall_top and (self.v_pos.y < self.radius):
                    self.primed_collision_wall_top = False
                    self.v_vel_unit.y = -self.v_vel_unit.y
                    self.v_vel.y = -self.v_vel.y
                    assets.CHANNEL[5].play(assets.TOP_WALL_SFX)
                # reset the latch allowing collision detection since the ball
                # has moved fully away
                if self.v_pos.y >= self.radius:
                    self.primed_collision_wall_top = True

                # WORLD_GRAVITY_ACC: apply gravity, if any
                if gs.gravity_acc_length > 0.0:
                    self.v_vel += gs.v_gravity_acc * gs.tick_time * 1.0
                    self.v_vel_unit = self.v_vel.normalize()

                self.v_pos += self.v_vel * gs.tick_time * 1.0

                self.rect.x = int(self.v_pos.x)
                self.rect.y = int(self.v_pos.y)

                self.x = self.rect.x
                self.y = self.rect.y

        else:
            self.move_to_x(self.commanded_pos_x)

        gs.cur_ball_x = self.x

        # Decrement lives everytime ball goes below the window and resets its
        # position to above the paddle.
        # Prompts for SPACEBAR key to continue the game
        if self.rect.top > constants.HEIGHT:
            ps.lives -= 1
            self.reset_position()
            gs.cur_state = GameState.GameStateName.READY_TO_LAUNCH

            # Displays game_over menu if user loses all of their lives
            if ps.lives <= 0:
                # collects the player's initials if this is a high score
                if lb.is_high_score(ps.score):
                    gs.cur_state = GameState.GameStateName.GET_HIGH_SCORE
                else:
                    gs.cur_state = GameState.GameStateName.GAME_OVER

    def draw_wo(self, screen: pygame.Surface) -> None:
        """
        Draw the WorldObject/Ball to the screen

        :param screen:
        :return:
        """
        if self.image is None:
            pygame.draw.circle(screen, constants.WHITE, self.rect.center, self.radius)
        else:
            screen.blit(self.image.convert_alpha(), (self.rect.x - 4, self.rect.y - 3.15))

    def reset_position(self) -> None:
        """
        Resets the position of the ball

        :return:
        """
        # SIMPLE_1 motion model defaults
        self.rect.x = self.commanded_pos_x
        self.rect.y = (constants.HEIGHT - constants.PAD_HEIGHT -
                        constants.PADDLE_START_POSITION_OFFSET - (constants.BALL_RADIUS * 3))
        self.dx = rnd.choice([1, -1])
        self.dy = -1

        # VECTOR motion models defaults
        self.v_pos = pygame.Vector2(self.commanded_pos_x,
                             (constants.HEIGHT - constants.PAD_HEIGHT -
                              constants.PADDLE_START_POSITION_OFFSET - (constants.BALL_RADIUS * 3)))
        self.rect.x = int(self.v_pos.x)
        self.rect.y = int(self.v_pos.y)

        self.v_vel_unit = pygame.Vector2(1.0, 0.0)
        self.v_vel_unit = self.v_vel_unit.rotate(rnd.choice([-45.0, -135.0]))
        self.v_vel = self.v_vel_unit * self.speed_v

    def detect_collision(self, wo: pygame.rect, gs: GameState) -> None:
        """
        Detects collisions between the ball and other objects

        :param wo: another world_object
        :param gs: GameState
        :return:
        """
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

            if isinstance(wo, paddle.Paddle):
                assets.CHANNEL[6].play(assets.PADDLE_SFX)

        ##############################################################
        # determine how/which direction to bounce after collision under
        # the VECTOR models
        ##############################################################
        elif gs.motion_model == MotionModels.VECTOR_1:

            if self.v_vel_unit.x > 0:  # checks for horizontal ball collision
                x_delta = self.rect.right - wo.rect.left
            else:
                x_delta = wo.rect.right - self.rect.left

            if self.v_vel_unit.y > 0:  # checks for vertical ball collision
                y_delta = self.rect.bottom - wo.rect.top
            else:
                y_delta = wo.rect.bottom - self.rect.top

            if abs(x_delta - y_delta) < 10:
                self.v_vel_unit.x = -self.v_vel_unit.x
                self.v_vel.x = -self.v_vel.x
                self.v_vel_unit.y = -self.v_vel_unit.y
                self.v_vel.y = -self.v_vel.y
            # TODO check - this logic seems backwards, but works?
            elif x_delta > y_delta:  # vertical collision
                # elif y_delta > x_delta:  # vertical collision
                self.v_vel_unit.y = -self.v_vel_unit.y
                self.v_vel.y = -self.v_vel.y
            # TODO check - this logic seems backwards, but works?
            elif y_delta > x_delta:  # horizontal collision
                # elif x_delta > y_delta:  # horizontal collision
                self.v_vel_unit.x = -self.v_vel_unit.x
                self.v_vel.x = -self.v_vel.x

            # PADDLE_IMPULSE: add an impulse to the ball's velocity when
            # striking the paddle, similar to brick breaking
            if isinstance(wo, paddle.Paddle) and (gs.paddle_impulse_vel_length > 0.0):
                # add a 'push' straight up
                v_impulse = pygame.Vector2(0.0, -gs.paddle_impulse_vel_length)
                self.v_vel += v_impulse
                self.speed_v = self.v_vel.magnitude()
                gs.ball_speed_increased_ratio = self.speed_v / constants.BALL_SPEED_VECTOR
                self.v_vel_unit = self.v_vel.normalize()

            if isinstance(wo, paddle.Paddle):
                assets.CHANNEL[6].play(assets.PADDLE_SFX)

    def move_to_x(self, pos_x: int) -> None:
        """
        Move ball_x to mouse_position
        Used when repositioning the ball when game is no longer in the
        PLAYING state

        :param pos_x: move Ball to this x position
        :return:
        """
        self.rect.x = pos_x

        # Check that the paddle is not going too far (off the screen)
        self.rect.left = max(self.rect.left, constants.PAD_WIDTH // 2 - self.radius)
        self.rect.right = min(self.rect.right, constants.WIDTH - constants.PAD_WIDTH // 2 + self.radius)

        self.v_pos.x = self.rect.x
        self.x = self.rect.x
