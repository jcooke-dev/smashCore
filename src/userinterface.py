"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: UserInterface contains the various UI element drawing functions.
"""

import pygame
import constants


class UserInterface:
    """ This provides a number of different UI element drawing functions """

    def __init__(self):
        # Font setup
        self.font_game_over = pygame.font.Font(None, 100)
        self.font_buttons = pygame.font.Font(None, 50)
        # not certain this will reliably get a font (especially on diff OSes), but it's supposed to
        # fallback to a default pygame font
        self.font_fixed_small = pygame.font.SysFont("Courier", 16, True)
        self.font_fixed_large = pygame.font.SysFont("Courier", 35, True)
        self.font_fixed_xlarge = pygame.font.SysFont("Courier", 60, True)
        self.surface = None
        self.screen = None
        self.tb_initials_text = ""

    def draw_button(self, text, x, y, width, height, color, hover_color, action=None):
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

    def draw_pause_menu(self):
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

    def draw_game_over_menu(self):
        """
        Draws the game over screen on a surface and displays it if game is lost
        Buttons to give the user the option to try again or quit

        :return:
        """

        pygame.mouse.set_visible(True)
        pygame.draw.rect(self.surface,
                         (0, 0, 0, 140),
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

    def draw_get_high_score(self):
        """
        Draws the game over screen on a surface and displays it if game is lost
        Buttons to give the user the option to try again or quit

        :return:
        """

        pygame.mouse.set_visible(True)
        pygame.draw.rect(self.surface,
                         (0, 0, 0, 140),
                         [0, 0, constants.WIDTH, constants.HEIGHT])

        # draw message
        text_high_score1 = self.font_game_over.render(
            "That's a high score!", True, constants.YELLOW)
        text_rect1 = text_high_score1.get_rect(
            center=(constants.WIDTH // 2, constants.HEIGHT // 3))

        text_high_score2 = self.font_game_over.render(
            "Please enter your initials:", True, constants.YELLOW)
        text_rect2 = text_high_score2.get_rect(
            center=(constants.WIDTH // 2, (constants.HEIGHT // 3) + 80))

        bg_surface1 = pygame.Surface(
            (text_rect1.width + 20, text_rect1.height + 10), pygame.SRCALPHA)
        bg_surface1.fill((0, 0, 0, 255))

        bg_surface2 = pygame.Surface(
            (text_rect2.width + 20, text_rect2.height + 10), pygame.SRCALPHA)
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
        width = 400
        text = "---" if len(self.tb_initials_text) == 0 else self.tb_initials_text
        tb_text = self.font_fixed_xlarge.render(text, True, color, constants.BLACK)
        tb_text_rect = tb_text.get_rect(center=pos)

        pygame.draw.rect(self.surface, backcolor, tb_text_rect.inflate(2, 2), 200)
        self.surface.blit(tb_text, tb_text_rect)

        # draw enter button
        button_width = 200
        button_height = 75
        button_x = (constants.WIDTH - button_width) // 2  # Center buttons horizontally
        button_y_start = tb_text_rect.y + 125

        enter_btn = pygame.Rect(button_x, button_y_start, button_width, button_height)
        self.draw_button("Enter", button_x, button_y_start, button_width, button_height,
                         (0, 255, 0),
                         (0, 200, 0))

        self.screen.blit(self.surface, (0, 0))

        return enter_btn

    def draw_game_intro(self):
        """
        Displays the intro screen where the player must press the spacebar to begin play

        :return:
        """
        self.screen.blit(self.font_buttons.render("Press SPACEBAR to start", True, constants.WHITE),
                         ((constants.WIDTH //4) + 50, constants.HEIGHT - (constants.HEIGHT // 6)))

    def draw_status(self, lives, score, level):
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

    def draw_dev_overlay(self, gs):
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

    def draw_splash_screen(self):
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

    def draw_start_screen(self):
        """
        Show the start screen

        :return:
        """
        self.surface.fill(constants.BLACK)
        font = pygame.font.Font(None, 48)
        text = font.render("Click to Play", True, constants.BLACK)
        button_width = text.get_width() + 40
        button_height = text.get_height() + 20
        button_rect = pygame.Rect((constants.WIDTH - button_width) // 2,(constants.HEIGHT - button_height)
                                  // 2 + 50, button_width, button_height)
        pygame.draw.rect(self.surface, constants.WHITE, button_rect)
        text_rect = text.get_rect(center=button_rect.center)
        self.surface.blit(text, text_rect)
        self.start_button_rect = button_rect
        self.screen.blit(self.surface, (0, 0))

        # add Credits button
        credits_width = 185
        credits_height = 40
        credits_x = 20  # a little to the right
        credits_y = constants.HEIGHT - credits_height - 30  # a little higher
        credits_rect = pygame.Rect(credits_x, credits_y, credits_width, credits_height)
        credits_font = pygame.font.Font(None, 36)  # same size as the rest of the buttons.
        credits_text = credits_font.render("Credits", True, constants.BLACK)  # same color as the rest of the buttons
        credits_text_rect = credits_text.get_rect(center=credits_rect.center)

        pygame.draw.rect(self.surface, (150, 150, 150), credits_rect)
        self.surface.blit(credits_text, credits_text_rect)

        self.credits_button_rect = credits_rect

        self.screen.blit(self.surface, (0, 0))

        # add Leaderboard button
        leader_width = 185
        leader_height = 40
        leader_x = 20  # a little to the right
        leader_y = constants.HEIGHT - credits_height - leader_height - 60  # a little higher
        leader_rect = pygame.Rect(leader_x, leader_y, leader_width, leader_height)
        leader_font = pygame.font.Font(None, 36)  # same size as the rest of the buttons.
        leader_text = leader_font.render("Leaderboard", True, constants.BLACK)  # same color as the rest of the buttons
        leader_text_rect = leader_text.get_rect(center=leader_rect.center)

        pygame.draw.rect(self.surface, (150, 150, 150), leader_rect)
        self.surface.blit(leader_text, leader_text_rect)

        self.leader_button_rect = leader_rect

        self.screen.blit(self.surface, (0, 0))

    def draw_credits_screen(self):
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
        back_x = 10
        back_y = constants.HEIGHT - back_height - 10
        back_rect = pygame.Rect(back_x, back_y, back_width, back_height)
        back_font = pygame.font.Font(None, 36)
        back_text = back_font.render("Back", True, constants.BLACK)
        back_text_rect = back_text.get_rect(center=back_rect.center)

        pygame.draw.rect(self.surface, (150, 150, 150), back_rect)
        self.surface.blit(back_text, back_text_rect)
        self.back_button_rect = back_rect
        self.screen.blit(self.surface, (0, 0))

    def draw_leaderboard_screen(self, lb):
        """
        Show the leaderboard screen

        :return:
        """
        self.surface.fill(constants.BLACK)

        l_scores = []
        l_scores.append("HIGH SCORES")
        l_scores.append("")

        score_sorted = sorted(lb.l_top_scores, key=lambda scr: scr.score, reverse=True)
        for scr in score_sorted:
            str_build = (f"{scr.id}  "
                         f"{scr.score:>8d}   "
                         f"(level: {scr.level:>2d})")
            l_scores.append(str_build)

        y_offset = constants.HEIGHT // 6
        for score_str in l_scores:
            score_text = self.font_fixed_large.render("  " + score_str, True, constants.WHITE)
            score_rect = score_text.get_rect(center=(constants.WIDTH // 2, y_offset))
            self.surface.blit(score_text, score_rect)
            y_offset += 50

        # Draws back button
        back_width = 100
        back_height = 40
        back_x = 10
        back_y = constants.HEIGHT - back_height - 10
        back_rect = pygame.Rect(back_x, back_y, back_width, back_height)
        back_font = pygame.font.Font(None, 36)
        back_text = back_font.render("Back", True, constants.BLACK)
        back_text_rect = back_text.get_rect(center=back_rect.center)

        pygame.draw.rect(self.surface, (150, 150, 150), back_rect)
        self.surface.blit(back_text, back_text_rect)
        self.back_button_rect = back_rect

        # draw everything
        self.screen.blit(self.surface, (0, 0))
