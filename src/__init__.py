"""
    SmashCore is a breakout style game
"""

import pygame

from src.gamestate import GameState
from src.userinterface import UserInterface
from src.gameworld import GameWorld
from src.gameengine import GameEngine


pygame.init()

# setup various game objects
ui = UserInterface()
gs = GameState()
gw = GameWorld()
ge = GameEngine(gw, gs, ui)

# run the main game loop -- this returns when done
ge.run_loop()

