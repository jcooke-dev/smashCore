"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This brings together the various modules that make up the game (GameWorld,
                        GameState, UI, etc.) and runs the main game loop.
"""

import pygame

import persistence
from src.ball import Ball
from src.brick import Brick
from src.constants import (WIDTH, HEIGHT, INITIAL_FPS_SIMPLE, GAME_NAME,
    PAD_WIDTH, START_LIVES, START_SCORE, BALL_SPEED_VECTOR, BALL_SPEED_SIMPLE,
    BALL_SPEED_LEVEL_INCREMENT, BLACK, SPLASH_TIME_SECS,
    PADDLE_IMPULSE_INCREMENT, WORLD_GRAVITY_ACC_INCREMENT,
    BALL_SPEED_STEP_INCREMENT, MAX_FPS_VECTOR, SCORE_INITIALS_MAX)
from src.levels import Levels
from src.gameworld import GameWorld
from gamestates import GameStates
from motionmodels import MotionModels

import utils


class GameEngine:
    """ The main engine that drives the game loop """

    def __init__(self, lb, ps, gw, gs, ui):
        """

        :param ps: PlayerState
        :param gw: GameWorld
        :param gs: GameState
        :param ui: UserInterface
        """
        self.mouse_pos = None
        self.lb = lb
        self.ps = ps
        self.gw = gw
        self.gs = gs
        self.ui = ui

        ui.screen = self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        ui.surface = self.surface = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.fps = INITIAL_FPS_SIMPLE

        # record the app start ticks to time the splash screen display
        self.app_start_ticks = pygame.time.get_ticks()

        pygame.display.set_caption(GAME_NAME)

        # Initially, hide the mouse cursor
        pygame.mouse.set_visible(False)

    def reset_game(self):
        """
        Resets the game to the initial state

        :return:
        """
        # does python run auto garbage collection so it's OK to just
        # assign a new gw?
        self.gw = GameWorld(Levels.LevelName.SMASHCORE_1)
        self.fps = INITIAL_FPS_SIMPLE
        self.gs.cur_state = GameStates.SPLASH
        self.gs.cur_ball_x = (WIDTH / 2) - (PAD_WIDTH / 2)
        self.ps.lives = START_LIVES
        self.ps.score = START_SCORE
        self.ps.level = 1
        pygame.mouse.set_visible(False)  # Hide the cursor when game restarts


    def next_level(self):
        """
        Builds the next level, resets the ball position and initial speed
        Slight increase in initial ball speed to add difficulty

        :return:
        """
        for wo in self.gw.world_objects:
            if isinstance(wo, Ball):
                wo.reset_position()
                wo.speed_v = BALL_SPEED_VECTOR + (self.ps.level * BALL_SPEED_LEVEL_INCREMENT)
                wo.speed = BALL_SPEED_SIMPLE + (self.ps.level * BALL_SPEED_LEVEL_INCREMENT)
        # builds level in cycles of the 4 levels
        if self.ps.level % 4 == 1:
            Levels.build_level(self.gw, Levels.LevelName.SMASHCORE_1)
        if self.ps.level % 4 == 2:
            Levels.build_level(self.gw, Levels.LevelName.SMASHCORE_SOLID_ROWS_1)
        if self.ps.level % 4 == 3:
            Levels.build_level(self.gw, Levels.LevelName.SMASHCORE_IMG_CHAMFER_1)
        if self.ps.level % 4 == 0:
            Levels.build_level(self.gw, Levels.LevelName.SMASHCORE_SOLID_ROWS_IMG_CHAMFER_1)

        self.fps = INITIAL_FPS_SIMPLE
        self.gs.cur_state = GameStates.READY_TO_LAUNCH
        #self.gs.ball_speed_step += BALL_SPEED_STEP_INCREMENT

    def draw_world_and_status(self):
        """
        Draw all objects in GameWorld plus status overlays

        :return:
        """
        # draw every game object
        for world_object in self.gw.world_objects:
            world_object.draw_wo(self.screen)
        # draw any status overlays
        self.ui.draw_status(self.ps.lives, self.ps.score, self.ps.level)

    def menu_screen_handler(self):
        """
        Checks for button presses and shifts to the proper GameSate

        :return:
        """
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ui.start_button_rect.collidepoint(event.pos):
                    self.gs.cur_state = GameStates.READY_TO_LAUNCH
                elif self.ui.credits_button_rect.collidepoint(event.pos):
                    self.gs.cur_state = GameStates.CREDITS

    def clean_shutdown(self):
        self.gs.running = False
        self.gs.cur_state = GameStates.GAME_OVER

        # store leaderboard
        self.lb.store(persistence.LEADERBOARD_FILE_PATH)

        pygame.quit()
        exit()


    def run_loop(self):
        """
        Runs the main game loop

        :return:
        """

        while self.gs.running:
            # fill the screen with black as a good default
            self.screen.fill(BLACK)

            match self.gs.cur_state:

                ##############################################################
                # display the SPLASH screen
                ##############################################################
                case GameStates.SPLASH:
                    # placeholder for the splash screen graphic
                    self.ui.draw_splash_screen()

                    # go beyond the splash GameState after desired time
                    cur_ticks = pygame.time.get_ticks()
                    if ((cur_ticks - self.app_start_ticks) / 1000) > SPLASH_TIME_SECS:
                        self.gs.cur_state = GameStates.MENU_SCREEN

                ##############################################################
                # display the MENU SCREEN
                ##############################################################
                case GameStates.MENU_SCREEN:
                    self.ui.draw_start_screen()
                    pygame.mouse.set_visible(True)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.clean_shutdown()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.ui.start_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameStates.READY_TO_LAUNCH
                            elif self.ui.credits_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameStates.CREDITS
                            elif self.ui.leader_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameStates.LEADERBOARD

                ##############################################################
                # display credits screen
                ##############################################################
                case GameStates.CREDITS:
                    self.ui.draw_credits_screen()
                    pygame.mouse.set_visible(True)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # Add this line
                            self.clean_shutdown()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.ui.back_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameStates.MENU_SCREEN

                ##############################################################
                # display leaderboard screen
                ##############################################################
                case GameStates.LEADERBOARD:
                    self.ui.draw_leaderboard_screen(self.lb)
                    pygame.mouse.set_visible(True)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # Add this line
                            self.clean_shutdown()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.ui.back_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameStates.MENU_SCREEN

                ##############################################################
                # display the PLAYING gameplay screen
                ##############################################################
                case GameStates.PLAYING | GameStates.READY_TO_LAUNCH:
                    # Hide the mouse again when transitioning away from the start screen.
                    pygame.mouse.set_visible(False)
                    # update all objects in GameWorld
                    mouse_pos = pygame.mouse.get_pos()
                    for current_wo in self.gw.world_objects:
                        # this controls whether the AutoPlay system or the
                        # player's mouse input is driving the paddle
                        current_wo.commanded_pos_x = self.gs.cur_ball_x if self.gs.auto_play else mouse_pos[0]
                        current_wo.update_wo(self.gs, self.ps, self.lb)
                        # test for collisions between world_objects, but ignore
                        # objects that can't be affected (for performance)
                        if current_wo.can_react:
                            for other_wo in self.gw.world_objects:
                                # don't check for collisions with self
                                if current_wo is not other_wo:
                                    if current_wo.rect.colliderect(other_wo.rect):
                                        # a collision was detected - should we react to it?  this matters because two
                                        # objects can overlap/collide across multiple looping collision checks - if
                                        # we don't deactivate the collision detection, the object can bounce back and
                                        # forth, getting trapped
                                        if other_wo.allow_collision():
                                            # bounce object properly -
                                            # determining in which direction
                                            # to bounce, based on approach
                                            current_wo.detect_collision(other_wo, self.gs)
                                            other_wo.add_collision()
                                            if other_wo.should_remove():
                                                self.ps.score += other_wo.value
                                                # special effect
                                                #  TODO probably need to store this brick rect and set
                                                #  it to be displayed for some duration because we sometimes don't see
                                                #  the inflation effect, likely because it's removed before being drawn
                                                other_wo.rect.inflate_ip(current_wo.rect.width * 3,
                                                                         current_wo.rect.height * 3)
                                                pygame.draw.rect(self.screen, other_wo.color, other_wo.rect)
                                                current_wo.speed += .20
                                                # BALL_SPEED_STEP: adding to the ball speed, but diff logic for the
                                                # VECTOR models
                                                if isinstance(current_wo, Ball):
                                                    current_wo.speed_v += self.gs.ball_speed_step
                                                    current_wo.v_vel = current_wo.v_vel_unit * current_wo.speed_v

                                                self.gw.world_objects.remove(other_wo)

                                    else:
                                        # this is the other side of the allow_collision logic above, since
                                        # not colliding now, it resets the latch or 'primed for collision' flag
                                        other_wo.prime_for_collision()

                    # draw all objects in GameWorld
                    self.draw_world_and_status()

                    # note this is the way the player enters the gameplay
                    # screen, in a pending, ready to launch mode, with the
                    # ball stuck to the paddle
                    if self.gs.cur_state == GameStates.READY_TO_LAUNCH:
                        self.ui.draw_game_intro()

                    if not any(isinstance(wo, Brick) for wo in self.gw.world_objects):
                        self.ps.level += 1
                        self.next_level()

                ##############################################################
                # display the PAUSED popup over the frozen gameplay
                ##############################################################
                case GameStates.PAUSED:
                    # draw all objects in GameWorld
                    self.draw_world_and_status()
                    # getting the rects for the UI buttons for later collision
                    # detection (button pressing)
                    self.restart_game, self.quit_game = self.ui.draw_pause_menu()
                    pygame.mouse.set_visible(True)

                ##############################################################
                # display the GET_HIGH_SCORE popup over the frozen gameplay
                ##############################################################
                case GameStates.GET_HIGH_SCORE:
                    # draw all objects in GameWorld
                    self.draw_world_and_status()
                    # getting the rects for the UI buttons for later collision
                    # detection (button pressing)
                    self.high_score_enter_btn = self.ui.draw_get_high_score()

                ##############################################################
                # display the GAME_OVER popup over the frozen gameplay
                ##############################################################
                case GameStates.GAME_OVER:
                    # draw all objects in GameWorld
                    self.draw_world_and_status()
                    # getting the rects for the UI buttons for later collision
                    # detection (button pressing)
                    self.restart_game, self.quit_game = self.ui.draw_game_over_menu()

            ##############################################################
            # event handling
            ##############################################################

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.clean_shutdown()

                if event.type == pygame.KEYDOWN:
                    # toggle PAUSE GameState with ESCAPE key press
                    if event.key == pygame.K_ESCAPE:
                        if self.gs.cur_state == GameStates.PAUSED:
                            self.gs.cur_state = GameStates.PLAYING
                            pygame.mouse.set_pos(self.mouse_pos)
                            pygame.mouse.set_visible(False)
                        elif self.gs.cur_state == GameStates.PLAYING:
                            self.gs.cur_state = GameStates.PAUSED
                            self.mouse_pos = pygame.mouse.get_pos()
                            pygame.mouse.set_visible(True)

                    if event.key == pygame.K_SPACE:
                        if self.gs.cur_state == GameStates.READY_TO_LAUNCH:
                            self.gs.cur_state = GameStates.PLAYING

                    # detect the CTRL+d key combo to toggle the dev overlay
                    # calculation and display
                    if event.key == pygame.K_d:
                        if event.mod & pygame.KMOD_CTRL:
                            self.gs.show_dev_overlay = not self.gs.show_dev_overlay

                    # detect the CTRL+a key combo to toggle the AUTO-PLAY mode
                    # on and off
                    if event.key == pygame.K_a:
                        if event.mod & pygame.KMOD_CTRL:
                            self.gs.auto_play = not self.gs.auto_play

                    # detect the CTRL+p and CTRL+SHIFT+p key combos to
                    # increase/decrease the PADDLE_IMPULSE
                    if event.key == pygame.K_p:
                        if event.mod & pygame.KMOD_CTRL:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.gs.paddle_impulse_vel_length -= PADDLE_IMPULSE_INCREMENT
                                if self.gs.paddle_impulse_vel_length < 0.0:
                                    self.gs.paddle_impulse_vel_length = 0.0
                            else:
                                self.gs.paddle_impulse_vel_length += PADDLE_IMPULSE_INCREMENT

                    # detect the CTRL+g and CTRL+SHIFT+g key combos to
                    # increase/decrease the WORLD_GRAVITY_ACC
                    if event.key == pygame.K_g:
                        if event.mod & pygame.KMOD_CTRL:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.gs.gravity_acc_length -= WORLD_GRAVITY_ACC_INCREMENT
                                if self.gs.gravity_acc_length < 0.0:
                                    self.gs.gravity_acc_length = 0.0
                                self.gs.v_gravity_acc = self.gs.v_gravity_unit * self.gs.gravity_acc_length
                            else:
                                self.gs.gravity_acc_length += WORLD_GRAVITY_ACC_INCREMENT
                                self.gs.v_gravity_acc = self.gs.v_gravity_unit * self.gs.gravity_acc_length

                    # detect the CTRL+s and CTRL+SHIFT+s key combos to
                    # increase/decrease the BALL_SPEED_STEP
                    if event.key == pygame.K_s:
                        if event.mod & pygame.KMOD_CTRL:
                            if event.mod & pygame.KMOD_SHIFT:
                                self.gs.ball_speed_step -= BALL_SPEED_STEP_INCREMENT
                            else:
                                self.gs.ball_speed_step += BALL_SPEED_STEP_INCREMENT

                    # detect the CTRL+m key combo to cycle through the various motion models
                    if event.key == pygame.K_m:
                        if event.mod & pygame.KMOD_CTRL:
                            match self.gs.motion_model:
                                case MotionModels.SIMPLE_1:
                                    self.gs.motion_model = MotionModels.VECTOR_1
                                case MotionModels.VECTOR_1:
                                    self.gs.motion_model = MotionModels.SIMPLE_1

                    # handle initials textbox input
                    if self.gs.cur_state == GameStates.GET_HIGH_SCORE:
                        if (event.key == pygame.K_RETURN) or (event.key == pygame.K_KP_ENTER):
                            self.lb.add_score(self.ps, self.ui)
                            self.gs.cur_state = GameStates.GAME_OVER
                        elif event.key == pygame.K_BACKSPACE:
                            self.ui.tb_initials_text = self.ui.tb_initials_text[:-1]
                        elif len(self.ui.tb_initials_text) < SCORE_INITIALS_MAX:
                            self.ui.tb_initials_text += event.unicode

                # the actual button press checks from the returned rects above
                if (event.type == pygame.MOUSEBUTTONDOWN and
                        ((self.gs.cur_state == GameStates.PAUSED) or
                         (self.gs.cur_state == GameStates.GAME_OVER))):
                    if self.restart_game.collidepoint(event.pos):
                        self.reset_game()
                    if self.quit_game.collidepoint(event.pos):
                        self.clean_shutdown()
                    if self.gs.cur_state == GameStates.GAME_OVER:
                        if self.credits_game.collidepoint(event.pos):
                            self.gs.cur_state = GameStates.CREDITS

                if (event.type == pygame.MOUSEBUTTONDOWN and
                        (self.gs.cur_state == GameStates.GET_HIGH_SCORE)):
                    if self.high_score_enter_btn.collidepoint(event.pos):
                        self.lb.add_score(self.ps, self.ui)
                        self.gs.cur_state = GameStates.GAME_OVER

            # draw the developer overlay, if requested
            if self.gs.show_dev_overlay:
                self.ui.draw_dev_overlay(self.gs)

            ##############################################################
            # update screen
            ##############################################################
            pygame.display.flip()

            # choose from the available motion models; note that SIMPLE models
            # use clock.tick(fps) to force the motion update logic to the
            # frame rate - VECTOR models decouple the frame rate from the
            # dT motion logic
            if self.gs.motion_model == MotionModels.SIMPLE_1:
                self.gs.tick_time = self.clock.tick(self.fps)
            elif self.gs.motion_model == MotionModels.VECTOR_1:
                # removing the fps arg (rather, setting it to 0) allows pygame
                # to run this loop at full speed
                # self.gs.tick_time = self.clock.tick(MAX_FPS_VECTOR)
                self.gs.tick_time = self.clock.tick_busy_loop(MAX_FPS_VECTOR)

            # don't bother calculating these running dev averages unless wanted
            if self.gs.show_dev_overlay:
                self.gs.fps_avg, self.gs.loop_time_avg = utils.calculate_timing_averages(self.clock.get_fps(), self.clock.get_time())

        ##############################################################
        # close down cleanly
        ##############################################################
        pygame.quit()
