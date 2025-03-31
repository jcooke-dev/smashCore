import pygame
import asyncio
from random import randrange as rnd

pygame.display.set_caption("Smash Core")
WIDTH, HEIGHT = 1200, 800
frame_rate = 60

# Paddle configuration
paddle_width = 200
paddle_height = 20
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - paddle_height - 10
paddle = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)

# Ball configuration
ball_rad = 11
ball_speed = 6
ball_box = int(ball_rad * 2 ** 0.5)
ball_x = rnd(ball_box, WIDTH - ball_box)
ball_y = HEIGHT // 2
ball = pygame.Rect(ball_x, ball_y, ball_box, ball_box)
x_axis, y_axis = 1, -1

# Brick configuration with gap
block_rows = 5
block_cols = 10
block_margin = 5
block_width = (WIDTH - (block_cols - 1) * block_margin) / block_cols
block_height = 50
block_gap = 40

# Generate brick layout and colors.
block_layout = [pygame.Rect(i * (block_width + block_margin), block_gap + block_margin + (block_height + block_margin) * j, block_width, block_height) for i in range(block_cols) for j in range(block_rows)]
block_colors = [(255, 0, 0), (255, 165, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255)] * block_cols
block_colors = [block_colors[j] for j in range(block_rows)] * block_cols
block_colors = [block_colors[j] for j in range(len(block_layout))]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

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
    global ball_x, ball_y, block_layout, block_colors, x_axis, y_axis, frame_rate, game_over, ball, lives, score, level, game_started
    ball_x = rnd(ball_box, WIDTH - ball_box)
    ball_y = HEIGHT // 2
    ball.x, ball.y = ball_x, ball_y
    block_layout = [pygame.Rect(i * (block_width + block_margin), block_gap + block_margin + (block_height + block_margin) * j, block_width, block_height) for i in range(block_cols) for j in range(block_rows)]
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
    global level, block_layout, block_colors, game_started, ball_x, ball_y, ball, block_rows, block_cols, block_width, block_height

    level += 1

    initial_rows = 5
    initial_cols = 10
    initial_width = block_width
    initial_height = block_height

    initial_block_area = initial_rows * initial_cols * initial_width * initial_height

    block_rows += 1
    block_cols += 1

    block_width = (WIDTH - (block_cols - 1) * block_margin) / block_cols
    block_height = initial_block_area / (block_cols * block_rows * block_width)

    block_layout = [
        pygame.Rect(
            i * (block_width + block_margin),
            block_gap + block_margin + (block_height + block_margin) * j,
            block_width,
            block_height
        )
        for i in range(block_cols)
        for j in range(block_rows)
    ]

    block_colors = [(255, 0, 0), (255, 165, 0), (0, 255, 0), (255, 255, 0), (0, 255, 255)] * block_cols
    block_colors = [block_colors[j] for j in range(block_rows)] * block_cols
    block_colors = [block_colors[j] for j in range(len(block_layout))]

    game_started = False
    ball_x = rnd(ball_box, WIDTH - ball_box)
    ball_y = HEIGHT // 2
    ball.x, ball.y = ball_x, ball_y

def logo(screen, x, y):

    logo_color = (255, 165, 0)
    text_color = (255, 255, 255)
    shadow_color = (100, 100, 100)

    font_smash = pygame.font.Font(None, 60)
    text_smash = font_smash.render("Smash", True, text_color)
    text_smash_shadow = font_smash.render("Smash", True, shadow_color)

    text_smash_rect = text_smash.get_rect(center=(x + 100, y + 40))
    text_smash_shadow_rect = text_smash_rect.copy()
    text_smash_shadow_rect.move_ip(3, 3)

    screen.blit(text_smash_shadow, text_smash_shadow_rect)
    screen.blit(text_smash, text_smash_rect)

    font_core = pygame.font.Font(None, 60)
    text_core = font_core.render("Core", True, text_color)
    text_core_shadow = font_core.render("Core", True, shadow_color)

    text_core_rect = text_core.get_rect(center=(x + 230, y + 80))
    text_core_shadow_rect = text_core_rect.copy()
    text_core_shadow_rect.move_ip(3, 3)

    screen.blit(text_core_shadow, text_core_shadow_rect)
    screen.blit(text_core, text_core_rect)

    pygame.draw.line(screen, logo_color, (x, y + 120), (x + 300, y + 120), 3)

    font_arcade = pygame.font.Font(None, 24)
    text_arcade = font_arcade.render("The Retro Arcade Experience", True, (200, 200, 200))
    text_arcade_rect = text_arcade.get_rect(center=(x + 150, y + 150))
    screen.blit(text_arcade, text_arcade_rect)

