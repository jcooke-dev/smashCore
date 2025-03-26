import pygame
from random import randrange as rnd

pygame.display.set_caption("Smash Core")
WIDTH, HEIGHT = 1200, 800
frame_rate = 60

# paddle configuration
paddle_width = 200
paddle_height = 20

paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - paddle_height - 10
paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)  # Draw Paddle

# ball configuration
ball_rad = 15
ball_speed = 6

ball_box = int(ball_rad * 2 ** 0.5)  # Ball box size

ball_x = rnd(ball_box, WIDTH - ball_box)
ball_y = HEIGHT // 2
ball = pygame.Rect(ball_x, ball_y, ball_box, ball_box)  # Draw ball
x_axis, y_axis = 1, -1  # Ball movement

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
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Hide the mouse cursor initially
pygame.mouse.set_visible(False)

# Font setup
font_game_over = pygame.font.Font(None, 100)
font_buttons = pygame.font.Font(None, 50)

# Game state
game_over = False

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
    global ball_x, ball_y, block_layout, block_colors, x_axis, y_axis, frame_rate, game_over, ball
    ball_x = rnd(ball_box, WIDTH - ball_box)
    ball_y = HEIGHT // 2
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
    x_axis, y_axis = 1, -1
    frame_rate = 60
    game_over = False
    pygame.mouse.set_visible(False)  # Hide the cursor when game restarts

while True:
    # fill the screen with black.
    sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    if game_over:
        pygame.mouse.set_visible(True)  # Show the cursor in game over screen
        # Game over screen
        text_game_over = font_game_over.render("YOU GOT SMASHED!", True, pygame.Color('red'))
        text_rect = text_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        sc.blit(text_game_over, text_rect)

        # Draw buttons
        draw_button(sc, "Play Again", WIDTH // 4, HEIGHT // 2, 200, 75, (0, 255, 0), (0, 200, 0), reset_game)
        draw_button(sc, "Quit", WIDTH * 3 // 4 - 100, HEIGHT // 2, 200, 75, (255, 0, 0), (200, 0, 0), exit)
    else:
        # draws game objects
        [pygame.draw.rect(sc, block_colors[color], block) for color, block in enumerate(block_layout)]
        pygame.draw.rect(sc, pygame.Color('red'), paddle)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_rad)

        # Move the ball
        ball.x += ball_speed * x_axis
        ball.y += ball_speed * y_axis

        # ball collision wall left/right
        if ball.centerx < ball_rad or ball.centerx > WIDTH - ball_rad:
            x_axis = -x_axis
        # ball collision wall top
        if ball.centery < ball_rad:
            y_axis = -y_axis
        # ball collision paddle
        if ball.colliderect(paddle) and y_axis > 0:
            x_axis, y_axis = detect_collision(x_axis, y_axis, ball, paddle)

        # collision blocks
        block_collision = ball.collidelist(block_layout)
        if block_collision != -1:
            hitbox = block_layout.pop(block_collision)
            hit_color = block_colors.pop(block_collision)
            x_axis, y_axis = detect_collision(x_axis, y_axis, ball, hitbox)
            # special effect
            hitbox.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(sc, hit_color, hitbox)
            frame_rate += 2

        # win, game over
        if ball.top > HEIGHT:
            game_over = True

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
    clock.tick(frame_rate)
