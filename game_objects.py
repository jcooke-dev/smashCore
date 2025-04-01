import pygame
from pygame import Vector2
import settings

class Bricks(pygame.sprite.Sprite):
    def __init__(self, brick_color, brick_body):
        pygame.sprite.Sprite.__init__(self)
        self.image = brick_color
        self.rect = brick_body
        self.x = brick_body.x
        self.y = brick_body.y
        self.center = brick_body.center
        self.centerx = brick_body.centerx
        self.centery = brick_body.centery
        self.rect.x = self.x
        self.rect.y = self.y
        self.left = brick_body.left
        self.right = brick_body.right
        self.top = brick_body.top
        self.bottom = brick_body.bottom
        self.width = brick_body.width
        self.height = brick_body.height
        self.rect.width = self.width
        self.rect.height = self.height
        self.mask = pygame.mask.from_surface(self.image)

    def convert(self):
        return self.image.convert_alpha()

class Balls(pygame.sprite.Sprite):
    def __init__(self, ball_face, ball_body):
        pygame.sprite.Sprite.__init__(self)
        self.image = ball_face
        self.rect = ball_body
        self.x = ball_body.x
        self.y = ball_body.y
        self.center = ball_body.center
        self.centerx = ball_body.centerx
        self.centery = ball_body.centery
        self.rect.x = self.x
        self.rect.y = self.y
        self.left = ball_body.left
        self.right = ball_body.right
        self.top = ball_body.top
        self.bottom = ball_body.bottom
        self.width = ball_body.width
        self.height = ball_body.height
        self.rect.width = self.width
        self.rect.height = self.height
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = Vector2(6, -6)

    def convert(self):
        return self.image.convert_alpha()

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.rect.left <= 0 or self.rect.right >= settings.WIDTH:
            self.velocity.x *= -1

        if self.rect.top <= 10:
            self.velocity.y *= -1

        if self.rect.bottom >= settings.HEIGHT:
            self.velocity.y *= -1

    def bounce(self, diff):
        # Calculate the angle of reflection based on where the ball hits the paddle
        angle = diff * -90 / 12
        self.velocity.y *= -1
        self.velocity.rotate_ip(angle)

class Paddles(pygame.sprite.Sprite):
    def __init__(self, paddle_face, paddle_body):
        pygame.sprite.Sprite.__init__(self)
        self.image = paddle_face
        self.rect = paddle_body
        self.x = paddle_body.x
        self.y = paddle_body.y
        self.center = paddle_body.center
        self.centerx = paddle_body.centerx
        self.centery = paddle_body.centery
        self.rect.x = self.x
        self.rect.y = self.y
        self.left = paddle_body.left
        self.right = paddle_body.right
        self.top = paddle_body.top
        self.bottom = paddle_body.bottom
        self.width = paddle_body.width
        self.height = paddle_body.height
        self.rect.width = self.width
        self.rect.height = self.height
        self.mask = pygame.mask.from_surface(self.image)

    def convert(self):
        return self.image.convert_alpha()

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] - self.width // 2


