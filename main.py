import pygame
from random import randrange as rnd

pygame.display.set_caption("Smash Core")
WIDTH, HEIGHT = 1200, 800
fps = 60

# paddle settings
paddle_w = 330
paddle_h = 35
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# ball settings
ball_radius = 15
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

while True:
    # fill the screen with black.
    sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # drawing
    pygame.draw.rect(sc, pygame.Color('dark-blue'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    # ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # ball collision left/right
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    # ball collision top
    if ball.centery < ball_radius:
        dy = -dy
    # ball collision paddle
    if ball.colliderect(paddle) and dy > 0:
        dy = -dy

    # paddle control (mouse)
    mouse_pos = pygame.mouse.get_pos()
    paddle.centerx = mouse_pos[0]
    # Keep paddle within screen bounds
    if paddle.left < 0:
        paddle.left = 0
    if paddle.right > WIDTH:
        paddle.right = WIDTH

    # update screen
    pygame.display.flip()
    clock.tick(fps)
