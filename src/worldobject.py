"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is meant to be a useful parent type class for all objects in the
                        GameWorld, although there isn't much commonality between the types.
"""
import pygame

import gamestate as gs_
import playerstate as ps_
import leaderboard as lb_
import gamesettings as gst_


class WorldObject:
    """ This is a parent class for the specific world objects (Ball, Paddle, Bricks) """

    def __init__(self) -> None:
        self.speed = None
        self.bonus = 0
        self.color: pygame.color = None
        self.value: int = 0
        self.rect: pygame.rect = None
        self.can_react: bool = False  # can this object react to collisions with other objects?
        self.primed_collision: bool = True
        self.strength: int = 1
        self.strength_initial: int = self.strength

    def update_wo(self, gs: gs_.GameState, ps: ps_.PlayerState, lb: lb_.Leaderboard, gset: gst_.GameSettings):
        """
        Update the WorldObject's pos, vel, acc, etc. (and possibly GameState)

        :param gset: GameSettings
        :param lb: Leaderboard
        :param gs: GameState
        :param ps: PlayerState
        :return:
        """

    def draw_wo(self, screen: pygame.Surface) -> None:
        """
        Draw the WorldObject to the screen

        :param screen:
        :return:
        """

    def detect_collision(self, wo: pygame.rect, gs: gs_.GameState, gset: gst_.GameSettings) -> None:
        """
        Function to detect collisions

        :param gset: GameSettings
        :param wo: the other Rect in the collision detection check
        :param gs: GameState
        :return:
        """

    def add_collision(self) -> None:
        """
        Record that something collided with this WorldObject

        :return:
        """

    def should_score(self) -> bool:
        """
        Inform caller that this WorldObject should increase the player's score

        :return:
        """
        return False

    def should_remove(self) -> bool:
        """
        Inform caller that this WorldObject should be removed from the GameWorld

        :return:
        """
        return False

    def allow_collision(self) -> bool:
        """
        Determines if this object can participate in a collision

        :return:
        """
        if self.primed_collision:
            self.primed_collision = False
            return True
        return False

    def prime_for_collision(self) -> None:
        """
        Reset the latch to allow for future collisions

        :return:
        """
        self.primed_collision = True

    def trigger_destruction_effect(self, world_objects, gset: gst_.GameSettings) -> None:
        """
        This is called to create and trigger the animation effect.

        :param gset: GameSettings
        :param world_objects: list of WorldObjects
        :return:
        """
