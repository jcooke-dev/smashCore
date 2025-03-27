import pygame
from random import randrange as rnd

pygame.display.set_caption("Smash Core")  # Set window title.
WIDTH, HEIGHT = 1200, 800  # Define screen dimensions.
frame_rate = 60  # Set frame rate.

# Paddle configuration
paddle_width = 200
paddle_height = 20
paddle_x = (WIDTH - paddle_width) // 2  # Center horizontally.
paddle_y = HEIGHT - paddle_height - 10  # Position near bottom.
paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)  # Create paddle rectangle.

# Ball configuration
ball_rad = 15
ball_speed = 6
ball_box = int(ball_rad * 2 ** 0.5)  # Calculate bounding box.
ball_x = rnd(ball_box, WIDTH - ball_box)  # Random initial x position.
ball_y = HEIGHT // 2  # Initial y position at screen center.
ball = pygame.Rect(ball_x, ball_y, ball_box, ball_box)  # Create ball rectangle.
x_axis, y_axis = 1, -1  # Initial ball direction.

# Brick configuration
block_rows = 5
block_cols = 10
block_margin = 5
block_width = (WIDTH - (block_cols - 1) * block_margin) / block_cols  # Calculate brick width.
block_height = 50

# Generate brick layout and colors.
block_layout = [pygame.Rect(i * (block_width + block_margin), block_margin + (block_height + block_margin) * j, block_width, block_height) for i in range(block_cols) for j in range(block_rows)]
block_colors = [(255, 0, 0), (255, 165, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255)] * block_cols  # Define brick colors.
block_colors = [block_colors[j] for j in range(block_rows)] * block_cols  # Adjust colors for rows.
block_colors = [block_colors[j] for j in range(len(block_layout))]  # Adjust colors for layout length.

pygame.init()  # Initialize pygame.
sc = pygame.display.set_mode((WIDTH, HEIGHT))  # Create game screen.
clock = pygame.time.Clock()  # Initialize game clock.

pygame.mouse.set_visible(False)  # Hide mouse cursor.

# Font definitions
font_game_over = pygame.font.Font(None, 100)
font_buttons = pygame.font.Font(None, 50)
font_score = pygame.font.Font(None, 36)
font_level = pygame.font.Font(None, 60)

# Game state variables
game_over = False
lives = 3
score = 0
level = 1
game_started = False

def detect_collision(horizontal, vertical, ball, hitbox):
    # Collision detection logic.
    if horizontal > 0:
        x_delta = ball.right - hitbox.left
    else:
        x_delta = hitbox.right - ball.left
    if vertical > 0:
        y_delta = ball.bottom - hitbox.top
    else:
        y_delta = hitbox.bottom - ball.top

    if abs(x_delta - y_delta) < 10:
        horizontal, vertical = -horizontal, -vertical
    elif x_delta > y_delta:
        vertical = -vertical
    elif y_delta > x_delta:
        horizontal = -horizontal
    return horizontal, vertical

def draw_button(screen, text, x, y, width, height, color, hover_color, action=None):
    # Draw button on screen.
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
    # Reset game state.
    global ball_x, ball_y, block_layout, block_colors, x_axis, y_axis, frame_rate, game_over, ball, lives, score, level, game_started
    ball_x = rnd(ball_box, WIDTH - ball_box)
    ball_y = HEIGHT // 2
    ball.x, ball.y = ball_x, ball_y
    block_layout = [pygame.Rect(i * (block_width + block_margin), block_margin + (block_height + block_margin) * j, block_width, block_height) for i in range(block_cols) for j in range(block_rows)]
    block_colors = [(255, 0, 0), (255, 165, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255)] * block_cols
    block_colors = [block_colors[j] for j in range(block_rows)] * block_cols
    block_colors = [block_colors[j] for j in range(len(block_layout))]
    x_axis, y_axis = 1, -1
    frame_rate = 60
    game_over = False
    lives = 3
    score = 0
    level = 1
    game_started = False
    pygame.mouse.set_visible(False)

