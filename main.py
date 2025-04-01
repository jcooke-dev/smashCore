import settings
import game_manager
from game_objects import Balls, Bricks, Paddles
import pygame

pygame.init()
active_bricks = []
brick_colors = []
brick_bodies = []

game_screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("SmashCore")
clock = pygame.time.Clock()
game_surface = pygame.draw.rect(game_screen,
                                (0,0,0), (0,0,settings.WIDTH,settings.HEIGHT))

game_manager.generate_bricks(active_bricks, brick_colors, brick_bodies)
game_manager.generate_ball()
game_manager.generate_paddle()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    settings.all_sprites.update()

    for brick in settings.bricks:
        Bricks.convert(brick)

    for ball in settings.balls:
        Balls.convert(ball)

    for paddle in settings.paddles:
        Paddles.convert(paddle)

    if pygame.sprite.collide_rect(ball, paddle):
        diff = (paddle.rect.x + 61) - (ball.rect.x + 12)
        ball.bounce(diff)

    brick_collision_list = pygame.sprite.spritecollide(ball, settings.bricks, True)
    for brick in brick_collision_list:
        ball.bounce(0)
        settings.score += 10

    game_screen.blit(settings.background_img, game_surface)
    settings.all_sprites.draw(game_screen)

    pygame.display.flip()
    clock.tick(settings.fps)

pygame.quit()

#pygame.mixer.music.load('sounds/music.mp3')
#pygame.mixer.music.play()

#pygame.mixer.music.stop()
#pygame.mixer.quit()
#pygame.mixer.init()


