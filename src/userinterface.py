"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: UserInterface contains the various UI element drawing functions.
"""
from collections.abc import Callable
import random
import pygame
import constants
from gamestate import GameState
from src import assets


class UserInterface:
    """ This provides a number of different UI element drawing functions """

    def __init__(self) -> None:
        # Font setup
        self.font_game_over = pygame.font.Font(None, 100)
        self.font_buttons = pygame.font.Font(None, 50)
        # not certain this will reliably get a font (especially on diff OSes), but it's supposed to
        # fallback to a default pygame font
        self.font_fixed_small: pygame.font = pygame.font.SysFont("Courier", 16, True)
        self.surface: pygame.surface = None
        self.screen: pygame.surface = None
        self.background_balls = []
        self.background_bricks = []
        self.initialize_background_elements()

    def draw_button(self, text: str, x: int, y: int, width: int, height: int, color: pygame.color,
                    hover_color: pygame.color, action: Callable = None) -> None:
        """
        Draw a button

        :param text: button text
        :param x: Rect x
        :param y: Rect y
        :param width: Rect width
        :param height: Rect height
        :param color: button color
        :param hover_color: button hover color
        :param action:
        :return:
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, width, height)

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.surface, hover_color, rect)
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.surface, color, rect)

        text_surface = self.font_buttons.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.surface.blit(text_surface, text_rect)

    def draw_pause_menu(self) -> tuple[pygame.Rect, pygame.Rect]:
        """
        Displays the pause menu where user can continue, restart, or quit the game

        :return:
        """
        pygame.draw.rect(self.surface, (0, 0, 0, 100), [0, 0, constants.WIDTH, constants.HEIGHT])
        reset = pygame.draw.rect(self.surface, (0, 255, 0), [(constants.WIDTH // 2) - 200, 350, 400, 75])
        quit = pygame.draw.rect(self.surface, (0, 255, 0), [(constants.WIDTH // 2) - 200, 450, 400, 75])
        self.surface.blit(self.font_game_over.render('Game Paused: ESC to Resume', True, constants.DARKBLUE),
                          (90, 270))
        self.surface.blit(self.font_buttons.render('Restart Game', True, constants.BLACK),
                          ((constants.WIDTH // 2) - 190, 370))
        self.surface.blit(self.font_buttons.render('Quit Game', True, constants.BLACK),
                          ((constants.WIDTH // 2) - 190, 470))
        self.screen.blit(self.surface, (0, 0))

        return reset, quit

    def draw_game_over_menu(self) -> tuple[pygame.Rect, pygame.Rect]:
        """
        Draws the game over screen on a surface and displays it if game is lost
        Buttons to give the user the option to try again or quit

        :return:
        """
        pygame.mouse.set_visible(True)
        pygame.draw.rect(self.surface,
                         (0, 0, 0, 160),
                         [0, 0, constants.WIDTH, constants.HEIGHT])

        text_game_over = self.font_game_over.render(
            "YOU GOT SMASHED!", True, pygame.Color('red'))
        text_rect = text_game_over.get_rect(
            center=(constants.WIDTH // 2, constants.HEIGHT // 3))

        bg_surface = pygame.Surface(
            (text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 255))

        bg_rect = bg_surface.get_rect(center=text_rect.center)
        self.surface.blit(bg_surface, bg_rect)
        self.surface.blit(text_game_over, text_rect)

        button_width = 200
        button_height = 75
        button_x = (constants.WIDTH - button_width) // 2  # Center buttons horizontally
        button_y_start = constants.HEIGHT // 2
        button_spacing = 30

        # Draw buttons
        reset = pygame.Rect(button_x, button_y_start, button_width, button_height)
        self.draw_button("Try Again", button_x, button_y_start, button_width, button_height,
                         (0, 255, 0),
                         (0, 200, 0))

        quit = pygame.Rect(button_x, button_y_start + button_height + button_spacing, button_width,
                           button_height)
        self.draw_button("Quit", button_x, button_y_start + button_height + button_spacing, button_width, button_height,
                         (255, 0, 0),
                         (200, 0, 0))
        self.screen.blit(self.surface, (0, 0))
        return reset, quit

    def draw_game_intro(self) -> None:
        """
        Displays the intro screen where the player must press the spacebar to begin play

        :return:
        """
        self.screen.blit(self.font_buttons.render("Press SPACEBAR to start", True, constants.WHITE),
                         ((constants.WIDTH //4) + 50, constants.HEIGHT - (constants.HEIGHT // 6)))

    def draw_status(self, lives: int, score: int, level: int) -> None:
        """
        Draws each life in the top left corner of the screen
        Draws the score in the top right corner of the screen
        Draws the level name in the top middle of the screen

        :param lives:
        :param score:
        :param level:
        :return:
        """
        self.screen.blit(self.font_buttons.render("Lives:", True, constants.WHITE), (10, 10))
        for i in range(lives):
            pygame.draw.circle(self.screen, constants.WHITE, (130 + 35 * i, 27), 12)

        score_display = self.font_buttons.render(f"Score: {score}", True, constants.WHITE)
        self.screen.blit(score_display, (constants.WIDTH - score_display.get_width() - 100, 10))

        level_display = self.font_buttons.render(f"Level: {level}", True, constants.WHITE)
        self.screen.blit(level_display, ((constants.WIDTH - level_display.get_width()) / 2, 10))

    def draw_dev_overlay(self, gs: GameState) -> None:
        """
        Show the developer overlay

        :param gs: GameState
        :return:
        """
        str_build = (f"FPS: {gs.fps_avg:>6.1f}  "
                     f"LoopTime(ms): {gs.loop_time_avg:>4.1f}  "
                     f"MotionModel: {gs.motion_model.name}  "
                     f"Auto-Play: {gs.auto_play}")
        dev_overlay1 = self.font_fixed_small.render(str_build, True, constants.GREEN)

        str_build = (f"PaddleImpulse: {gs.paddle_impulse_vel_length:>4.2f}  "
                     f"Gravity: {gs.gravity_acc_length:>7.5f}  "
                     f"SpeedStep: {gs.ball_speed_step:>6.3f}")
        dev_overlay2 = self.font_fixed_small.render(str_build, True, constants.GREEN)

        self.screen.blit(dev_overlay1, ((constants.WIDTH - dev_overlay1.get_width()) / 2,
                                        constants.HEIGHT - dev_overlay1.get_height() - 5))
        self.screen.blit(dev_overlay2, ((constants.WIDTH - dev_overlay2.get_width()) / 2,
                                        constants.HEIGHT - dev_overlay2.get_height() - 24))

    def draw_splash_screen(self) -> None:
        """
        Show the splash screen

        :return:
        """
        logo_color = (255, 165, 0)
        text_color = constants.WHITE
        shadow_color = (100, 100, 100)

        logo_x, logo_y = constants.WIDTH // 2 - 150, constants.HEIGHT // 3
        font_smash = pygame.font.Font(None, 60)
        text_smash = font_smash.render("Smash", True, text_color)
        text_smash_shadow = font_smash.render("Smash", True, shadow_color)

        text_smash_rect = text_smash.get_rect(center=
                                              (logo_x + 100, logo_y + 40))
        text_smash_shadow_rect = text_smash_rect.copy()
        text_smash_shadow_rect.move_ip(3, 3)

        self.screen.blit(text_smash_shadow, text_smash_shadow_rect)
        self.screen.blit(text_smash, text_smash_rect)

        font_core = pygame.font.Font(None, 60)
        text_core = font_core.render("Core", True, text_color)
        text_core_shadow = font_core.render("Core", True, shadow_color)

        text_core_rect = text_core.get_rect(center=(logo_x + 230, logo_y + 80))
        text_core_shadow_rect = text_core_rect.copy()
        text_core_shadow_rect.move_ip(3, 3)

        self.screen.blit(text_core_shadow, text_core_shadow_rect)
        self.screen.blit(text_core, text_core_rect)

        pygame.draw.line(self.screen, logo_color,
                         (logo_x, logo_y + 120), (logo_x + 300, logo_y + 120),
                         3)

        font_arcade = pygame.font.Font(None, 24)
        text_arcade = font_arcade.render("The Retro Arcade Experience", True,
                                         (200, 200, 200))
        text_arcade_rect = text_arcade.get_rect(center=
                                                (logo_x + 150, logo_y + 150))
        self.screen.blit(text_arcade, text_arcade_rect)

    def initialize_background_elements(self):
        """Creates a set of bricks with different colors and multiple balls."""
        # Create multiple balls
        for _ in range(8): # Use this to change number of balls
            x = random.randint(0, constants.WIDTH)
            y = random.randint(0, constants.HEIGHT)
            speed_x = random.choice([-2, 2])
            speed_y = random.choice([-2, 2])
            ball_rect = pygame.Rect(x, y, constants.BALL_RADIUS * 2, constants.BALL_RADIUS * 2)
            ball_image = pygame.transform.scale(assets.BALL_IMG, (constants.BALL_RADIUS * 2, constants.BALL_RADIUS * 2))
            self.background_balls.append(
                {'rect': ball_rect, 'speed_x': speed_x, 'speed_y': speed_y, 'image': ball_image})

            # Create bricks with fixed positions and colors
        brick_data = [
            ((constants.WIDTH // 4, constants.HEIGHT // 4), constants.YELLOW),
            ((constants.WIDTH // 2, constants.HEIGHT // 3), constants.RED),
            ((constants.WIDTH // 3, constants.HEIGHT // 2), constants.ORANGE),
            ((constants.WIDTH // 5, constants.HEIGHT // 5 * 3), constants.LIGHTBLUE),
            ((constants.WIDTH // 6, constants.HEIGHT // 6 * 4), constants.GREEN),
            ((constants.WIDTH // 8 * 7, constants.HEIGHT // 8), constants.YELLOW),
            ((constants.WIDTH // 8, constants.HEIGHT // 8 * 7), constants.RED),
            ((constants.WIDTH // 2, constants.HEIGHT // 5 * 4), constants.ORANGE),
            ((constants.WIDTH // 5 * 4, constants.HEIGHT // 3), constants.LIGHTBLUE),
        ]

        for (x, y), color in brick_data:
            brick_surface = pygame.Surface((100, 50))
            brick_surface.fill(color)
            brick_rect = pygame.Rect(x, y, 100, 50)
            self.background_bricks.append({'rect': brick_rect, 'image': brick_surface})

    def update_background_elements(self):
        """Collisions for menu screen"""
        for ball in self.background_balls:
            ball['rect'].x += ball['speed_x']
            ball['rect'].y += ball['speed_y']
            if ball['rect'].left < 0 or ball['rect'].right > constants.WIDTH:
                ball['speed_x'] *= -1
                ball['speed_y'] += random.uniform(-0.5, 0.5)
            if ball['rect'].top < 0 or ball['rect'].bottom > constants.HEIGHT:
                ball['speed_y'] *= -1
                ball['speed_x'] += random.uniform(-0.5, 0.5)

            for brick in self.background_bricks:
                if ball['rect'].colliderect(brick['rect']):
                    overlap_x = min(ball['rect'].right, brick['rect'].right) - max(ball['rect'].left,
                                                                                   brick['rect'].left)
                    overlap_y = min(ball['rect'].bottom, brick['rect'].bottom) - max(ball['rect'].top,
                                                                                     brick['rect'].top)

                    if overlap_x > 0 and overlap_y > 0:
                        if abs(overlap_x) < abs(overlap_y):
                            if ball['speed_x'] > 0:
                                ball['rect'].right = brick['rect'].left
                            else:
                                ball['rect'].left = brick['rect'].right
                            ball['speed_x'] *= -1
                        else:
                            if ball['speed_y'] > 0:
                                ball['rect'].bottom = brick['rect'].top
                            else:
                                ball['rect'].top = brick['rect'].bottom
                            ball['speed_y'] *= -1

    def draw_start_screen(self) -> None:
        """
        Show the start screen

        :return:
        """
        self.surface.fill((0, 0, 0, 200))
        self.update_background_elements()

        for ball in self.background_balls:
            self.surface.blit(ball['image'], ball['rect'])

        for brick in self.background_bricks:
            self.surface.blit(brick['image'], brick['rect'])

        # Draw Click to Play button
        font = pygame.font.Font(None, 72)
        text = font.render("Click to Play", True, constants.BLACK)
        button_width = text.get_width() + 120
        button_height = text.get_height() + 60
        button_rect = pygame.Rect((constants.WIDTH - button_width) // 2,
                                  (constants.HEIGHT - button_height) // 2 + 50,
                                  button_width, button_height)
        pygame.draw.rect(self.surface, constants.RED, button_rect, border_radius=10)
        text_rect = text.get_rect(center=button_rect.center)
        self.surface.blit(text, text_rect)
        self.start_button_rect = button_rect

        # Draw How to Play Button
        how_to_play_width = 200
        how_to_play_height = 40
        how_to_play_x = (constants.WIDTH - how_to_play_width) // 2
        how_to_play_y = button_rect.y + button_height + 20
        how_to_play_rect = pygame.Rect(how_to_play_x, how_to_play_y, how_to_play_width, how_to_play_height)
        how_to_play_font = pygame.font.Font(None, 36)
        how_to_play_text = how_to_play_font.render("How to Play", True, constants.BLACK)
        how_to_play_text_rect = how_to_play_text.get_rect(center=how_to_play_rect.center)
        pygame.draw.rect(self.surface, constants.RED, how_to_play_rect, border_radius=10)
        self.surface.blit(how_to_play_text, how_to_play_text_rect)
        self.how_to_play_button_rect = how_to_play_rect

        # Draw Credits button
        credits_width = 100
        credits_height = 40
        credits_x = 20
        credits_y = constants.HEIGHT - credits_height - 30
        credits_rect = pygame.Rect(credits_x, credits_y, credits_width, credits_height)
        credits_font = pygame.font.Font(None, 36)
        credits_text = credits_font.render("Credits", True, constants.BLACK)
        credits_text_rect = credits_text.get_rect(center=credits_rect.center)

        pygame.draw.rect(self.surface, constants.RED, credits_rect, border_radius=10)
        self.surface.blit(credits_text, credits_text_rect)
        self.credits_button_rect = credits_rect

        self.screen.blit(self.surface, (0, 0))

    def draw_how_to_play_screen(self):
        """Shows how to play information when button is clicked"""
        self.surface.fill(constants.BLACK)
        font = pygame.font.Font(None, 30)
        text_lines = [
            "SmashCore is a brick-breaking game.",
            "Use the paddle to hit the ball.",
            "Break all bricks to win.",
            "",
            "ESC to pause.",
            "CTRL-D for dev stats."
        ]

        y = constants.HEIGHT // 4
        line_height = font.get_linesize() + 10

        for line in text_lines:
            rendered_text = font.render(line, True, constants.WHITE)
            text_rect = rendered_text.get_rect(center=(constants.WIDTH // 2, y))
            self.surface.blit(rendered_text, text_rect)
            y += line_height

        # Back button
        back_width = 100
        back_height = 40
        back_x = 20
        back_y = constants.HEIGHT - back_height - 30
        back_rect = pygame.Rect(back_x, back_y, back_width, back_height)
        self.draw_button("Back", back_rect.x, back_rect.y, back_rect.width, back_rect.height, constants.RED, constants.RED, None)
        self.how_to_play_back_button_rect = back_rect

        self.screen.blit(self.surface, (0, 0))

    def draw_credits_screen(self) -> None:
        """
        Show the credits screen

        :return:
        """
        self.surface.fill(constants.BLACK)
        font_credits = pygame.font.Font(None, 40)

        developers = ["DEVELOPERS", "", "Justin Cooke", "Ann Rauscher", "Camila Roxo", "Justin Smith", "Rex Vargas"]

        y_offset = constants.HEIGHT // 3
        for dev_name in developers:
            credits_text = font_credits.render("  " + dev_name, True, constants.WHITE)
            credits_rect = credits_text.get_rect(center=(constants.WIDTH // 2, y_offset))
            self.surface.blit(credits_text, credits_rect)
            y_offset += 50

            # Draws back button
            back_width = 100
            back_height = 40
            back_x = 20  # same x as credits button
            back_y = constants.HEIGHT - back_height - 30  # same y as credits button
            back_rect = pygame.Rect(back_x, back_y, back_width, back_height)
            back_font = pygame.font.Font(None, 36)
            back_text = back_font.render("Back", True, constants.BLACK)
            back_text_rect = back_text.get_rect(center=back_rect.center)

            pygame.draw.rect(self.surface, constants.RED, back_rect)  # same color as credits
            self.surface.blit(back_text, back_text_rect)
            self.back_button_rect = back_rect
            self.screen.blit(self.surface, (0, 0))


