"""
    This brings together the various modules that make up the game (GameWorld, GameState, UI, etc.) and runs
    the main game loop.
"""

import pygame

import constants
from src.levels import Levels
from src.gameworld import GameWorld


class GameEngine:


    def __init__(self, gw, gs, ui):

        self.gw = gw
        self.gs = gs
        self.ui = ui

        ui.screen = self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        ui.surface = self.surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.fps = constants.INITIAL_FPS

        pygame.display.set_caption(constants.GAME_NAME)

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    # reset game to initial state
    def reset_game(self):

        # does python run auto garbage collection so it's OK to just assign a new gw?
        self.gw = GameWorld(Levels.LevelName.SMASHCORE_1)
        self.fps = constants.INITIAL_FPS
        self.gs.game_over = False
        pygame.mouse.set_visible(False)  # Hide the cursor when game restarts

    # this runs the main game loop
    def run_loop(self):

        while self.gs.running:

            # fill the screen with black.
            self.screen.fill(constants.BLACK)

            if not self.gs.pause and not self.gs.game_over:
                # update all objects in GameWorld
                mouse_pos = pygame.mouse.get_pos()
                for world_object in self.gw.world_objects:
                    world_object.mouse_position = mouse_pos[0]
                    world_object.update_wo(self.gs)
                    # test for collisions between world_objects, but ignore objects that can't be affected (for performance)
                    if world_object.can_react:
                        for wo in self.gw.world_objects:
                            # don't check for collisions with self
                            if world_object is not wo:
                                if world_object.rect.colliderect(wo.rect): # and self.dy > 0:
                                    # bounce object properly
                                    world_object.detect_collision(wo.rect)
                                    wo.add_collision()
                                    if wo.should_remove():
                                        # special effect
                                        wo.rect.inflate_ip(world_object.rect.width * 3, world_object.rect.height * 3)
                                        pygame.draw.rect(self.screen, wo.color, wo.rect)
                                        self.fps += 2
                                        self.gw.world_objects.remove(wo)

            # draw all objects in GameWorld
            for world_object in self.gw.world_objects:
                world_object.draw_wo(self.screen)

            # getting the rects for the UI buttons for later collision detection (button pressing)
            if self.gs.game_over:
                self.restart_game, self.quit_game = self.ui.draw_game_over_menu()

            if self.gs.pause:
                self.restart_game, self.quit_game = self.ui.draw_pause_menu()


            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gs.running = False
                    self.gs.game_over = True
                    exit()

                if event.type == pygame.KEYDOWN:
                    # toggle PAUSE GameState with ESCAPE key press
                    if event.key == pygame.K_ESCAPE:
                        if self.gs.pause:
                            self.gs.pause = False
                            pygame.mouse.set_pos(self.mouse_pos)
                            pygame.mouse.set_visible(False)
                        else:
                            self.gs.pause = True
                            self.mouse_pos = pygame.mouse.get_pos()
                            pygame.mouse.set_visible(True)

                # the actual button press checks from the returned rects above
                if event.type == pygame.MOUSEBUTTONDOWN and (self.gs.pause or self.gs.game_over):
                    if self.restart_game.collidepoint(event.pos):
                        self.reset_game()
                        self.gs.pause = False
                    if self.quit_game.collidepoint(event.pos):
                        self.gs.running = False
                        self.gs.game_over = True
                        exit()


            # update screen
            pygame.display.flip()
            self.clock.tick(self.fps)

        # close down cleanly
        pygame.quit()