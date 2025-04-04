"""
    This brings together the various modules that make up the game (GameWorld,
    GameState, UI, etc.) and runs the main game loop.
"""

import pygame

import src.ball
from src import constants
from constants import *
from src.levels import Levels
from src.gameworld import GameWorld
from gamestates import GameStates
from motionmodels import MotionModels

import utils


class GameEngine:

    def __init__(self, ps, gw, gs, ui):
        self.mouse_pos = None
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

        pygame.display.set_caption(constants.GAME_NAME)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    # reset game to initial state
    def reset_game(self):

        # does python run auto garbage collection so it's OK to just assign a new gw?
        self.gw = GameWorld(Levels.LevelName.SMASHCORE_1)
        self.fps = constants.INITIAL_FPS_SIMPLE
        self.gs.cur_state = GameStates.SPLASH
        self.ps.lives = constants.START_LIVES
        self.ps.score = 0
        pygame.mouse.set_visible(False)  # Hide the cursor when game restarts

    # draw all objects in GameWorld plus status overlays
    def draw_world_and_status(self):
        # draw every game object
        for world_object in self.gw.world_objects:
            world_object.draw_wo(self.screen)
        # draw any status overlays
        self.ui.draw_lives(self.ps.lives)
        self.ui.draw_score(self.ps.score)

    # this runs the main game loop
    def run_loop(self):

        while self.gs.running:
            # fill the screen with black as a good default
            self.screen.fill(constants.BLACK)

            match self.gs.cur_state:

                ##############################################################
                # display the SPLASH screen
                ##############################################################
                case GameStates.SPLASH:
                    # placeholder for the splash screen graphic
                    self.screen.fill(constants.YELLOW)

                    # go beyond the splash GameState after desired time
                    cur_ticks = pygame.time.get_ticks()
                    if ((cur_ticks - self.app_start_ticks) / 1000) > constants.SPLASH_TIME_SECS:
                        self.gs.cur_state = GameStates.READY_TO_LAUNCH

                ##############################################################
                # display the PLAYING gameplay screen
                ##############################################################
                case GameStates.PLAYING | GameStates.READY_TO_LAUNCH:
                    # update all objects in GameWorld
                    mouse_pos = pygame.mouse.get_pos()
                    for current_wo in self.gw.world_objects:
                        current_wo.mouse_position = mouse_pos[0]
                        current_wo.update_wo(self.gs, self.ps)
                        # test for collisions between world_objects, but ignore objects that
                        # can't be affected (for performance)
                        if not current_wo.can_react:
                            continue

                        for other_wo in self.gw.world_objects:
                            inflate_factor = 3
                            # skips loop for collision checks with self
                            # skips loop if current_wo does not collide with other_wo.
                            if current_wo is other_wo or not current_wo.rect.colliderect(other_wo.rect):
                                continue
                            # checks if the collision should not be reacted to. if yes,
                            # resets the latch or 'primed for collision' flag
                            # prevents the current_wo from being trapped by preventing unnecessary collisions
                            if not other_wo.allow_collision():
                                other_wo.prime_for_collision()
                            # bounce object properly - determining in which direction to bounce, based on approach
                            current_wo.detect_collision(other_wo, self.gs)
                            other_wo.add_collision()

                            if not other_wo.should_remove():
                                continue
                            # adding to the ball speed, but diff logic for the VECTOR models
                            if isinstance(current_wo, src.ball.Ball):
                                current_wo.speedV += BALL_SPEED_INCREMENT_VECTOR
                                current_wo.vVel = current_wo.vVelUnit * current_wo.speedV

                                self.ps.score += other_wo.value
                                # special effect
                                # TODO probably need to store this brick rect and set it to be displayed
                                # for some duration because we sometimes don't see the inflation effect, likely
                                # because it's removed before being drawn
                                other_wo.rect.inflate_ip(current_wo.rect.width * inflate_factor,
                                                         current_wo.rect.height * inflate_factor)
                                pygame.draw.rect(self.screen, other_wo.color, other_wo.rect)
                                current_wo.speed += .20
                                self.gw.world_objects.remove(other_wo)

                    # draw all objects in GameWorld
                    self.draw_world_and_status()

                    # note this is the way the player enters the gameplay screen, in a pending, ready
                    # to launch mode, with the ball stuck to the paddle
                    if self.gs.cur_state == GameStates.READY_TO_LAUNCH:
                        self.ui.draw_game_intro()

                ##############################################################
                # display the PAUSED popup over the frozen gameplay
                ##############################################################
                case GameStates.PAUSED:
                    # draw all objects in GameWorld
                    self.draw_world_and_status()
                    # getting the rects for the UI buttons for later collision detection (button pressing)
                    self.restart_game, self.quit_game = self.ui.draw_pause_menu()

                ##############################################################
                # display the GAME_OVER popup over the frozen gameplay
                ##############################################################
                case GameStates.GAME_OVER:
                    # draw all objects in GameWorld
                    self.draw_world_and_status()
                    # getting the rects for the UI buttons for later collision detection (button pressing)
                    self.restart_game, self.quit_game = self.ui.draw_game_over_menu()

            ##############################################################
            # event handling
            ##############################################################
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gs.running = False
                    self.gs.cur_state = GameStates.GAME_OVER
                    exit()

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

                    # detect the CTRL+d key combo to toggle the dev overlay calculation and display
                    if event.key == pygame.K_d:
                        if event.mod & pygame.KMOD_CTRL:
                            self.gs.show_dev_overlay = not self.gs.show_dev_overlay

                    # detect the CTRL+m key combo to cycle through the various motion models
                    if event.key == pygame.K_m:
                        if event.mod & pygame.KMOD_CTRL:
                            match self.gs.motion_model:
                                case MotionModels.SIMPLE_1:
                                    self.gs.motion_model = MotionModels.VECTOR_1
                                case MotionModels.VECTOR_1:
                                    self.gs.motion_model = MotionModels.VECTOR_2
                                case MotionModels.VECTOR_2:
                                    self.gs.motion_model = MotionModels.SIMPLE_1

                # the actual button press checks from the returned rects above
                if (event.type == pygame.MOUSEBUTTONDOWN and
                        ((self.gs.cur_state == GameStates.PAUSED) or (self.gs.cur_state == GameStates.GAME_OVER))):
                    if self.restart_game.collidepoint(event.pos):
                        self.reset_game()

                    if self.quit_game.collidepoint(event.pos):
                        self.gs.running = False
                        self.gs.cur_state = GameStates.GAME_OVER
                        exit()

            # draw the developer overlay, if requested
            if self.gs.show_dev_overlay:
                self.ui.draw_dev_overlay(self.gs.fps_avg, self.gs.loop_time_avg, self.gs.motion_model)

            ##############################################################
            # update screen
            ##############################################################
            pygame.display.flip()

            # choose from the available motion models; note that SIMPLE models use clock.tick(fps) to force the
            # motion update logic to the frame rate - VECTOR models decouple the frame rate from the dT motion logic
            if self.gs.motion_model == MotionModels.SIMPLE_1:
                self.gs.tick_time = self.clock.tick(self.fps)
            elif (self.gs.motion_model == MotionModels.VECTOR_1) or (self.gs.motion_model == MotionModels.VECTOR_2):
                # removing the fps arg (rather, setting it to 0) allows pygame to run this loop at full speed
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
