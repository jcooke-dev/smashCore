"""
    SmashCore is a breakout style game
"""

import pygame

import assets
from src.gamestate import GameState
from src.playerstate import PlayerState
from src.userinterface import UserInterface
from src.gameworld import GameWorld
from src.gameengine import GameEngine


pygame.init()

# setup various game objects


if __name__ == "__main__":
    assets.load_assets()
    ui = UserInterface()
    gs = GameState()
    gw = GameWorld()
    ps = PlayerState()
    ge = GameEngine(ps, gw, gs, ui)

    # run the main game loop -- this returns when done
    ge.run_loop()
