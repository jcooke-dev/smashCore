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
from sys import exit
import pygame

import utils
import persistence
import assets
from ball import Ball
from brick import Brick
from paddle import Paddle
from constants import (WIDTH, HEIGHT, INITIAL_FPS_SIMPLE, GAME_NAME,
                       PAD_WIDTH, START_LIVES, START_SCORE, BALL_SPEED_VECTOR, BALL_SPEED_SIMPLE,
                       BALL_SPEED_LEVEL_INCREMENT, BLACK, SPLASH_TIME_SECS,
                       PADDLE_IMPULSE_INCREMENT, WORLD_GRAVITY_ACC_INCREMENT,
                       BALL_SPEED_STEP_INCREMENT, MAX_FPS_VECTOR, SCORE_INITIALS_MAX,
                       MUSIC_VOLUME_STEP, SLIDER_WIDTH, KNOB_RADIUS)
from levels import Levels
from gameworld import GameWorld
from userinterface import UserInterface
from playerstate import PlayerState
from leaderboard import Leaderboard
from gamestate import GameState
from motionmodels import MotionModels


class GameEngine:
    """ The main engine that drives the game loop """

    def __init__(self, lb: Leaderboard, ps: PlayerState, gw: GameWorld, gs: GameState, ui: UserInterface) -> None:
        """
        
        :param ps: PlayerState
        :param gw: GameWorld
        :param gs: GameState
        :param ui: UserInterface
        """
        self.prev_state = None
        self.quit_game_button = None
        self.restart_game_button = None
        self.main_menu_button = None
        self.high_score_enter_btn = None
        self.mouse_pos = None
        self.lb: Leaderboard = lb
        self.ps: PlayerState = ps
        self.gw: GameWorld = gw
        self.gs: GameState = gs
        self.ui: UserInterface = ui

        self.screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface: pygame.Surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self.clock: pygame.time = pygame.time.Clock()
        self.fps: float = INITIAL_FPS_SIMPLE

        # record the app start ticks to time the splash screen display
        self.app_start_ticks: float = pygame.time.get_ticks()
        self.gs.cur_state = GameState.GameStateName.SPLASH

        pygame.display.set_caption(GAME_NAME)

        ui.screen = self.screen
        ui.surface = self.surface

        # Initially, hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Initialize game music and paths
        pygame.mixer.init()
        self.current_music_path = None
        self.dragging_bgm_slider = False
        self.dragging_sfx_slider = False

    def reset_game(self) -> None:
        """
        Resets the game to the initial state
        
        :return:
        """
        # does python run auto garbage collection so it's OK to just
        # assign a new gw?
        self.gw = GameWorld(Levels.LevelName.SMASHCORE_1)
        self.fps = INITIAL_FPS_SIMPLE
        self.gs.cur_state = GameState.GameStateName.READY_TO_LAUNCH
        self.gs.cur_ball_x = (WIDTH // 2) - (PAD_WIDTH // 2)
        self.ps.lives = START_LIVES
        self.ps.score = START_SCORE
        self.ps.level = 1
        pygame.mouse.set_visible(False)  # Hide the cursor when game restarts
        pygame.mixer.music.stop()
        self.current_music_path = None

    def next_level(self) -> None:
        """
        Builds the next level, resets the ball position and initial speed
        Slight increase in initial ball speed to add difficulty
        
        :return:
        """
        self.gw.remove_obstacles()
        self.gw.remove_bricks()

        for wo in self.gw.world_objects:
            if isinstance(wo, Ball):
                wo.reset_position()
                wo.speed_v = BALL_SPEED_VECTOR + (self.ps.level * BALL_SPEED_LEVEL_INCREMENT)
                self.gs.ball_speed_increased_ratio = wo.speed_v / BALL_SPEED_VECTOR
                wo.v_vel = wo.v_vel_unit * wo.speed_v
                wo.speed = BALL_SPEED_SIMPLE + (self.ps.level * BALL_SPEED_LEVEL_INCREMENT)
        # builds the next level
        next_level = Levels.get_level_name_from_num(self.ps.level)
        Levels.build_level(self.gw.world_objects, next_level)

        self.fps = INITIAL_FPS_SIMPLE
        self.gs.cur_state = GameState.GameStateName.READY_TO_LAUNCH

    def draw_world_and_status(self) -> None:
        """
        Draw all objects in GameWorld plus status overlays
        
        :return:
        """
        # draw every game object
        for world_object in self.gw.world_objects:
            world_object.draw_wo(self.screen)
        # draw any status overlays
        self.ui.draw_status(self.ps.lives, self.ps.score, self.ps.level)

    def clean_shutdown(self) -> None:
        pygame.mixer.music.stop()
        self.current_music_path = None
        self.gs.running = False
        self.gs.cur_state = GameState.GameStateName.GAME_OVER

        # store leaderboard
        self.lb.store(persistence.LEADERBOARD_FILENAME)

        pygame.quit()
        exit()

    def play_music(self, gs: GameState):
        """
        Plays the music file for each game state
        
        :return:
        """
        if not self.gs.bgm_sounds:
            pygame.mixer.music.stop()
            self.current_music_path = None
            return

        target_music_path: str = ""
        loop: int = -1  # Default to loop infinitely

        if gs.cur_state in assets.MUSIC_PATHS:
            target_music_path = assets.MUSIC_PATHS[gs.cur_state]
            if ((gs.cur_state == GameState.GameStateName.SPLASH) or
                    (gs.cur_state == GameState.GameStateName.GET_HIGH_SCORE) or
                    (gs.cur_state == GameState.GameStateName.GAME_OVER)):
                loop = 0  # Play only once

        if target_music_path and self.current_music_path != target_music_path:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(target_music_path)
            pygame.mixer.music.set_volume(self.gs.music_volume)
            pygame.mixer.music.play(loop)
            self.current_music_path = target_music_path
        elif not target_music_path and self.current_music_path is not None:
            pygame.mixer.music.stop()
            self.current_music_path = None

    def run_loop(self) -> None:
        """
        Runs the main game loop

        :return:
        """

        while self.gs.running:
            # fill the screen with black as a good default
            self.screen.fill(BLACK)

            self.play_music(self.gs)

            # get all events from queue for handling
            events = pygame.event.get()

            match self.gs.cur_state:

                ##############################################################
                # display the SPLASH screen
                ##############################################################
                case GameState.GameStateName.SPLASH:
                    # placeholder for the splash screen graphic
                    self.ui.draw_splash_screen()

                    # go beyond the splash GameState after desired time
                    cur_ticks = pygame.time.get_ticks()
                    if ((cur_ticks - self.app_start_ticks) / 1000) > SPLASH_TIME_SECS:
                        self.gs.cur_state = GameState.GameStateName.MENU_SCREEN

                ##############################################################
                # display the MENU SCREEN
                ##############################################################
                case GameState.GameStateName.MENU_SCREEN:
                    self.ui.draw_start_screen()
                    pygame.mouse.set_visible(True)
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.ui.start_button_rect.collidepoint(event.pos):
                                self.reset_game()
                                self.gs.cur_state = GameState.GameStateName.READY_TO_LAUNCH
                            elif self.ui.credits_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameState.GameStateName.CREDITS
                            elif self.ui.settings_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameState.GameStateName.SETTINGS
                            elif self.ui.leader_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameState.GameStateName.LEADERBOARD
                            elif self.ui.how_to_play_button_rect and self.ui.how_to_play_button_rect.collidepoint(
                                    event.pos):
                                self.gs.cur_state = GameState.GameStateName.HOW_TO_PLAY
                            elif self.ui.quit_button_start_rect.collidepoint(event.pos):
                                self.clean_shutdown()

                ##############################################################
                # display how to play screen
                ##############################################################
                case GameState.GameStateName.HOW_TO_PLAY:
                    self.ui.draw_how_to_play_screen()
                    pygame.mouse.set_visible(True)
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if hasattr(self.ui,
                                       'back_button_rect') and self.ui.back_button_rect.collidepoint(
                                event.pos):
                                self.gs.cur_state = GameState.GameStateName.MENU_SCREEN

                ##############################################################
                # display credits screen
                ##############################################################
                case GameState.GameStateName.CREDITS:
                    self.ui.draw_credits_screen()
                    pygame.mouse.set_visible(True)
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.ui.back_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameState.GameStateName.MENU_SCREEN

                ##############################################################
                # display leaderboard screen
                ##############################################################
                case GameState.GameStateName.LEADERBOARD:
                    self.ui.draw_leaderboard_screen(self.lb)
                    pygame.mouse.set_visible(True)
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.ui.back_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameState.GameStateName.MENU_SCREEN

                ##############################################################
                # display settings screen
                ##############################################################
                case GameState.GameStateName.SETTINGS:
                    self.ui.draw_settings_screen(self.gs.bgm_sounds, self.gs.sfx_sounds,
                                                 self.gs.paddle_under_mouse_control, self.gs.music_volume,
                                                 self.gs.sfx_volume)
                    pygame.mouse.set_visible(True)

                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.ui.volume_bgbutton_rect.collidepoint(event.pos):
                                self.gs.bgm_sounds = not self.gs.bgm_sounds
                                if not self.gs.bgm_sounds and self.gs.music_volume <= 0:
                                    self.gs.bgm_sounds = True
                                    self.gs.music_volume = 0.2
                                    pygame.mixer.music.set_volume(self.gs.music_volume)
                            elif self.ui.volume_sfbutton_rect.collidepoint(event.pos):
                                self.gs.sfx_sounds = not self.gs.sfx_sounds
                                if not self.gs.sfx_sounds and self.gs.sfx_volume <= 0:
                                    self.gs.sfx_sounds = True
                                    self.gs.sfx_volume = 0.2
                                    pygame.mixer.music.set_volume(self.gs.sfx_volume)
                            elif self.ui.back_button_rect.collidepoint(event.pos):
                                self.gs.cur_state = GameState.GameStateName.MENU_SCREEN
                            elif self.ui.knob_bg_rect.collidepoint(event.pos):
                                self.dragging_bgm_slider = True
                            elif self.ui.knob_sf_rect.collidepoint(event.pos):
                                self.dragging_sfx_slider = True
                            elif self.ui.pad_btn_rect.collidepoint(event.pos):
                                self.gs.paddle_under_mouse_control = not self.gs.paddle_under_mouse_control
                        elif event.type == pygame.MOUSEMOTION:
                            if self.dragging_bgm_slider:
                                slider_bg_x = self.ui.volume_bgbutton_rect.centerx + 75
                                new_vol = (event.pos[0] - (slider_bg_x - KNOB_RADIUS)) / SLIDER_WIDTH
                                self.gs.music_volume = max(0.0, min(1.0, round(
                                    new_vol / MUSIC_VOLUME_STEP) * MUSIC_VOLUME_STEP))
                                pygame.mixer.music.set_volume(self.gs.music_volume)
                            if self.dragging_sfx_slider:
                                slider_sf_x = self.ui.volume_sfbutton_rect.centerx + 75
                                new_vol = (event.pos[0] - (slider_sf_x - KNOB_RADIUS)) / SLIDER_WIDTH
                                self.gs.sfx_volume = max(0.0, min(1.0, round(
                                    new_vol / MUSIC_VOLUME_STEP) * MUSIC_VOLUME_STEP))
                        elif event.type == pygame.MOUSEBUTTONUP:
                            self.dragging_bgm_slider = False
                            self.dragging_sfx_slider = False

                ##############################################################
                # display the PLAYING gameplay screen
                ##############################################################
                case GameState.GameStateName.PLAYING | GameState.GameStateName.READY_TO_LAUNCH:
                    # Hide the mouse again when transitioning away from the start screen.
                    pygame.mouse.set_visible(False)
                    # update all objects in GameWorld

                    mouse_pos = pygame.mouse.get_pos()
                    self.gs.last_mouse_pos_x = mouse_pos[0]

                    for current_wo in self.gw.world_objects:

                        if isinstance(current_wo, Paddle):
                            # this controls whether the AutoPlay system or the
                            # player's mouse input is driving the paddle
                            if self.gs.auto_play:
                                current_wo.commanded_pos_x = self.gs.cur_ball_x
                            elif self.gs.paddle_under_mouse_control:
                                current_wo.commanded_pos_x = mouse_pos[0]

                        if isinstance(current_wo, Ball) and GameState.GameStateName.READY_TO_LAUNCH:
                            current_wo.commanded_pos_x = self.gs.paddle_pos_x

                        # generic WorldObject update()
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
                                            if other_wo.should_score():
                                                self.ps.score += other_wo.value
                                            if other_wo.should_remove():
                                                self.ps.score += other_wo.bonus
                                                # special effect
                                                #  TODO probably need to store this brick rect and set
                                                #  it to be displayed for some duration because we sometimes don't see
                                                #  the inflation effect, likely because it's removed before being drawn
                                                other_wo.animate(self.screen)
                                                pygame.display.update(other_wo.rect)
                                                other_wo.destruction(self.gw.world_objects)
                                                #other_wo.rect.inflate_ip(current_wo.rect.width * 3,
                                                #                         current_wo.rect.height * 3)
                                                #pygame.draw.rect(self.screen, other_wo.color, other_wo.rect)
                                                current_wo.speed += .20
                                                # BALL_SPEED_STEP: adding to the ball speed, but diff logic for the
                                                # VECTOR models
                                                if isinstance(current_wo, Ball):
                                                    current_wo.speed_v += self.gs.ball_speed_step
                                                    self.gs.ball_speed_increased_ratio = current_wo.speed_v / BALL_SPEED_VECTOR
                                                    current_wo.v_vel = current_wo.v_vel_unit * current_wo.speed_v
                                                #self.gw.world_objects.remove(other_wo)

                                    else:
                                        # this is the other side of the allow_collision logic above, since
                                        # not colliding now, it resets the latch or 'primed for collision' flag
                                        other_wo.prime_for_collision()

                    # draw all objects in GameWorld
                    self.draw_world_and_status()

                    # note this is the way the player enters the gameplay
                    # screen, in a pending, ready to launch mode, with the
                    # ball stuck to the paddle
                    if self.gs.cur_state == GameState.GameStateName.READY_TO_LAUNCH:
                        self.ui.draw_game_intro()

                    if not any(isinstance(wo, Brick) for wo in self.gw.world_objects):
                        self.ps.level += 1
                        self.next_level()

                ##############################################################
                # display the PAUSED popup over the frozen gameplay
                ##############################################################
                case GameState.GameStateName.PAUSED:
                    # draw all objects in GameWorld
                    self.draw_world_and_status()
                    # getting the rects for the UI buttons for later collision
                    # detection (button pressing)
                    self.restart_game_button, self.main_menu_button, self.quit_game_button = self.ui.draw_pause_menu(
                                                                                    self.gs.paddle_under_mouse_control)
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if self.ui.pad_btn_rect.collidepoint(event.pos):
                                self.gs.paddle_under_mouse_control = not self.gs.paddle_under_mouse_control

                ##############################################################
                # display the GET_HIGH_SCORE popup over the frozen gameplay
                ##############################################################
                case GameState.GameStateName.GET_HIGH_SCORE:
                    # draw all objects in GameWorld
                    self.draw_world_and_status()
                    # getting the rects for the UI buttons for later collision
                    # detection (button pressing)
                    self.high_score_enter_btn = self.ui.draw_get_high_score()

                ##############################################################
                # display the GAME_OVER popup over the frozen gameplay
                ##############################################################
                case GameState.GameStateName.GAME_OVER:
                    # draw all objects in GameWorld
                    self.draw_world_and_status()
                    # getting the rects for the UI buttons for later collision
                    # detection (button pressing)
                    self.restart_game_button, self.main_menu_button, self.quit_game_button = self.ui.draw_game_over_menu()

            ##############################################################
            # event handling
            ##############################################################

            for event in events:
                if event.type == pygame.QUIT:
                    self.clean_shutdown()

                if event.type == pygame.KEYDOWN:
                    # toggle PAUSE GameState with ESCAPE key press
                    if event.key == pygame.K_ESCAPE:
                        if (self.gs.cur_state == GameState.GameStateName.PLAYING or
                                self.gs.cur_state == GameState.GameStateName.READY_TO_LAUNCH):
                            self.prev_state = self.gs.cur_state
                            self.gs.cur_state = GameState.GameStateName.PAUSED
                            self.mouse_pos = pygame.mouse.get_pos()
                            pygame.mouse.set_visible(True)
                        elif self.gs.cur_state == GameState.GameStateName.PAUSED:
                            self.gs.cur_state = self.prev_state
                            pygame.mouse.set_pos(self.mouse_pos)
                            pygame.mouse.set_visible(False)

                    if event.key == pygame.K_SPACE:
                        if self.gs.cur_state == GameState.GameStateName.READY_TO_LAUNCH:
                            self.gs.cur_state = GameState.GameStateName.PLAYING

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

                    # detect the CTRL+'=' and CTRL+'-' key combos to adjust music volume
                    if event.key == pygame.K_EQUALS:
                        if event.mod & pygame.KMOD_CTRL:
                            self.gs.bgm_sounds = True
                            self.gs.music_volume += MUSIC_VOLUME_STEP
                            self.gs.music_volume = min(self.gs.music_volume, 1.0)
                            pygame.mixer.music.set_volume(self.gs.music_volume)

                    # detect the CTRL+'+' and CTRL+'-' key combos to adjust music volume
                    if event.key == pygame.K_MINUS:
                        if event.mod & pygame.KMOD_CTRL:
                            self.gs.music_volume -= MUSIC_VOLUME_STEP
                            self.gs.music_volume = max(self.gs.music_volume, 0.0)
                            if self.gs.music_volume < 0.01:
                                self.gs.bgm_sounds = False
                            pygame.mixer.music.set_volume(self.gs.music_volume)

                    # detect the CTRL+l to force-load next level in sequence
                    if event.key == pygame.K_l:
                        if event.mod & pygame.KMOD_CTRL:
                            self.ps.level += 1
                            self.next_level()

                    # handle initials textbox input
                    if self.gs.cur_state == GameState.GameStateName.GET_HIGH_SCORE:
                        if (event.key == pygame.K_RETURN) or (event.key == pygame.K_KP_ENTER):
                            self.lb.add_score(self.ps, self.ui)
                            self.gs.cur_state = GameState.GameStateName.GAME_OVER
                        elif event.key == pygame.K_BACKSPACE:
                            self.ui.tb_initials_text = self.ui.tb_initials_text[:-1]
                        elif len(self.ui.tb_initials_text) < SCORE_INITIALS_MAX:
                            self.ui.tb_initials_text += event.unicode

                # the actual button press checks from the returned rects above
                if (event.type == pygame.MOUSEBUTTONDOWN and
                        ((self.gs.cur_state == GameState.GameStateName.PAUSED) or
                         (self.gs.cur_state == GameState.GameStateName.GAME_OVER))):
                    if self.restart_game_button and self.restart_game_button.collidepoint(event.pos):
                        self.reset_game()
                    if self.quit_game_button and self.quit_game_button.collidepoint(event.pos):
                        self.clean_shutdown()
                    if self.main_menu_button and self.main_menu_button.collidepoint(event.pos):
                        self.gs.cur_state = GameState.GameStateName.MENU_SCREEN

                if (event.type == pygame.MOUSEBUTTONDOWN and
                        (self.gs.cur_state == GameState.GameStateName.GET_HIGH_SCORE)):
                    if self.high_score_enter_btn.collidepoint(event.pos):
                        self.lb.add_score(self.ps, self.ui)
                        self.gs.cur_state = GameState.GameStateName.GAME_OVER

            # get the continuously pressed keys, rather than single key press events
            pressed_keys = pygame.key.get_pressed()
            if not self.gs.paddle_under_mouse_control:
                if pressed_keys[pygame.K_LEFT]:
                    self.gs.paddle_under_key_control_left = True
                elif pressed_keys[pygame.K_RIGHT]:
                    self.gs.paddle_under_key_control_right = True

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
                self.gs.fps_avg, self.gs.loop_time_avg = utils.calculate_timing_averages(self.clock.get_fps(),
                                                                                         self.clock.get_time())

        ##############################################################
        # close down cleanly
        ##############################################################
        pygame.quit()
