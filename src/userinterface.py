"""
    UserInterface holds some of the UI drawing functions and could probably be expanded with more.
"""

import pygame
import constants


class UserInterface:

    def __init__(self):
        # Font setup
        self.font_game_over = pygame.font.Font(None, 100)
        self.font_buttons = pygame.font.Font(None, 50)
        # not certain this will reliably get a font (especially on diff OSes), but it's supposed to
        # fallback to a default pygame font
        self.font_fixed_small = pygame.font.SysFont("Courier", 16, True)
        self.surface = None
        self.screen = None

    # Button function
    def draw_button(self, text, x, y, width, height, color, hover_color, action=None):
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

    # Displays the pause menu where user can continue, restart, or quit the game
    def draw_pause_menu(self):
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

    # draws the game over screen on a surface and displays it if game is lost
    def draw_game_over_menu(self):
        pygame.mouse.set_visible(True)  # Show the cursor in game over screen
        pygame.draw.rect(self.surface, (0, 0, 0, 160), [0, 0, constants.WIDTH, constants.HEIGHT])

        # Game over screen
        text_game_over = self.font_game_over.render("YOU GOT SMASHED!", True, pygame.Color('red'))
        text_rect = text_game_over.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 3))
        self.surface.blit(text_game_over, text_rect)

        # Draw buttons
        reset = pygame.Rect(constants.WIDTH // 4, constants.HEIGHT // 2, 200, 75)
        self.draw_button("Play Again", constants.WIDTH // 4, constants.HEIGHT // 2, 200, 75,
                         (0, 255, 0),
                         (0, 200, 0))

        quit = pygame.Rect(constants.WIDTH * 3 // 4 - 100, constants.HEIGHT // 2, 200, 75)
        self.draw_button("Quit", constants.WIDTH * 3 // 4 - 100, constants.HEIGHT // 2, 200, 75,
                         (255, 0, 0),
                         (200, 0, 0))
        self.screen.blit(self.surface, (0, 0))

        return reset, quit

    def draw_game_intro(self):
        self.screen.blit(self.font_buttons.render("Press SPACEBAR to start", True, constants.WHITE),
                         ((constants.WIDTH //4) + 50, constants.HEIGHT - (constants.HEIGHT // 6)))

    # draws each life in the top left corner of the screen
    # draws the score in the top right corner of the screen
    # draws the level name in the top middle of the screen
    def draw_status(self, lives, score, level):
        self.screen.blit(self.font_buttons.render("Lives:", True, constants.WHITE), (10, 10))
        for i in range(lives):
            pygame.draw.circle(self.screen, constants.WHITE, (130 + 35 * i, 27), 12)

        score_display = self.font_buttons.render(f"Score: {score}", True, constants.WHITE)
        self.screen.blit(score_display, (constants.WIDTH - score_display.get_width() - 100, 10))

        level_display = self.font_buttons.render(f"Level: {level}", True, constants.WHITE)
        self.screen.blit(level_display, ((constants.WIDTH - level_display.get_width()) / 2, 10))

    # show the developer overlay
    def draw_dev_overlay(self, gs):
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


