import random
import settings
from game_objects import Bricks, Balls, Paddles

def generate_bricks(active_bricks, brick_colors, brick_bodies):

    for i in range(0, 1200, 120):
        for j in range(400, 220, -20):
            brick_choice = (random.choice([settings.yellow, settings.green, settings.blue,
                                        settings.red, settings.pink, settings.orange,
                                        settings.lt_blue, settings.purple, settings.teal,
                                        settings.lavender]))
            brick_face = brick_choice
            brick_body = brick_face.get_rect()
            brick_body.x = i
            brick_body.y = j
            brick_body.center = (brick_body.centerx, brick_body.centery)
            brick_obj = Bricks(brick_face, brick_body)
            brick = brick_obj
            brick_colors.append(brick_face)
            brick_bodies.append(brick_body)
            active_bricks.append(brick)
            settings.bricks.add(brick)
            settings.all_sprites.add(brick)

    return active_bricks, brick_colors, brick_bodies

def generate_paddle():

    paddle_face = settings.paddle
    paddle_body = paddle_face.get_rect()
    paddle_body.x = settings.WIDTH // 2 - paddle_body.width // 2
    paddle_body.y = settings.HEIGHT - 150
    paddle_obj = Paddles(paddle_face, paddle_body)
    paddle = paddle_obj
    settings.paddles.add(paddle)
    settings.all_sprites.add(paddle)

    return paddle_face, paddle_body, paddle

def generate_ball():

    ball_face = settings.ball
    ball_body = ball_face.get_rect()
    ball_body.x = settings.WIDTH // 2 - ball_body.width // 2
    ball_body.y = settings.HEIGHT - 180
    ball_body.center = (ball_body.centerx, ball_body.centery)
    ball_obj = Balls(ball_face, ball_body)
    ball = ball_obj
    settings.balls.add(ball)
    settings.all_sprites.add(ball)

    return ball_face, ball_body, ball










