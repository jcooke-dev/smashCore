"""
    SmashCore is a breakout style game
"""
import pygame
import settings
from paddle import Paddle
from random import randrange as rnd

pygame.display.set_caption(settings.GAME_NAME)
fps = 60

# List of all the sprites used
all_sprites_list = pygame.sprite.Group()

# Create the Paddle
paddle_speed = 15
paddle = Paddle(settings.LIGHTBLUE, settings.PAD_WIDTH, settings.PAD_HEIGHT)
paddle.rect.x = settings.PAD_LOC_X
paddle.rect.y = settings.PAD_LOC_Y

# Add the paddle to the list of sprites
all_sprites_list.add(paddle)

# ball settings
ball_radius = 15
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, settings.WIDTH - ball_rect), settings.HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

pygame.init()
sc = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(False)

while True:
    # fill the screen with black.
    sc.fill(settings.BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # drawing
    pygame.draw.rect(sc, pygame.Color('blue'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    # ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # ball collision left/right
    if ball.centerx < ball_radius or ball.centerx > settings.WIDTH - ball_radius:
        dx = -dx
    # ball collision top
    if ball.centery < ball_radius:
        dy = -dy
    # ball collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dy = -dy

    # Paddle Control
    """
    # Move the paddle when the player uses the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move_left(settings.PAD_MOVE_LEFT)
    if keys[pygame.K_RIGHT]:
        paddle.move_right(settings.PAD_MOVE_RIGHT)
    """
    # Move paddle using mouse
    paddle.move_by_mouse(pygame.mouse.get_pos()[0])

    all_sprites_list.update()

    # update screen
    pygame.display.flip()
    clock.tick(fps)
