"""
    SmashCore is a breakout style game
"""
import pygame
import settings
from paddle import Paddle
from random import randrange as rnd


pygame.display.set_caption(settings.GAME_NAME)
fps = settings.INITIAL_FPS

# # List of all the sprites used
# all_sprites_list = pygame.sprite.Group()

# Create the Paddle and start location
paddle = Paddle(pygame.Color('red'), settings.PAD_WIDTH, settings.PAD_HEIGHT)

# # Add the paddle to the list of sprites
# all_sprites_list.add(paddle)

# ball settings
ball_radius = 15
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball_x = rnd(ball_rect, settings.WIDTH - ball_rect)
ball_y = settings.HEIGHT // 2
ball = pygame.Rect(ball_x, ball_y, ball_rect, ball_rect)
dx, dy = 1, -1

# Block configuration
block_layout = [
    pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50)
    for i in range(10)
    for j in range(4)
]

block_colors = [
    (rnd(30, 256), rnd(30, 256), rnd(30, 256))
    for i in range(10)
    for j in range(4)
]


pygame.init()
sc = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
surface = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(False)


# Font setup
font_game_over = pygame.font.Font(None, 100)
font_buttons = pygame.font.Font(None, 50)

# Game state
running = True
game_over = False
pause = False

# Displays the pause menu where user can continue, restart, or quit the game
def draw_pause_menu():
    pygame.draw.rect(surface, (0, 0, 0, 100), [0, 0, settings.WIDTH, settings.HEIGHT])
    #pygame.draw.rect(surface, settings.DARKBLUE, [(settings.WIDTH // 2) - 300, 250, 600, 75])
    reset = pygame.draw.rect(surface, (0, 255, 0), [(settings.WIDTH // 2) - 200, 350, 400, 75])
    quit = pygame.draw.rect(surface, (0, 255, 0), [(settings.WIDTH // 2) - 200, 450, 400, 75])
    surface.blit(font_game_over.render('Game Paused: ESC to Resume', True, settings.DARKBLUE), (90, 270))
    surface.blit(font_buttons.render('Restart Game', True, settings.BLACK), ((settings.WIDTH // 2) - 190, 370))
    surface.blit(font_buttons.render('Quit Game', True, settings.BLACK), ((settings.WIDTH // 2) - 190, 470))
    sc.blit(surface, (0, 0))
    return reset, quit

# Function to detect collisions
def detect_collision(horizontal, vertical, ball, hitbox):
    if horizontal > 0:  # checks for horizontal ball collision
        x_delta = ball.right - hitbox.left
    else:
        x_delta = hitbox.right - ball.left

    if vertical > 0:  # checks for vertical ball collision
        y_delta = ball.bottom - hitbox.top
    else:
        y_delta = hitbox.bottom - ball.top

    # Collision type
    if abs(x_delta - y_delta) < 10:
        horizontal, vertical = -horizontal, -vertical
    elif x_delta > y_delta:  # vertical collision
        vertical = -vertical
    elif y_delta > x_delta:  # horizontal collision
        horizontal = -horizontal

    return horizontal, vertical


# Button function
def draw_button(screen, text, x, y, width, height, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, width, height)

    if rect.collidepoint(mouse):
        pygame.draw.rect(screen, hover_color, rect)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, rect)

    text_surface = font_buttons.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def reset_game():
    global ball_x, ball_y, block_layout, block_colors, dx, dy, fps, game_over, ball
    ball_x = rnd(ball_rect, settings.WIDTH - ball_rect)
    ball_y = settings.HEIGHT // 2
    ball.x, ball.y = ball_x, ball_y
    block_layout = [
        pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50)
        for i in range(10)
        for j in range(4)
    ]
    block_colors = [
        (rnd(30, 256), rnd(30, 256), rnd(30, 256))
        for i in range(10)
        for j in range(4)
    ]
    dx, dy = 1, -1
    fps = settings.INITIAL_FPS
    game_over = False
    pygame.mouse.set_visible(False)  # Hide the cursor when game restarts

#draws the game over screen on a surface and displays it if game is lost    
def draw_game_over_menu():
    pygame.mouse.set_visible(True)  # Show the cursor in game over screen
    pygame.draw.rect(surface, (0, 0, 0, 160), [0, 0, settings.WIDTH, settings.HEIGHT])
    # Game over screen
    text_game_over = font_game_over.render("YOU GOT SMASHED!", True, pygame.Color('red'))
    text_rect = text_game_over.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 3))
    surface.blit(text_game_over, text_rect)

    # Draw buttons
    draw_button(surface, "Play Again", settings.WIDTH // 4, settings.HEIGHT // 2, 200, 75, (0, 255, 0), (0, 200, 0), reset_game)
    draw_button(surface, "Quit", settings.WIDTH * 3 // 4 - 100, settings.HEIGHT // 2, 200, 75, (255, 0, 0), (200, 0, 0), exit)
    sc.blit(surface, (0, 0))

while running:

    # fill the screen with black.
    sc.fill(settings.BLACK)

    # draws game objects
    [pygame.draw.rect(sc, block_colors[color], block) for color, block in enumerate(block_layout)]
    pygame.draw.rect(sc, pygame.Color('red'), paddle.rect, 0, 7)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    if game_over:
        draw_game_over_menu()

    if pause:
        restart_game, quit_game = draw_pause_menu()

    if not pause and not game_over: 
        # Move the ball
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy

        # paddle control (mouse)
        mouse_pos = pygame.mouse.get_pos()
        paddle.move_by_mouse(mouse_pos[0])

    # ball collision wall left/right
    if ball.centerx < ball_radius or ball.centerx > settings.WIDTH - ball_radius:
        dx = -dx
    # ball collision wall top
    if ball.centery < ball_radius:
        dy = -dy
    # ball collision paddle
    if ball.colliderect(paddle.rect) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle.rect)

    # collision blocks
    block_collision = ball.collidelist(block_layout)
    if block_collision != -1:

        hitbox = block_layout.pop(block_collision)
        hit_color = block_colors.pop(block_collision)
        dx, dy = detect_collision(dx, dy, ball, hitbox)

        # special effect
        hitbox.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(sc, hit_color, hitbox)
        fps += 2

    # win, game over
    if ball.top > settings.HEIGHT:
        game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                    pygame.mouse.set_pos(mouse_pos)
                    pygame.mouse.set_visible(False)
                else:
                    pause = True
                    pygame.mouse.set_visible(True)
        if event.type == pygame.MOUSEBUTTONDOWN and pause:
            if restart_game.collidepoint(event.pos):
                reset_game()
                pause = False
            if quit_game.collidepoint(event.pos):
                exit()

    # all_sprites_list.update()

    # update screen
    pygame.display.flip()
    clock.tick(fps)
