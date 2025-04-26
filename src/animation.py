"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: The Animation type of WorldObject, with various customizable aspects.
"""

import pygame
from pygame import Vector2, Color, SRCALPHA

from gamestate import GameState
from leaderboard import Leaderboard
from playerstate import PlayerState
from worldobject import WorldObject

class Animation(WorldObject, pygame.sprite.Sprite):
    """
    Animation objects can be dropped into the world and then controlled in various ways: lifetime, static shape or image,
    animation frames, fade, velocity, etc.
    """

    def __init__(self, duration: int, rect: pygame.rect, color: Color, fade: bool = False, v_vel: Vector2 = Vector2(0.0, 0.0),
                 v_acc: Vector2 = Vector2(0.0, 0.0), images: list[pygame.image] = None ) -> None:
        """
        Initializes an Animation object.

        :param duration: lifetime in ms
        :param rect: The rectangle representing the animation's static position and size.
        :param color: The RGB color of the animation.
        :param fade: Should the animation fade?
        :param v_vel: velocity vector of animation
        :param v_acc: acceleration vector of animation
        :param images: list of animation image frames

        """
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.primed_collision = False

        self.start_ticks: float = pygame.time.get_ticks()
        self.cur_ticks: float = self.start_ticks
        self.duration: int = duration

        self.fade: bool = fade
        self.alpha: int = 255

        self.rect: pygame.rect = pygame.Rect(rect)
        self.v_pos: Vector2 = Vector2(self.rect.x, self.rect.y)
        self.v_vel: Vector2 = v_vel
        self.v_acc: Vector2 = v_acc

        self.color: Color = color
        self.images: list[pygame.image] = images
        self.num_images: int = 0 if self.images is None else len(self.images)
        self.images_index: int = 0

    def update_wo(self, gs: GameState, ps: PlayerState, lb: Leaderboard) -> None:
        """
        Update the WorldObject's pos, vel, acc, and image info (alpha, animation frame)

        :param lb: Leaderboard
        :param gs: GameState
        :param ps: PlayerState
        :return:
        """

        self.cur_ticks = pygame.time.get_ticks()

        if self.v_acc.magnitude() > 0.0:
            self.v_vel += self.v_acc * gs.tick_time

        if self.v_vel.magnitude() > 0.0:
            self.v_pos += self.v_vel * gs.tick_time

        self.rect.x = int(self.v_pos.x)
        self.rect.y = int(self.v_pos.y)

        # if fade, calculate alpha increment
        if self.fade:
            self.alpha = int(255 - (((self.cur_ticks - self.start_ticks) / self.duration) * 255))
            self.alpha = max(min(self.alpha, 255), 0)

        # sequence through animation frames
        if (self.images is not None) and (self.num_images >= 1):
            self.images_index = int(((self.cur_ticks - self.start_ticks) / self.duration) * self.num_images)
            self.images_index = max(min(self.images_index, self.num_images - 1), 0)


    def draw_wo(self, screen: pygame.Surface) -> None:
        """
        Draws the Animation to the screen.

        :param screen:
        :return:
        """

        color = Color(self.color[0], self.color[1], self.color[2], self.alpha)
        alpha_surf = pygame.Surface((self.rect.width, self.rect.height), SRCALPHA)

        if self.images is None:
            pygame.draw.rect(alpha_surf, color, (0, 0, self.rect.width, self.rect.height))
            screen.blit(alpha_surf, self.rect)
        else:
            screen.blit(pygame.transform.scale(self.images[self.images_index], (self.rect.width * 1.0, self.rect.height * 1.0)), self.rect)

    def should_remove(self) -> bool:
        """
        Returns True if the Animation should be removed (has exceeded its lifetime).

        :return: bool indicating whether Animation should be removed
        """

        return (self.cur_ticks - self.start_ticks) > self.duration

    def allow_collision(self) -> bool:
        """
        Determines if this object can participate in a collision

        :return:
        """

        return False

    def prime_for_collision(self) -> None:
        """
        Reset the latch to allow for future collisions

        :return:
        """
        self.primed_collision = False
