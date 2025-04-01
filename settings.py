import pygame
import os

bricks = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
paddles = pygame.sprite.Group()
score = 0

art_dir = 'assets/art/'
sound_dir = 'assets/sound/'
background_img_path = 'background.png'
yellow_img_path = 'yellow_brick.png'
blue_img_path = 'blue_brick.png'
green_img_path = 'green_brick.png'
red_img_path = 'red_brick.png'
pink_img_path = 'pink_brick.png'
orange_img_path = 'orange_brick.png'
lt_blue_img_path = 'lt_blue_brick.png'
purple_img_path = 'purple_brick.png'
teal_img_path = 'teal_brick.png'
lavender_img_path = 'lavender_brick.png'
ball_img_path = 'ball.png'
paddle_img_path = 'paddle.png'

background_img = pygame.image.load(os.path.join(art_dir, background_img_path))
yellow = pygame.image.load(os.path.join(art_dir, yellow_img_path))
blue = pygame.image.load(os.path.join(art_dir, blue_img_path))
green = pygame.image.load(os.path.join(art_dir, green_img_path))
red = pygame.image.load(os.path.join(art_dir, red_img_path))
pink = pygame.image.load(os.path.join(art_dir, pink_img_path))
orange = pygame.image.load(os.path.join(art_dir, orange_img_path))
lt_blue = pygame.image.load(os.path.join(art_dir, lt_blue_img_path))
purple = pygame.image.load(os.path.join(art_dir, purple_img_path))
teal = pygame.image.load(os.path.join(art_dir, teal_img_path))
lavender = pygame.image.load(os.path.join(art_dir, lavender_img_path))
ball = pygame.image.load(os.path.join(art_dir, ball_img_path))
paddle = pygame.image.load(os.path.join(art_dir, paddle_img_path))

WIDTH = 1200
HEIGHT = 900
fps = 60