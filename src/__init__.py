"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is the entry point for SmashCore, a breakout style game.
"""

import pygame

import assets
from leaderboard import Leaderboard
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
    lb = Leaderboard.create_persisted_object()

    ge = GameEngine(lb, ps, gw, gs, ui)

    # run the main game loop -- this returns when done
    ge.run_loop()
