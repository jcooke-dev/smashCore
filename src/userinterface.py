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

import brick
import constants
import obstacle
from gamesettings import GameSettings
from gamestate import GameState
from leaderboard import Leaderboard
import assets


class UserInterface:
    """ This provides a number of different UI element drawing functions """

    def __init__(self) -> None:
        # Define Main Menu buttons
        self.knob_sf_rect = None
        self.knob_bg_rect = None
        self.pad_btn_rect = None
        self.graphics_btn_rect = None
        self.vol_sfx_btn_rect = None
        self.vol_bgm_btn_rect = None
        self.settings_button_rect = None
        self.quit_button_start_rect = None
        self.leader_button_rect = None
        self.credits_button_rect = None
        self.how_to_play_button_rect = None
        self.start_classic_button_rect = None
        self.start_modern_button_rect = None
        self.back_button_rect = None

        # Font setups
        # font - logo (splash screen fonts)
        self.font_logo: pygame.font = pygame.font.Font(None, 100)
        self.font_logo_tagline: pygame.font = pygame.font.Font(None, 30)
        # font - main menu
        self.font_menu_main: pygame.font = pygame.font.Font(None, 36)
        self.font_menu_sub: pygame.font = pygame.font.Font(None, 30)
        # font - main menu elements
        self.font_h2p: pygame.font = pygame.font.Font(None, 30)
        self.font_credits: pygame.font = pygame.font.Font(None, 40)
        self.font_leaderboard: pygame.font = pygame.font.SysFont("Courier", 36, True)
        self.font_back_btn: pygame.font = pygame.font.Font(None, 36)
        self.font_settings: pygame.font = pygame.font.SysFont("Courier", 36, True)
        #font - playing menus (game_over, pause, and highscore)
        self.font_title_text: pygame.font = pygame.font.Font(None, 100)
        self.font_subtitle_text: pygame.font = pygame.font.SysFont("Courier", 60, True)  # high scores
        self.font_buttons: pygame.font = pygame.font.Font(None, 50)
        # font - play screen elements
        self.font_game_intro: pygame.font = pygame.font.Font(None, 60)
        self.font_status: pygame.font = pygame.font.Font(None, 52)
        # not certain this will reliably get a font (especially on diff OSes), but it's supposed to
        # fall back to a default pygame font
        self.font_dev_overlay: pygame.font = pygame.font.SysFont("Courier", 16, True)  # dev overlay font

        self.surface: pygame.Surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        self.screen: pygame.surface = None
        self.tb_initials_text: str = ""
        self.background_balls = []
        self.background_bricks = []
        self.initialize_background_elements()

    def draw_button(self, btn_surface: pygame.Surface, x: int, y: int, width: int, height: int, color: pygame.color,
                    hover_color: pygame.color, action: Callable = None, corner_radius: int = 10) -> pygame.Rect:
        """
        Draw a button and return its Rect.

        :param corner_radius:
        :param btn_surface: button text
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

        text_rect = btn_surface.get_rect(center=rect.center)
        self.surface.blit(btn_surface, text_rect)
        return rect

    def draw_back_button(self):
        # Back button
        back_width = 100
        back_height = 40
        back_x = 20
        back_y = constants.HEIGHT - back_height - 30
        back_text = self.font_back_btn.render("Back", True, constants.BLACK)
        self.back_button_rect = self.draw_button(back_text, back_x, back_y,
                                                 back_width, back_height,
                                                 constants.YELLOW,
                                                 constants.DARK_YELLOW)

    def draw_pause_menu(self, gset: GameSettings) -> tuple[pygame.Rect, pygame.Rect, pygame.Rect]:
        """
        Displays the pause menu where user can continue, restart, or quit the game

        :param gset: game settings

        :return: tuple[pygame.Rect, pygame.Rect, pygame.Rect] each for try again, mainmenu, and quit buttons
        """
        pygame.mouse.set_visible(True)
        pygame.draw.rect(self.surface, (0, 0, 0, 140), [0, 0, constants.WIDTH, constants.HEIGHT])

        title1_text = self.font_title_text.render("Game Paused:", True, constants.YELLOW)
        title2_text = self.font_title_text.render("Press ESC to Continue", True, constants.YELLOW)
        pad_btn_lbl = self.font_buttons.render('Paddle Control', True, constants.WHITE)
        title1_text_rect = title1_text.get_rect(center=(constants.WIDTH // 2, 170))
        title2_text_rect = title2_text.get_rect(center=(constants.WIDTH // 2, 250))
        pad_btn_lbl_rect = pad_btn_lbl.get_rect(topright=(constants.WIDTH // 2, 350))

        self.surface.blit(title1_text, title1_text_rect)
        self.surface.blit(title2_text, title2_text_rect)
        self.surface.blit(pad_btn_lbl, pad_btn_lbl_rect)

        # Draw Paddle Control button
        if gset.paddle_under_auto_control:
            pad_btn_text = self.font_buttons.render("Auto", True, constants.BLACK)
        else:
            pad_btn_text = self.font_buttons.render("Mouse", True,
                                                    constants.BLACK) if gset.paddle_under_mouse_control else self.font_buttons.render(
                "Keyboard", True, constants.BLACK)
        self.pad_btn_rect = self.draw_button(pad_btn_text, pad_btn_lbl_rect.x + pad_btn_lbl.get_width() + 10,
                                             pad_btn_lbl_rect.y - 3,
                                             200, 40, (200, 200, 200), constants.GRAY)

        button_width = 200
        button_height = 75
        button_x = (constants.WIDTH - button_width) // 2
        button_y_start = (constants.HEIGHT + button_height) // 2
        button_spacing = 30

        # Draw "Restart" button
        restart_text_surface = self.font_buttons.render("Restart", True, (0, 0, 0))
        restart_rect = self.draw_button(restart_text_surface, button_x, button_y_start,
                                        button_width, button_height, constants.GREEN, constants.DARK_GREEN)

        # Draw "Main Menu" button
        main_menu_y = button_y_start + button_height + button_spacing
        menu_text_surface = self.font_buttons.render("Main Menu", True, (0, 0, 0))
        main_menu_rect = self.draw_button(menu_text_surface, button_x, main_menu_y,
                                          button_width, button_height, constants.YELLOW, constants.DARK_YELLOW)

        # Draw "Quit" button
        quit_y = main_menu_y + button_height + button_spacing
        quit_text_surface = self.font_buttons.render("Quit", True, (0, 0, 0))
        quit_rect = self.draw_button(quit_text_surface, button_x, quit_y,
                                     button_width, button_height, constants.RED, constants.DARK_RED)

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
        button_y_start = (constants.HEIGHT + button_height) // 2
        button_spacing = 30

        # Draw "Try Again" button
        reset_text_surface = self.font_buttons.render("Try Again", True, (0, 0, 0))
        reset_rect = self.draw_button(reset_text_surface, button_x, button_y_start,
                                      button_width, button_height, constants.GREEN, constants.DARK_GREEN)

        # Draw "Main Menu" button
        main_menu_y = button_y_start + button_height + button_spacing
        menu_text_surface = self.font_buttons.render("Main Menu", True, (0, 0, 0))
        main_menu_rect = self.draw_button(menu_text_surface, button_x, main_menu_y,
                                          button_width, button_height, constants.YELLOW, constants.DARK_YELLOW,
                                          go_to_main_menu_action)

        # Draw "Quit" button
        quit_y = main_menu_y + button_height + button_spacing
        quit_text_surface = self.font_buttons.render("Quit", True, (0, 0, 0))
        quit_rect = self.draw_button(quit_text_surface, button_x, quit_y,
                                     button_width, button_height, constants.RED, constants.DARK_RED)

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
        tb_text = self.font_subtitle_text.render(text, True, color, constants.BLACK)
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
                                          button_width, button_height, constants.GREEN, constants.DARK_GREEN)

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
            pygame.draw.circle(self.screen, constants.WHITE, (140 + 35 * i, 27), 12)

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

    def draw_logo(self, logo_x, logo_y) -> None:
        """
        Show the splash screen

        :return:
        """
        logo_color = constants.ORANGE
        text_color = constants.WHITE
        shadow_color = (100, 100, 100)

        text_smash = self.font_logo.render("Smash", True, text_color)
        text_smash_shadow = self.font_logo.render("Smash", True, shadow_color)
        text_core = self.font_logo.render("Core", True, text_color)
        text_core_shadow = self.font_logo.render("Core", True, shadow_color)

        # find center of logo smash core text
        logo_width = text_smash.get_width() + text_core.get_width()
        logo_center = logo_width // 2
        smash_x = logo_x - logo_center  # offset smash x position by the center of logo

        text_smash_rect = text_smash.get_rect(x=smash_x, y=(logo_y + 40))
        text_smash_shadow_rect = text_smash_rect.copy()
        text_smash_shadow_rect.move_ip(3, 3)

        # start Core after Smash (smash x position + smash width)
        text_core_rect = text_core.get_rect(x=(text_smash_rect.x + text_smash_rect.width),
                                            y=(text_smash_rect.y + text_smash_rect.height))

        text_core_shadow_rect = text_core_rect.copy()
        text_core_shadow_rect.move_ip(3, 3)

        # find the x, y position the line based on the placement and width of smash core text
        line_start_x = text_smash_rect.x - 20
        line_end_x = text_core_shadow_rect.x + text_core_shadow_rect.width + 20
        line_y = text_core_shadow_rect.y + text_core_shadow_rect.height + 15
        pygame.draw.line(self.screen, logo_color, (line_start_x, line_y), (line_end_x, line_y), 3)

        text_logo_tagline = self.font_logo_tagline.render("The Retro Arcade Experience", True, (200, 200, 200))
        text_logo_tagline_rect = text_logo_tagline.get_rect(
            center=(logo_x, text_core_shadow_rect.y + text_core_shadow_rect.height + 40))

        self.screen.blit(text_smash_shadow, text_smash_shadow_rect)
        self.screen.blit(text_smash, text_smash_rect)
        self.screen.blit(text_core_shadow, text_core_shadow_rect)
        self.screen.blit(text_core, text_core_rect)
        self.screen.blit(text_logo_tagline, text_logo_tagline_rect)

    def draw_splash_screen(self):
        self.draw_logo(constants.WIDTH // 2, constants.HEIGHT // 4)

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
            ((constants.WIDTH // 4.5, constants.HEIGHT // 4), constants.YELLOW),
            ((constants.WIDTH // 2, constants.HEIGHT // 3), constants.GREEN),
            ((constants.WIDTH // 3, constants.HEIGHT // 2), constants.ORANGE),
            ((constants.WIDTH // 5, constants.HEIGHT // 5 * 3), constants.LIGHT_BLUE),
            ((constants.WIDTH // 6, constants.HEIGHT // 6 * 4), constants.RED),
            ((constants.WIDTH // 8 * 7, constants.HEIGHT // 8), constants.YELLOW),
            ((constants.WIDTH // 6 * 4, constants.HEIGHT // 5 * 4), constants.ORANGE),
            ((constants.WIDTH // 5 * 4, constants.HEIGHT // 3), constants.LIGHT_BLUE),
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

        # Draw Click to Play CLASSIC button
        start_text = self.font_menu_main.render("PLAY CLASSIC MODE", True, constants.BLACK)
        button_width = start_text.get_width() + 30
        button_height = start_text.get_height() + 40
        button_x = constants.WIDTH // 2 - button_width
        self.start_classic_button_rect = self.draw_button(start_text, button_x,
                                                          340, button_width,
                                                          button_height,
                                                          constants.GREEN, constants.DARK_GREEN)

        # Draw Click to Play MODERN button
        start_text = self.font_menu_main.render("PLAY MODERN MODE", True, constants.BLACK)
        button_width = start_text.get_width() + 30
        button_height = start_text.get_height() + 40

        self.start_modern_button_rect = self.draw_button(start_text, button_x * 2,
                                                         340,
                                                         button_width, button_height,
                                                         constants.LIGHT_BLUE, constants.DARK_BLUE)

        sub_button_width = 250
        sub_button_height = 50
        sub_button_spacing = sub_button_height + 15
        sub_button_x = (constants.WIDTH - sub_button_width) // 2
        sub_button_y = self.start_modern_button_rect.y + self.start_modern_button_rect.height + sub_button_height  # Add or subtract to this to adjust sub_buttons y_position
        # Draw How to Play Button
        how_to_play_text = self.font_menu_sub.render("How to Play", True, constants.BLACK)
        self.how_to_play_button_rect = self.draw_button(how_to_play_text, sub_button_x, sub_button_y,
                                                        sub_button_width, sub_button_height,
                                                        constants.YELLOW, constants.DARK_YELLOW)

        # Draw Leaderboards button
        leader_text = self.font_menu_sub.render("Leaderboard", True,
                                                constants.BLACK)  # same color as the rest of the buttons
        self.leader_button_rect = self.draw_button(leader_text, sub_button_x, sub_button_y + (1 * sub_button_spacing),
                                                   sub_button_width, sub_button_height,
                                                   constants.YELLOW, constants.DARK_YELLOW)

        # Draw Settings button
        settings_text = self.font_menu_sub.render("Settings", True, constants.BLACK)
        self.settings_button_rect = self.draw_button(settings_text, sub_button_x,
                                                     sub_button_y + (2 * sub_button_spacing),
                                                     sub_button_width, sub_button_height,
                                                     constants.YELLOW, constants.DARK_YELLOW)

        # Draw Credits button
        credits_text = self.font_menu_sub.render("Credits", True, constants.BLACK)
        self.credits_button_rect = self.draw_button(credits_text, sub_button_x, sub_button_y + (3 * sub_button_spacing),
                                                    sub_button_width, sub_button_height,
                                                    constants.YELLOW, constants.DARK_YELLOW)

        # Draw Quit button
        quit_text = self.font_menu_sub.render("Quit", True, constants.BLACK)
        self.quit_button_start_rect = self.draw_button(quit_text, sub_button_x,
                                                       sub_button_y + int(4.3 * sub_button_spacing),
                                                       sub_button_width, sub_button_height,
                                                       constants.RED, constants.DARK_RED)

        self.screen.blit(self.surface, (0, 0))
        self.draw_logo(constants.WIDTH // 2, 30)

    def draw_how_to_play_screen(self) -> None:
        """Shows how to play information when button is clicked"""
        self.surface.fill(constants.BLACK)
        text1_lines = [
            "GAMEPLAY INSTRUCTIONS",
            "",
            "SmashCore is a brick-breaking game.",
            "Use a mouse, trackpad, or the arrow keys to control the paddle.",
            "Use the paddle to reflect the ball and hit the bricks.",
            "Breaking all of the bricks clears the level.",
        ]
        text2_lines = [
            "KEYBOARD SHORTCUTS",
            "",
            "ESC to pause.",
            "CTRL + D for dev stats.",
            "CTRL + - to decrease overall volume.",
            "CTRL + = to increase overall volume."
        ]

        y1 = 75
        y2 = y1
        line_height = self.font_h2p.get_linesize() + 10

        for line in text1_lines:
            rendered_text = self.font_h2p.render(line, True, constants.WHITE)
            text_rect = rendered_text.get_rect(topleft=(50, y1))
            self.surface.blit(rendered_text, text_rect)
            y1 += line_height

        for line in text2_lines:
            rendered_text = self.font_h2p.render(line, True, constants.WHITE)
            text_rect = rendered_text.get_rect(topleft=(constants.WIDTH // 2 + 150, y2))
            self.surface.blit(rendered_text, text_rect)
            y2 += line_height

        pygame.draw.line(self.surface, constants.ORANGE, (75, y2 + 25), (constants.WIDTH - 75, y2 + 25), 3)

        btn_text = self.font_menu_main.render("CLASSIC MODE", True, constants.BLACK)
        button_width = btn_text.get_width() + 20
        button_height = btn_text.get_height() + 20
        self.draw_button(btn_text, 50, y2 + 50, button_width,
                         button_height, constants.GREEN, constants.DARK_GREEN)

        mode_text = self.font_h2p.render("Play the game with solid color bricks.", True, constants.WHITE)
        mode_text_rect = mode_text.get_rect(topleft=(button_width + 75, y2 + 50 + (btn_text.get_height() // 2)))
        self.surface.blit(mode_text, mode_text_rect)

        btn_text = self.font_menu_main.render("MODERN MODE", True, constants.BLACK)
        self.draw_button(btn_text, 50, y2 + 125, button_width,
                         button_height, constants.LIGHT_BLUE, constants.DARK_BLUE)

        mode_text = self.font_h2p.render("Play the game with modern image bricks.", True, constants.WHITE)
        mode_text_rect = mode_text.get_rect(topleft=(button_width + 75, y2 + 125 + (btn_text.get_height() // 2)))
        self.surface.blit(mode_text, mode_text_rect)

        y3 = y2 + 175 + (button_height // 2)
        pygame.draw.line(self.surface, constants.ORANGE, (75, y3), (constants.WIDTH - 75, y3), 3)

        norm_brick = pygame.Rect(50, y3 + 25, 100, 50)
        brick.Brick(norm_brick, constants.RED).draw_wo(self.surface)
        norm_brick = pygame.Rect(50 + 125, y3 + 25, 100, 50)
        norm_img_brick = pygame.transform.scale(assets.BRK_RED_IMG, (norm_brick.width, norm_brick.height))
        brick.Brick(norm_brick, constants.GREEN, image=norm_img_brick).draw_wo(self.surface)
        brick_lbl = self.font_h2p.render("Normal Bricks", True, constants.WHITE)
        brick_lbl_rect = brick_lbl.get_rect(midleft=(norm_brick.x + norm_brick.width + 20, norm_brick.centery))
        self.surface.blit(brick_lbl, brick_lbl_rect)

        mult_brick = pygame.Rect(50, y3 + 100, 100, 50)
        brick.Brick(mult_brick, constants.YELLOW, strength=5, bonus=1).draw_wo(self.surface)
        mult_brick = pygame.Rect(50 + 125, y3 + 100, 100, 50)
        mult_img_brick = pygame.transform.scale(assets.BRK_GOLD_IMG, (mult_brick.width, mult_brick.height))
        brick.Brick(mult_brick, constants.YELLOW, image=mult_img_brick, strength=5, bonus=1).draw_wo(self.surface)
        brick_lbl = self.font_h2p.render("Multi-Hit Breakable Bricks", True, constants.WHITE)
        brick_lbl_rect = brick_lbl.get_rect(midleft=(mult_brick.x + mult_brick.width + 20, mult_brick.centery))
        self.surface.blit(brick_lbl, brick_lbl_rect)

        obst_brick = pygame.Rect(50, y3 + 175, 100, 50)
        obstacle.Obstacle(obst_brick, constants.GRAY, text="X X X").draw_wo(self.surface)
        obst_brick = pygame.Rect(50 + 125, y3 + 175, 100, 50)
        obst_img_brick = pygame.transform.scale(assets.BRK_OBSTACLE_IMG, (obst_brick.width, obst_brick.height))
        obstacle.Obstacle(obst_brick, constants.GRAY, image=obst_img_brick).draw_wo(self.surface)
        brick_lbl = self.font_h2p.render("Unbreakable Bricks", True, constants.WHITE)
        brick_lbl_rect = brick_lbl.get_rect(midleft=(obst_brick.x + obst_brick.width + 20, obst_brick.centery))
        self.surface.blit(brick_lbl, brick_lbl_rect)

        text3_lines = [
            "SCORING SYSTEM",
            "",
            "On random levels, each brick has a random value",
            "in the range of (1 - 10).",
            "On other levels, each brick in a row has a value",
            "of [10, 7, 5, 3, 1] starting from the top.",
            "Multi-hit bricks have a 10 point bonus."
        ]

        for line in text3_lines:
            rendered_text = self.font_h2p.render(line, True, constants.WHITE)
            text_rect = rendered_text.get_rect(topleft=(brick_lbl_rect.width + brick_lbl_rect.x + 150, y3 + 25))
            self.surface.blit(rendered_text, text_rect)
            y3 += line_height

        # Back button
        self.draw_back_button()
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
        self.draw_back_button()

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
        self.draw_back_button()

        # draw everything
        self.screen.blit(self.surface, (0, 0))

    def draw_settings_screen(self, gset: GameSettings) -> None:
        """
        Show the settings screen

        :param gset: game settings

        :return:
        """
        bg_sound = assets.VOLUME_ICON.convert_alpha() if gset.bgm_sounds and gset.music_volume > 0 else assets.MUTE_ICON.convert_alpha()
        sfx_sound = assets.VOLUME_ICON.convert_alpha() if gset.sfx_sounds and gset.sfx_volume > 0 else assets.MUTE_ICON.convert_alpha()

        self.surface.fill(constants.BLACK)

        title_text = self.font_subtitle_text.render("SETTINGS", True, constants.WHITE)
        self.surface.blit(title_text, title_text.get_rect(center=(constants.WIDTH // 2, 100)))

        left_align_x = constants.WIDTH // 6

        # show the graphics windowed/fullscreen toggle
        graphics_btn_lbl_y = (constants.HEIGHT // 3)
        graphics_btn_lbl = self.font_settings.render('Graphics Mode       ', True, constants.WHITE)
        self.surface.blit(graphics_btn_lbl,
                          graphics_btn_lbl.get_rect(bottomleft=(left_align_x, graphics_btn_lbl_y - 10)))

        if gset.is_fullscreen:
            graphics_btn_text = self.font_buttons.render("Fullscreen", True, constants.BLACK)
        else:
            graphics_btn_text = self.font_buttons.render("Windowed", True, constants.BLACK)

        self.graphics_btn_rect = self.draw_button(graphics_btn_text, left_align_x + graphics_btn_lbl.get_width() + 20,
                                                  graphics_btn_lbl_y - graphics_btn_lbl.get_height() - 10,
                                                  210, 40, (200, 200, 200), constants.GRAY)

        #icon_width, icon_height default = 330, 50
        icon_width, icon_height = 75, 75
        knob_radius = constants.KNOB_RADIUS

        #draw the bgm volume icons and sliders to the surface
        bg_icon_y = graphics_btn_lbl_y + icon_height
        bg_sound = pygame.transform.scale(bg_sound, (icon_width, icon_height))

        bgm_text = self.font_settings.render('BGM Volume', True, constants.WHITE)
        self.surface.blit(bgm_text, bgm_text.get_rect(bottomleft=(left_align_x, bg_icon_y - 10)))
        self.vol_bgm_btn_rect = self.draw_button(bg_sound, left_align_x, bg_icon_y, icon_width, icon_height,
                                                 (0, 0, 0, 0), (200, 200, 200, 0))

        slider_bg_x = self.vol_bgm_btn_rect.centerx + 75
        slider_bg_y = self.vol_bgm_btn_rect.centery - (constants.SLIDER_HEIGHT // 2)
        knob_bg_x = slider_bg_x - knob_radius + int(
            gset.music_volume * constants.SLIDER_WIDTH) if gset.bgm_sounds else slider_bg_x - knob_radius
        knob_bg_y = slider_bg_y + (constants.SLIDER_HEIGHT // 2) - knob_radius

        slider_bgm_rect = pygame.Rect(slider_bg_x, slider_bg_y, constants.SLIDER_WIDTH, constants.SLIDER_HEIGHT)
        pygame.draw.rect(self.surface, constants.WHITE, slider_bgm_rect, border_radius=20)
        knob_bg = pygame.Surface((knob_radius * 2, knob_radius * 2), pygame.SRCALPHA)
        self.knob_bg_rect = self.draw_button(knob_bg, knob_bg_x, knob_bg_y, knob_radius * 2, knob_radius * 2,
                                             constants.GRAY, constants.LIGHT_GRAY, corner_radius=knob_radius)

        # draws the sfx volume icons and sliders to the surface
        sfx_icon_y = bg_icon_y + icon_height + 100
        sfx_sound = pygame.transform.scale(sfx_sound, (icon_width, icon_height))
        sfx_text = self.font_settings.render('SFX Volume', True, constants.WHITE)
        self.surface.blit(sfx_text, sfx_text.get_rect(bottomleft=(left_align_x, sfx_icon_y - 10)))
        self.vol_sfx_btn_rect = self.draw_button(sfx_sound, left_align_x, sfx_icon_y, icon_width, icon_height,
                                                 (0, 0, 0, 0), (200, 200, 200, 0))

        slider_sf_x = self.vol_sfx_btn_rect.centerx + 75
        slider_sf_y = self.vol_sfx_btn_rect.centery - (constants.SLIDER_HEIGHT // 2)
        knob_sf_x = slider_sf_x - knob_radius + int(
            gset.sfx_volume * constants.SLIDER_WIDTH) if gset.sfx_sounds else slider_sf_x - knob_radius
        knob_sf_y = slider_sf_y + (constants.SLIDER_HEIGHT // 2) - knob_radius

        slider_sfx_rect = pygame.Rect(slider_sf_x, slider_sf_y, constants.SLIDER_WIDTH, constants.SLIDER_HEIGHT)
        pygame.draw.rect(self.surface, constants.WHITE, slider_sfx_rect, border_radius=20)
        knob_sf = pygame.Surface((knob_radius * 2, knob_radius * 2), pygame.SRCALPHA)
        self.knob_sf_rect = self.draw_button(knob_sf, knob_sf_x, knob_sf_y, knob_radius * 2, knob_radius * 2,
                                             constants.GRAY, constants.LIGHT_GRAY, corner_radius=knob_radius)

        pad_btn_lbl_y = sfx_icon_y + icon_height + 100
        pad_btn_lbl = self.font_settings.render('Paddle Control      ', True, constants.WHITE)
        self.surface.blit(pad_btn_lbl, pad_btn_lbl.get_rect(bottomleft=(left_align_x, pad_btn_lbl_y - 10)))

        if gset.paddle_under_auto_control:
            pad_btn_text = self.font_buttons.render("Auto", True, constants.BLACK)
        else:
            pad_btn_text = self.font_buttons.render("Mouse", True,
                                                    constants.BLACK) if gset.paddle_under_mouse_control else self.font_buttons.render(
                "Keyboard", True, constants.BLACK)

        self.pad_btn_rect = self.draw_button(pad_btn_text, left_align_x + pad_btn_lbl.get_width() + 20,
                                             pad_btn_lbl_y - pad_btn_lbl.get_height() - 10,
                                             210, 40, (200, 200, 200), constants.GRAY)

        self.draw_back_button()

        # draw everything
        self.screen.blit(self.surface, (0, 0))
