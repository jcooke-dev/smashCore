"""
    This brings together the various modules that make up the game (GameWorld,
    GameState, UI, etc.) and runs the main game loop.
"""

import pygame
from constants import *
from src.levels import Levels
from src.gameworld import GameWorld
from gamestates import GameStates


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
        self.fps = INITIAL_FPS
        self.score = 0

        # record the app start ticks to time the splash screen display
        self.app_start_ticks = pygame.time.get_ticks()

        pygame.display.set_caption(constants.GAME_NAME)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    # reset game to initial state
    def reset_game(self):

        # does python run auto garbage collection so it's OK to just assign a new gw?
        self.gw = GameWorld(Levels.LevelName.SMASHCORE_1)
        self.fps = constants.INITIAL_FPS
        self.gs.cur_state = GameStates.SPLASH
        self.ps.lives = constants.START_LIVES
        pygame.mouse.set_visible(False)  # Hide the cursor when game restarts

    # draw all objects in GameWorld plus status overlays
    def drawWorldAndStatus(self):
        # draw every game object
        for world_object in self.gw.world_objects:
            world_object.draw_wo(self.screen)
        # draw any status overlays
        self.ui.draw_lives(self.ps.lives)
        self.ui.draw_score(self.score)


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
                    for world_object in self.gw.world_objects:
                        world_object.mouse_position = mouse_pos[0]
                        world_object.update_wo(self.gs, self.ps)
                        # test for collisions between world_objects, but ignore objects that can't be affected (for performance)
                        if world_object.can_react:
                            for wo in self.gw.world_objects:
                                # don't check for collisions with self
                                if world_object is not wo:
                                    if world_object.rect.colliderect(wo.rect):  # and self.dy > 0:
                                        # bounce object properly
                                        world_object.detect_collision(wo.rect)
                                        wo.add_collision()
                                        if wo.should_remove():
                                            self.score += wo.value
                                            # special effect
                                            wo.rect.inflate_ip(world_object.rect.width * 3,
                                                               world_object.rect.height * 3)
                                            pygame.draw.rect(self.screen, wo.color, wo.rect)
                                            self.fps += 2
                                            self.gw.world_objects.remove(wo)

                    # draw all objects in GameWorld
                    self.drawWorldAndStatus()

                    # note this is the way the player enters the gameplay screen, in a pending, ready
                    # to launch mode, with the ball stuck to the paddle
                    if self.gs.cur_state == GameStates.READY_TO_LAUNCH:
                        self.ui.draw_game_intro()

                ##############################################################
                # display the PAUSED popup over the frozen gameplay
                ##############################################################
                case GameStates.PAUSED:
                    # draw all objects in GameWorld
                    self.drawWorldAndStatus()
                    # getting the rects for the UI buttons for later collision detection (button pressing)
                    self.restart_game, self.quit_game = self.ui.draw_pause_menu()

                ##############################################################
                # display the GAME_OVER popup over the frozen gameplay
                ##############################################################
                case GameStates.GAME_OVER:
                    # draw all objects in GameWorld
                    self.drawWorldAndStatus()
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

                # the actual button press checks from the returned rects above
                if (event.type == pygame.MOUSEBUTTONDOWN and
                        ((self.gs.cur_state == GameStates.PAUSED) or (self.gs.cur_state == GameStates.GAME_OVER))):
                    if self.restart_game.collidepoint(event.pos):
                        self.reset_game()

                    if self.quit_game.collidepoint(event.pos):
                        self.gs.running = False
                        self.gs.cur_state = GameStates.GAME_OVER
                        exit()

            ##############################################################
            # update screen
            ##############################################################
            pygame.display.flip()
            self.clock.tick(self.fps)

        ##############################################################
        # close down cleanly
        ##############################################################
        pygame.quit()