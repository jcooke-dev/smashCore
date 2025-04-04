"""
    SmashCore is a breakout style game
"""

import pygame

from src.gamestate import GameState
from src.playerstate import PlayerState
from src.userinterface import UserInterface
from src.gameworld import GameWorld
from src.gameengine import GameEngine


pygame.init()

# setup various game objects
ui = UserInterface()
gs = GameState()
gw = GameWorld()
ps = PlayerState()
ge = GameEngine(ps, gw, gs, ui)

if __name__ == "__main__":
    # run the main game loop -- this returns when done
    ge.run_loop()