async def main():
    global game_over, game_started, frame_rate, x_axis, y_axis, score, lives, level

    show_logo_delay = 5.0
    logo_timer = 0.0

    while True:
        sc.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and not game_started:
                if logo_timer >= show_logo_delay:
                    game_started = True

        if not game_started:
            if logo_timer < show_logo_delay:
                logo(sc, WIDTH // 2 - 150, HEIGHT // 3)
                logo_timer += clock.get_time() / 1000.0
            else:
                level_text = font_level.render(f"Level {level}", True, (255, 255, 255))
                level_rect = level_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                sc.blit(level_text, level_rect)
                instruction_text = font_buttons.render("Click to Start", True, (200, 200, 200))
                instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
                sc.blit(instruction_text, instruction_rect)

        elif game_over:
            pygame.mouse.set_visible(True)
            text_game_over = font_game_over.render("You got smashed!", True, pygame.Color('red'))
            text_rect = text_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            sc.blit(text_game_over, text_rect)

            button_width = 200
            button_height = 75
            button_x = WIDTH // 2 - button_width // 2
            button_y_start = HEIGHT // 2 + 50

            draw_button(sc, "Try Again", button_x, button_y_start, button_width, button_height, (0, 255, 0), (0, 200, 0),
                        reset_game)
            draw_button(sc, "Quit", button_x, button_y_start + button_height + 10, button_width, button_height, (255, 0, 0),
                        (200, 0, 0), pygame.quit)
        else:
            [pygame.draw.rect(sc, block_colors[color], block) for color, block in enumerate(block_layout)]
            pygame.draw.rect(sc, pygame.Color('red'), paddle)
            pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_rad)

            ball.x += ball_speed * x_axis
            ball.y += ball_speed * y_axis

            if ball.centerx < ball_rad or ball.centerx > WIDTH - ball_rad:
                x_axis = -x_axis
            if ball.centery < ball_rad:
                y_axis = -y_axis
            if ball.colliderect(paddle) and y_axis > 0:
                x_axis, y_axis = detect_collision(x_axis, y_axis, ball, paddle)

            block_collision = ball.collidelist(block_layout)
            if block_collision != -1:
                hitbox = block_layout.pop(block_collision)
                hit_color = block_colors.pop(block_collision)
                x_axis, y_axis = detect_collision(x_axis, y_axis, ball, hitbox)
                hitbox.inflate_ip(ball.width * 3, ball.height * 3)
                pygame.draw.rect(sc, hit_color, hitbox)
                frame_rate += 2

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

            if ball.top > HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True

            if game_over:
                continue

            if ball.top > HEIGHT:
                ball_x = rnd(ball_box, WIDTH - ball_box)
                ball_y = HEIGHT // 2
                ball.x, ball.y = ball_x, ball_y
                x_axis, y_axis = 1, -1

            mouse_pos = pygame.mouse.get_pos()
            paddle.centerx = mouse_pos[0]
            if paddle.left < 0:
                paddle.left = 0
            if paddle.right > WIDTH:
                paddle.right = WIDTH

            if not block_layout:
                next_level()
                x_axis, y_axis = 1, -1

            score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
            sc.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

        # Render lives text outside the else block, only when game started.
        if game_started and not game_over:
            lives_text = font_score.render(f"Lives: {lives}", True, (255, 255, 255))
            sc.blit(lives_text, (10, HEIGHT - lives_text.get_height() - 30))

        pygame.display.flip()
        clock.tick(frame_rate)
        await asyncio.sleep(0)

asyncio.run(main())
