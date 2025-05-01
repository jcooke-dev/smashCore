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
from gamesettings import GameSettings
from gamestate import GameState
from playerstate import PlayerState
from leaderboard import Leaderboard
from worldobject import WorldObject


class Paddle(WorldObject, pygame.sprite.Sprite):
    """ The Paddle object used to keep the ball in play """

    def __init__(self, color: pygame.color, width: int, height: int, image: pygame.image = None) -> None:
        """
        Initialization of paddle

        :param color:
        :param width:
        :param height:
        :param image:
        """
        super().__init__()

        # Set starting location for paddle in the bottom center of screen
        self.rect: pygame.rect = pygame.Rect([((constants.WIDTH / 2) - (width / 2)),
                                              (constants.HEIGHT - (height * 2) -
                                               constants.PADDLE_START_POSITION_OFFSET), width, height])

        self.color: pygame.color = color
        self.image: pygame.image = image

        self.commanded_pos_x: int = self.rect.centerx

        self.delta_x: int = 0
        self.prev_x: int = self.rect.x

    def update_wo(self, gs: GameState, ps: PlayerState, lb: Leaderboard, gset: GameSettings) -> None:
        """
        Update the Paddle's pos

        :param gset: GameSettings
        :param lb: Leaderboard
        :param gs: GameState
        :param ps: PlayerState
        :return:
        """

        old_x = self.rect.x

        # update pos based on arrow key commands (if using)
        if gs.paddle_under_key_control_left:
            self.commanded_pos_x -= constants.PADDLE_KEY_SPEED * gs.tick_time * gs.ball_speed_increased_ratio
            self.commanded_pos_x = max(self.commanded_pos_x, 0)
        if gs.paddle_under_key_control_right:
            self.commanded_pos_x += constants.PADDLE_KEY_SPEED * gs.tick_time * gs.ball_speed_increased_ratio
            self.commanded_pos_x = min(self.commanded_pos_x, constants.WIDTH)

        # reset this kind of latch so that the mouse can again control the paddle if an arrow key isn't pressed
        gs.paddle_under_key_control_left = False
        gs.paddle_under_key_control_right = False

        gs.paddle_pos_x = self.commanded_pos_x
        self.move_to_x(self.commanded_pos_x)

        # detects if the paddle is moving to the right or to the left for both keyboard and mouse controls
        if self.rect.x - old_x > 0:
            self.delta_x = 1
        elif self.rect.x - old_x < 0:
            self.delta_x = -1
        else:
            self.delta_x = 0

        self.prev_x = self.rect.x

    def draw_wo(self, screen: pygame.Surface) -> None:
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

    def move_left(self, pixels: int) -> None:
        """
        Incremental Paddle movement to the left (likely used for KB control)

        :param pixels: how far to move
        :return:
        """
        self.rect.x -= pixels
        # Check that the paddle is not going too far (off the screen)
        self.rect.x = max(self.rect.x, 0)

    def move_right(self, pixels: int) -> None:
        """
        Incremental Paddle movement to the right (likely used for KB control)

        :param pixels: how far to move
        :return:
        """
        self.rect.x += pixels
        # Check that the paddle is not going too far (off the screen)
        self.rect.x = min(self.rect.x, constants.WIDTH - constants.PAD_WIDTH)

    def move_to_x(self, posx: int) -> None:
        """
        Absolute Paddle position setting (based on mouse position)

        :param posx: posx movement command
        :return:
        """
        self.rect.centerx = posx
        # Check that the paddle is not going too far (off the screen)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, constants.WIDTH)
