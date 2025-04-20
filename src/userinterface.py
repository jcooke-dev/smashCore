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
from leaderboard import Leaderboard
import assets


class UserInterface:
    """ This provides a number of different UI element drawing functions """

    def __init__(self) -> None:
        # Define Main Menu buttons
        self.quit_button_start_rect = None
        self.leader_button_rect = None
        self.credits_button_rect = None
        self.how_to_play_button_rect = None
        self.start_button_rect = None
        self.back_button_rect = None

        # Font setups
        # font - logo (splash screen fonts)
        self.font_logo: pygame.font = pygame.font.Font(None, 60)
        self.font_logo_tagline: pygame.font = pygame.font.Font(None, 24)
        # font - main menu
        self.font_menu_main: pygame.font = pygame.font.Font(None, 72)
        self.font_menu_sub: pygame.font = pygame.font.Font(None, 36)
        # font - main menu elements
        self.font_h2p: pygame.font = pygame.font.Font(None, 30)
        self.font_credits: pygame.font = pygame.font.Font(None, 40)
        self.font_leaderboard: pygame.font = pygame.font.SysFont("Courier", 36, True)
        self.font_back_btn: pygame.font = pygame.font.Font(None, 36)
        #font - playing menus (game_over, pause, and highscore)
        self.font_title_text: pygame.font = pygame.font.Font(None, 100)
        self.font_subtitle_text: pygame.font = pygame.font.SysFont("Courier", 60, True)  # high scores
        self.font_buttons: pygame.font = pygame.font.Font(None, 50)
        # font - play screen elements
        self.font_game_intro: pygame.font = pygame.font.Font(None, 40)
        self.font_status: pygame.font = pygame.font.Font(None, 36)
        # not certain this will reliably get a font (especially on diff OSes), but it's supposed to
        # fall back to a default pygame font
        self.font_dev_overlay: pygame.font = pygame.font.SysFont("Courier", 16, True)  # dev overlay font

        self.surface: pygame.surface = None
        self.screen: pygame.surface = None
        self.tb_initials_text: str = ""
        self.background_balls = []
        self.background_bricks = []
        self.initialize_background_elements()

    def draw_button(self, text: pygame.Surface, x: int, y: int, width: int, height: int, color: pygame.color,
                    hover_color: pygame.color, action: Callable = None, corner_radius: int = 10) -> pygame.Rect:
        """
        Draw a button and return its Rect.

        :param corner_radius:
        :param text: button text
        :param x: Rect x
        :param y: Rect y
        :param width: Rect width
        :param height: Rect height
        :param color: button color
        :param hover_color: button hover color
        :param action: Function to call on click
        :return: pygame.Rect of the button
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, width, height)

        if rect.collidepoint(mouse):
            pygame.draw.rect(self.surface, hover_color, rect, border_radius=corner_radius)
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.surface, color, rect, border_radius=corner_radius)

        #text_surface = self.font_buttons.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        self.surface.blit(text, text_rect)
        return rect

    def draw_pause_menu(self) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        """
        Displays the pause menu where user can continue, restart, or quit the game

        :return:
        """
        pygame.mouse.set_visible(True)
        pygame.draw.rect(self.surface, (0, 0, 0, 140), [0, 0, constants.WIDTH, constants.HEIGHT])

        title1_text = self.font_title_text.render("Game Paused:", True, constants.YELLOW)
        title2_text = self.font_title_text.render("Press ESC to Continue", True, constants.YELLOW)
        title1_text_rect = title1_text.get_rect(center=(constants.WIDTH // 2, 270))
        title2_text_rect = title2_text.get_rect(center=(constants.WIDTH // 2, 350))

        self.surface.blit(title1_text, title1_text_rect)
        self.surface.blit(title2_text, title2_text_rect)

        button_width = 200
        button_height = 75
        button_x = (constants.WIDTH - button_width) // 2
        button_y_start = constants.HEIGHT // 2
        button_spacing = 30

        # Draw "Restart" button
        restart_text_surface = self.font_buttons.render("Restart", True, (0, 0, 0))
        restart_rect = self.draw_button(restart_text_surface, button_x, button_y_start,
                                        button_width, button_height, constants.GREEN, (0, 200, 0))

        # Draw "Main Menu" button
        main_menu_y = button_y_start + button_height + button_spacing
        menu_text_surface = self.font_buttons.render("Main Menu", True, (0, 0, 0))
        main_menu_rect = self.draw_button(menu_text_surface, button_x, main_menu_y,
                                          button_width, button_height, constants.YELLOW, (200, 200, 0))

        # Draw "Quit" button
        quit_y = main_menu_y + button_height + button_spacing
        quit_text_surface = self.font_buttons.render("Quit", True, (0, 0, 0))
        quit_rect = self.draw_button(quit_text_surface, button_x, quit_y,
                                     button_width, button_height, constants.RED, (200, 0, 0))

        self.screen.blit(self.surface, (0, 0))

        return restart_rect, main_menu_rect, quit_rect

    def draw_game_over_menu(self, go_to_main_menu_action: Callable = None) -> (
            tuple)[pygame.Rect, pygame.Rect, pygame.Rect]:
        """
        Draws the game over screen with options to try again, go to main menu, and quit.

        :param go_to_main_menu_action: Function to call when the "Main Menu" button is clicked.
        :return: Tuple of Rects for "Try Again", "Main Menu", and "Quit" buttons.
        """
        pygame.mouse.set_visible(True)
        pygame.draw.rect(self.surface, (0, 0, 0, 140), [0, 0, constants.WIDTH, constants.HEIGHT])

        text_game_over = self.font_title_text.render("YOU GOT SMASHED!", True, pygame.Color('red'))
        text_rect = text_game_over.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 3))

        bg_surface = pygame.Surface((text_rect.width + 20, text_rect.height + 10), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 255))
        bg_rect = bg_surface.get_rect(center=text_rect.center)

        self.surface.blit(bg_surface, bg_rect)
        self.surface.blit(text_game_over, text_rect)

        button_width = 200
        button_height = 75
        button_x = (constants.WIDTH - button_width) // 2
        button_y_start = constants.HEIGHT // 2
        button_spacing = 30

        # Draw "Try Again" button
        reset_text_surface = self.font_buttons.render("Try Again", True, (0, 0, 0))
        reset_rect = self.draw_button(reset_text_surface, button_x, button_y_start,
                                      button_width, button_height, constants.GREEN, (0, 200, 0))

        # Draw "Main Menu" button
        main_menu_y = button_y_start + button_height + button_spacing
        menu_text_surface = self.font_buttons.render("Main Menu", True, (0, 0, 0))
        main_menu_rect = self.draw_button(menu_text_surface, button_x, main_menu_y,
                                          button_width, button_height, constants.YELLOW, (200, 200, 0),
                                          go_to_main_menu_action)

        # Draw "Quit" button
        quit_y = main_menu_y + button_height + button_spacing
        quit_text_surface = self.font_buttons.render("Quit", True, (0, 0, 0))
        quit_rect = self.draw_button(quit_text_surface, button_x, quit_y,
                                     button_width, button_height, constants.RED, (200, 0, 0))

        self.screen.blit(self.surface, (0, 0))

        return reset_rect, main_menu_rect, quit_rect

    def draw_get_high_score(self) -> pygame.Rect:
        """
        Draws the screen for getting high score initials.

        :return: Rect of the "Enter" button.
        """
        pygame.mouse.set_visible(True)
        pygame.draw.rect(self.surface, (0, 0, 0, 140), [0, 0, constants.WIDTH, constants.HEIGHT])

        # draw message
        text_high_score1 = self.font_subtitle_text.render("That's a high score!", True, constants.YELLOW)
        text_rect1 = text_high_score1.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 3))

        text_high_score2 = self.font_subtitle_text.render("Please enter your initials:", True, constants.YELLOW)
        text_rect2 = text_high_score2.get_rect(center=(constants.WIDTH // 2, (constants.HEIGHT // 3) + 80))

        bg_surface1 = pygame.Surface((text_rect1.width + 20, text_rect1.height + 10), pygame.SRCALPHA)
        bg_surface1.fill((0, 0, 0, 255))

        bg_surface2 = pygame.Surface((text_rect2.width + 20, text_rect2.height + 10), pygame.SRCALPHA)
        bg_surface2.fill((0, 0, 0, 255))

        bg_rect1 = bg_surface1.get_rect(center=text_rect1.center)
        bg_rect2 = bg_surface2.get_rect(center=text_rect2.center)

        self.surface.blit(bg_surface1, (bg_rect1.x, bg_rect1.y))
        self.surface.blit(text_high_score1, (text_rect1.x, text_rect1.y))

        self.surface.blit(bg_surface2, (bg_rect2.x, bg_rect2.y))
        self.surface.blit(text_high_score2, (text_rect2.x, text_rect2.y))

        # draw input box
        color = (0, 255, 0)
        backcolor = (255, 255, 255, 192)
        pos = (constants.WIDTH / 2, text_rect2.y + 150)
        text = "---" if len(self.tb_initials_text) == 0 else self.tb_initials_text
        tb_text = self.font_title_text.render(text, True, color, constants.BLACK)
        tb_text_rect = tb_text.get_rect(center=pos)

        pygame.draw.rect(self.surface, backcolor, tb_text_rect.inflate(2, 2), 200)
        self.surface.blit(tb_text, tb_text_rect)

        # draw enter button
        button_width = 200
        button_height = 75
        button_x = (constants.WIDTH - button_width) // 2
        button_y_start = tb_text_rect.y + 125

        enter_text_surface = self.font_buttons.render("Enter", True, (0, 0, 0))
        enter_btn_rect = self.draw_button(enter_text_surface, button_x, button_y_start,
                                          button_width, button_height, constants.GREEN, (0, 200, 0))

        self.screen.blit(self.surface, (0, 0))

        return enter_btn_rect

    def draw_game_intro(self) -> None:
        """
        Displays the intro screen where the player must press the spacebar to begin play

        :return:
        """
        game_intro_text = self.font_game_intro.render("Press SPACEBAR to begin", True, constants.WHITE)
        intro_rect = game_intro_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT - (constants.HEIGHT // 6)))

        self.screen.blit(game_intro_text, intro_rect)

    def draw_status(self, lives: int, score: int, level: int) -> None:
        """
        Draws each life, score, and level on the screen.

        :param lives: Number of remaining lives.
        :param score: Current game score.
        :param level: Current game level.
        :return: None
        """
        self.screen.blit(self.font_status.render("Lives:", True, constants.WHITE), (10, 10))
        for i in range(lives):
            pygame.draw.circle(self.screen, constants.WHITE, (170 + 35 * i, 27), 12)

        score_display = self.font_status.render(f"Score: {score}", True, constants.WHITE)
        self.screen.blit(score_display, (constants.WIDTH - score_display.get_width() - 100, 10))

        level_display = self.font_status.render(f"Level: {level}", True, constants.WHITE)
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
        dev_overlay1 = self.font_dev_overlay.render(str_build, True, constants.GREEN)

        str_build = (f"PaddleImpulse: {gs.paddle_impulse_vel_length:>4.2f}  "
                     f"Gravity: {gs.gravity_acc_length:>7.5f}  "
                     f"SpeedStep: {gs.ball_speed_step:>6.3f}")
        dev_overlay2 = self.font_dev_overlay.render(str_build, True, constants.GREEN)

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
        text_smash = self.font_logo.render("Smash", True, text_color)
        text_smash_shadow = self.font_logo.render("Smash", True, shadow_color)

        text_smash_rect = text_smash.get_rect(center=(logo_x + 100, logo_y + 40))
        text_smash_shadow_rect = text_smash_rect.copy()
        text_smash_shadow_rect.move_ip(3, 3)

        self.screen.blit(text_smash_shadow, text_smash_shadow_rect)
        self.screen.blit(text_smash, text_smash_rect)

        text_core = self.font_logo.render("Core", True, text_color)
        text_core_shadow = self.font_logo.render("Core", True, shadow_color)

        text_core_rect = text_core.get_rect(center=(logo_x + 230, logo_y + 80))
        text_core_shadow_rect = text_core_rect.copy()
        text_core_shadow_rect.move_ip(3, 3)

        self.screen.blit(text_core_shadow, text_core_shadow_rect)
        self.screen.blit(text_core, text_core_rect)

        pygame.draw.line(self.screen, logo_color, (logo_x, logo_y + 120), (logo_x + 300, logo_y + 120), 3)

        text_logo_tagline = self.font_logo_tagline.render("The Retro Arcade Experience", True, (200, 200, 200))
        text_logo_tagline_rect = text_logo_tagline.get_rect(center=(logo_x + 150, logo_y + 150))
        self.screen.blit(text_logo_tagline, text_logo_tagline_rect)

    def initialize_background_elements(self):
        """Creates a set of bricks with different colors and multiple balls."""
        # Create multiple balls
        for _ in range(8):  # Use this to change number of balls
            x = random.randint(0, constants.WIDTH)
            y = random.randint(0, constants.HEIGHT)
            speed_x = random.choice([-2, 2])
            speed_y = random.choice([-2, 2])
            ball_rect = pygame.Rect(x, y, constants.BALL_RADIUS * 2, constants.BALL_RADIUS * 2)
            ball_image = pygame.transform.scale(assets.BALL_IMG, (constants.BALL_RADIUS * 2, constants.BALL_RADIUS * 2))
            self.background_balls.append \
                ({'rect': ball_rect, 'speed_x': speed_x, 'speed_y': speed_y, 'image': ball_image})

            # Create bricks with fixed positions and colors
        brick_data = [
            ((constants.WIDTH // 4, constants.HEIGHT // 4), constants.YELLOW),
            ((constants.WIDTH // 2, constants.HEIGHT // 3), constants.GREEN),
            ((constants.WIDTH // 3, constants.HEIGHT // 2), constants.ORANGE),
            ((constants.WIDTH // 5, constants.HEIGHT // 5 * 3), constants.LIGHTBLUE),
            ((constants.WIDTH // 6, constants.HEIGHT // 6 * 4), constants.RED),
            ((constants.WIDTH // 8 * 7, constants.HEIGHT // 8), constants.YELLOW),
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
                    overlap_x = min(ball['rect'].right, brick['rect'].right) - \
                                max(ball['rect'].left, brick['rect'].left)
                    overlap_y = min(ball['rect'].bottom, brick['rect'].bottom) - \
                                max(ball['rect'].top, brick['rect'].top)

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
        start_text = self.font_menu_main.render("Click to Play", True, constants.BLACK)
        button_width = start_text.get_width() + 120
        button_height = start_text.get_height() + 60

        self.start_button_rect = self.draw_button(start_text, (constants.WIDTH - button_width) // 2,
                                                  (constants.HEIGHT - button_height) // 2 + 50, button_width,
                                                  button_height,
                                                  constants.GREEN, (0, 200, 0))

        sub_button_width = 200
        sub_button_height = 40
        # Draw How to Play Button
        how_to_play_x = (constants.WIDTH - sub_button_width) // 2
        how_to_play_y = self.start_button_rect.y + button_height + 20
        how_to_play_text = self.font_menu_sub.render("How to Play", True, constants.BLACK)
        self.how_to_play_button_rect = self.draw_button(how_to_play_text, how_to_play_x, how_to_play_y,
                                                        sub_button_width, sub_button_height, constants.YELLOW,
                                                        (200, 200, 0))

        # Draw Credits button
        credits_x = 20
        credits_y = constants.HEIGHT - sub_button_height - 30
        credits_text = self.font_menu_sub.render("Credits", True, constants.BLACK)
        self.credits_button_rect = self.draw_button(credits_text, credits_x, credits_y,
                                                    sub_button_width, sub_button_height, constants.YELLOW,
                                                    (200, 200, 0))

        leader_x = 20  # a little to the right
        leader_y = constants.HEIGHT - sub_button_height - sub_button_height - 60  # a little higher
        leader_text = self.font_menu_sub.render("Leaderboard", True,
                                                constants.BLACK)  # same color as the rest of the buttons
        self.leader_button_rect = self.draw_button(leader_text, leader_x, leader_y,
                                                   sub_button_width, sub_button_height, constants.YELLOW,
                                                   (200, 200, 0))

        # Draw Quit button
        quit_x = constants.WIDTH - sub_button_width - 20
        quit_y = constants.HEIGHT - sub_button_height - 30
        quit_text = self.font_menu_sub.render("Quit", True, constants.BLACK)
        self.quit_button_start_rect = self.draw_button(quit_text, quit_x, quit_y,
                                                       sub_button_width, sub_button_height, constants.RED,
                                                       (200, 0, 0))

        self.screen.blit(self.surface, (0, 0))

    def draw_how_to_play_screen(self) -> None:
        """Shows how to play information when button is clicked"""
        self.surface.fill(constants.BLACK)
        text_lines = [
            "SmashCore is a brick-breaking game.",
            "Use a mouse, trackpad, or the arrow keys to control the paddle.",
            "Use the paddle to hit the ball.",
            "Break all the bricks to win.",
            "",
            "ESC to pause.",
            "CTRL-D for dev stats."
        ]

        y = constants.HEIGHT // 4
        line_height = self.font_h2p.get_linesize() + 10

        for line in text_lines:
            rendered_text = self.font_h2p.render(line, True, constants.WHITE)
            text_rect = rendered_text.get_rect(center=(constants.WIDTH // 2, y))
            self.surface.blit(rendered_text, text_rect)
            y += line_height

        # Back button
        back_width = 100
        back_height = 40
        back_x = 20
        back_y = constants.HEIGHT - back_height - 30
        back_text = self.font_back_btn.render("Back", True, constants.BLACK)
        self.back_button_rect = self.draw_button(back_text, back_x, back_y,
                                                 back_width, back_height, constants.YELLOW,
                                                 (200, 200, 0))
        self.screen.blit(self.surface, (0, 0))

    def draw_credits_screen(self) -> None:
        """
        Show the credits screen

        :return:
        """
        self.surface.fill(constants.BLACK)

        developers = ["DEVELOPERS", "", "Justin Cooke", "Ann Rauscher", "Camila Roxo", "Justin Smith", "Rex Vargas"]

        y_offset = constants.HEIGHT // 3
        for dev_name in developers:
            credits_text = self.font_credits.render("  " + dev_name, True, constants.WHITE)
            credits_rect = credits_text.get_rect(center=(constants.WIDTH // 2, y_offset))
            self.surface.blit(credits_text, credits_rect)
            y_offset += 50

        # Back button
        back_width = 100
        back_height = 40
        back_x = 20
        back_y = constants.HEIGHT - back_height - 30
        back_text = self.font_back_btn.render("Back", True, constants.BLACK)
        self.back_button_rect = self.draw_button(back_text, back_x, back_y,
                                                 back_width, back_height, constants.YELLOW,
                                                 (200, 200, 0))
        self.screen.blit(self.surface, (0, 0))

    def draw_leaderboard_screen(self, lb: Leaderboard) -> None:
        """
        Show the leaderboard screen

        :return:
        """
        self.surface.fill(constants.BLACK)

        l_scores = ["HIGH SCORES", ""]

        score_sorted = sorted(lb.l_top_scores, key=lambda scr: scr.score, reverse=True)
        for scr in score_sorted:
            str_build = (f"{scr.id}  "
                         f"{scr.score:>8d}   "
                         f"(level: {scr.level:>2d})")
            l_scores.append(str_build)

        y_offset = constants.HEIGHT // 6
        for score_str in l_scores:
            score_text = self.font_leaderboard.render("  " + score_str, True, constants.WHITE)
            score_rect = score_text.get_rect(center=(constants.WIDTH // 2, y_offset))
            self.surface.blit(score_text, score_rect)
            y_offset += 50

        # Back button
        back_width = 100
        back_height = 40
        back_x = 20
        back_y = constants.HEIGHT - back_height - 30
        back_text = self.font_back_btn.render("Back", True, constants.BLACK)
        self.back_button_rect = self.draw_button(back_text, back_x, back_y,
                                                 back_width, back_height, constants.YELLOW,
                                                 (200, 200, 0))
        # draw everything
        self.screen.blit(self.surface, (0, 0))
