"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: The Brick type of WorldObject, with customized behavior.
"""

import pygame
from pygame import Vector2

import assets
from animation import Animation
from constants import (BALL_RADIUS, EFFECT_BRICK_PLAIN_DESTROY_DURATION, EFFECT_BRICK_PLAIN_DESTROY_INFLATION,
                       EFFECT_BRICK_PLAIN_DESTROY_FADE, EFFECT_BRICK_IMAGE_DESTROY_DURATION,
                       EFFECT_BRICK_IMAGE_DESTROY_INFLATION, EFFECT_BRICK_IMAGE_DESTROY_FADE,
                       EFFECT_POWER_UP_DURATION, EFFECT_POWER_UP_DROP_ACC_Y, BLACK, WHITE)

from gamesettings import GameSettings
from playerstate import PlayerState
from poweruptype import PowerUpType
from worldobject import WorldObject


class Brick(WorldObject, pygame.sprite.Sprite):
    """
    Brick to be lined up in rows and columns for the board
    They disappear when hit
    They have a size, color, and point value
    """

    def __init__(self, rect: pygame.rect, color: pygame.color, value: int = 1,
                 image: pygame.image = None, strength: int = 1, bonus: int = 0,
                 power_up: PowerUpType = PowerUpType.NO_TYPE) -> None:
        """
        Initializes a Brick object.

        :param rect: The rectangle representing the brick's position and size.
        :param color: The RGB color of the brick.
        :param value: The score value of the brick.
        """
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.rect: pygame.rect = pygame.Rect(rect)
        self.color: pygame.color = color
        self.value: int = value
        self.image: pygame.image = image
        self.strength: int = strength  # Number of hits required to break the brick
        self.strength_initial: int = strength
        self.bonus = bonus
        self.power_up: PowerUpType = power_up

        if bonus > 0:
            self.font_strength = pygame.font.Font(None, self.rect.height - 20)
        else:
            self.font_strength = None

    def _add_strength_indicator(self, screen: pygame.Surface) -> None:
        text_surface = self.font_strength.render(str(self.strength), True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def draw_wo(self, screen: pygame.Surface) -> None:
        """
        Draws the brick to the screen.

        :param screen:
        :return:
        """

        if self.image is None:
            pygame.draw.rect(screen, self.color, self.rect)
            # draw any power-up overlay
            match self.power_up:
                case PowerUpType.EXTRA_LIFE:
                    # draw an outline first
                    pygame.draw.circle(screen, BLACK, self.rect.center, BALL_RADIUS + 1)
                    # then, the fill
                    pygame.draw.circle(screen, WHITE, self.rect.center, BALL_RADIUS)
                case _:
                    pass
        else:
            screen.blit(self.image, self.rect)
            # draw any power-up overlay
            match self.power_up:
                case PowerUpType.EXTRA_LIFE:
                    screen.blit(assets.BALL_IMG.convert_alpha(),
                                (self.rect.centerx - BALL_RADIUS + 2, self.rect.centery - BALL_RADIUS + 2))
                case _:
                    pass

        if self.bonus > 0:
            self._add_strength_indicator(screen)

    def add_collision(self, gset: GameSettings) -> None:
        """
        Reduces the brick's strength when it's hit.

        :return:
        """
        self.strength -= 1
        if self.strength > 0:
            snd: pygame.mixer.Sound = pygame.mixer.Sound(assets.BRICK_BOUNCE_SFX)
            snd.set_volume(gset.sfx_volume)
            pygame.mixer.find_channel(True).play(snd)

    def should_score(self) -> bool:
        return True

    def should_remove(self) -> bool:
        """
        Returns True if the brick should be removed (strength <= 0).

        :return: bool indicating whether Brick should be removed
        """
        return self.strength <= 0

    def trigger_destruction_effect(self, world_objects: list[WorldObject], gset: GameSettings, ps: PlayerState) -> None:
        """
        This is called to create and trigger the animation effect (for Brick destruction, in this case).

        :param gset: GameSettings
        :param world_objects: list of WorldObjects
        :return:
        """

        if self.image is None:
            # if a plain rect Brick, then the animation is a brief minor rect.inflation(), with a fade
            world_objects.append(Animation(EFFECT_BRICK_PLAIN_DESTROY_DURATION,
                                           self.rect.inflate(self.rect.width * EFFECT_BRICK_PLAIN_DESTROY_INFLATION,
                                                             self.rect.height * EFFECT_BRICK_PLAIN_DESTROY_INFLATION),
                                           self.color, is_ball=False, fade=EFFECT_BRICK_PLAIN_DESTROY_FADE))
        else:
            # if an image Brick, the animation is an actual multi-frame image animation
            world_objects.append(Animation(EFFECT_BRICK_IMAGE_DESTROY_DURATION,
                                           self.rect.inflate(
                                               self.rect.width * EFFECT_BRICK_IMAGE_DESTROY_INFLATION,
                                               self.rect.height * EFFECT_BRICK_IMAGE_DESTROY_INFLATION),
                                           self.color, is_ball=False, fade=EFFECT_BRICK_IMAGE_DESTROY_FADE,
                                           images=assets.BRICK_ANIMATION))

        # if power-up, handle properly
        if self.power_up == PowerUpType.EXTRA_LIFE:
            ps.lives += 1

            # trigger an animation
            if self.image is None:
                # if a plain rect Brick, then the animation is a moving plain ball
                world_objects.append(Animation(EFFECT_POWER_UP_DURATION,
                                               self.rect,
                                               self.color, is_ball=True, fade=True,
                                               v_acc=Vector2(0.0, -1.0 * EFFECT_POWER_UP_DROP_ACC_Y)))
            else:
                # if an image Brick, the animation is a moving image ball
                world_objects.append(Animation(EFFECT_POWER_UP_DURATION,
                                               self.rect,
                                               self.color, is_ball=True, fade=True,
                                               v_acc=Vector2(0.0, -1.0 * EFFECT_POWER_UP_DROP_ACC_Y),
                                               images=[assets.BALL_IMG]))
                                               
        snd: pygame.mixer.Sound = pygame.mixer.Sound(assets.BRICK_SFX)
        snd.set_volume(gset.sfx_volume)
        pygame.mixer.find_channel(True).play(snd)