def next_level():
    # Advance to next level.
    global level, block_layout, block_colors, game_started, ball_x, ball_y, ball
    level += 1
    block_layout = [pygame.Rect(i * (block_width + block_margin), block_margin + (block_height + block_margin) * j, block_width, block_height) for i in range(block_cols) for j in range(block_rows)]
    block_colors = [(255, 0, 0), (255, 165, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255)] * block_cols
    block_colors = [block_colors[j] for j in range(block_rows)] * block_cols
    block_colors = [block_colors[j] for j in range(len(block_layout))]
    game_started = False
    ball_x = rnd(ball_box, WIDTH - ball_box)
    ball_y = HEIGHT // 2
    ball.x, ball.y = ball_x, ball_y

while True:
    sc.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            game_started = True

    if not game_started:
        # Display level and start instructions.
        level_text = font_level.render(f"Level {level}", True, (255, 255, 255))
        level_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        sc.blit(level_text, level_rect)
        instruction_text = font_buttons.render("Click to Start", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
        sc.blit(instruction_text, instruction_rect)

    elif game_over:
        # Game over screen.
        pygame.mouse.set_visible(True)
        text_game_over = font_game_over.render("You got smashed!", True, pygame.Color('red'))
        text_rect = text_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        sc.blit(text_game_over, text_rect)

        button_width = 200
        button_height = 75
        button_x = WIDTH // 2 - button_width // 2
        button_y_start = HEIGHT // 2 + 50

        draw_button(sc, "Try Again", button_x, button_y_start, button_width, button_height, (0, 255, 0), (0, 200, 0), reset_game)
        draw_button(sc, "Quit", button_x, button_y_start + button_height + 10, button_width, button_height, (255, 0, 0), (200, 0, 0), exit)
    else:
        # Game loop execution.
        [pygame.draw.rect(sc, block_colors[color], block) for color, block in enumerate(block_layout)]
        pygame.draw.rect(sc, pygame.Color('red'), paddle)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_rad)

        ball.x += ball_speed * x_axis
        ball.y += ball_speed * y_axis

        # Ball boundary collision.
        if ball.centerx < ball_rad or ball.centerx > WIDTH - ball_rad:
            x_axis = -x_axis
        if ball.centery < ball_rad:
            y_axis = -y_axis

        # Ball paddle collision.
        if ball.colliderect(paddle) and y_axis > 0:
            x_axis, y_axis = detect_collision(x_axis, y_axis, ball, paddle)

        # Ball brick collision.
        block_collision = ball.collidelist(block_layout)
        if block_collision != -1:
            hitbox = block_layout.pop(block_collision)
            hit_color = block_colors.pop(block_collision)
            x_axis, y_axis = detect_collision(x_axis, y_axis, ball, hitbox)
            hitbox.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(sc, hit_color, hitbox)
            frame_rate += 2  # Increase frame rate on brick hit.

            # Score logic based on brick color.
            if hit_color == (0, 255, 255):
                score += 1
            elif hit_color == (255, 255, 0):
                score += 3
            elif hit_color == (0, 255, 0):
                score += 5
            elif hit_color == (255, 165, 0):
                score += 7
            elif hit_color == (255, 0, 0):
                score += 10

        # Ball bottom boundary collision/life loss.
        if ball.top > HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True #set game over to true here.

        if game_over: #check if game over here and go to game over screen.
            continue #skip the rest of the game loop.

        if ball.top > HEIGHT: #rest of the life lost code.
            ball_x = rnd(ball_box, WIDTH - ball_box)
            ball_y = HEIGHT // 2
            ball.x, ball.y = ball_x, ball_y
            x_axis, y_axis = 1, -1

        # Paddle movement.
        mouse_pos = pygame.mouse.get_pos()
        paddle.centerx = mouse_pos[0]
        if paddle.left < 0:
            paddle.left = 0
        if paddle.right > WIDTH:
            paddle.right = WIDTH

        # Level completion check.
        if not block_layout:
            next_level()
            x_axis, y_axis = 1, -1  # Reset ball direction.

        # Score display.
        score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
        sc.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

        # Lives display.
        lives_text = font_score.render(f"Lives: {lives}", True, (255, 255, 255))
        sc.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 30))

    pygame.display.flip()
    clock.tick(frame_rate)
