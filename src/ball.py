import pygame
from settings import BALL_RADIUS, BALL_SPEED, WHITE, WIDTH, HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.radius = BALL_RADIUS
        self.speed = BALL_SPEED
        self.x = x - self.radius
        self.y = y
        self.ball_rect = int(self.radius * 2 ** 0.5)
        self.dx, self.dy = 1, -1
        
        self.rect = pygame.Rect(self.x, self.y, self.ball_rect, self.ball_rect)
    
    # moves and updates the ball position    
    def move_ball(self):
        self.x += self.speed * self.dx
        self.y += self.speed * self.dy
        
        self.rect.x = self.x
        self.rect.y = self.y
    
    # draws the ball on the screen
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.rect.center, self.radius)
    
    #defines collision behavior with the edges of the screen
    def wall_collisions(self):
         # ball collision wall left/right
        if self.rect.centerx < self.radius or self.rect.centerx > WIDTH - self.radius:
            self.dx = -self.dx
        # ball collision wall top
        if self.rect.centery < self.radius:
            self.dy = -self.dy