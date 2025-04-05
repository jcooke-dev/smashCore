from gameworld import GameWorld
from src.ball import Ball
from src.paddle import Paddle
from src.brick import Brick


def test_gameworld_init():
    """
    Test the gameworld has a ball, paddle, and at least one brick
    :return:
    """
    gw = GameWorld()
    ball_found = any(isinstance(obj, Ball) for obj in gw.world_objects)
    paddle_found = any(isinstance(obj, Paddle) for obj in gw.world_objects)
    brick_found = any(isinstance(obj, Brick) for obj in gw.world_objects)
    assert ball_found
    assert paddle_found
    assert brick_found
