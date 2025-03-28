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
		
	def move_ball(self):
		self.x += self.speed * self.dx
		self.y += self.speed * self.dy
		self.rect.x = self.x
		self.rect.y = self.y
	 
	def draw(self, screen):
	 	pygame.draw.circle(screen, WHITE, self.rect.center, self.radius)