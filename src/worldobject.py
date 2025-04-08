"""
    Project: SmashCore
    Course: UMGC CMSC 495 (7383)
    Term: Spring 2025
    Date: 20250401
    Code Repository: https://github.com/jcooke-dev/smashCore
    Authors: Justin Cooke, Ann Rauscher, Camila Roxo, Justin Smith, Rex Vargas

    Module Description: This is meant to be a useful parent type class for all objects in the
                        GameWorld, although there isn't much commonality between the types.
"""

class WorldObject:

    def __init__(self):

        self.can_react = False # can this object react to collisions with other objects?
        self.primed_collision = True

    # update the WorldObject's pos, vel, acc, etc. (and possibly GameState)
    def update_wo(self, gs, ps):
        pass

    # draw the WorldObject to the screen
    def draw_wo(self, screen):
        pass

    # Function to detect collisions
    def detect_collision(self, hitbox, gs):
        pass

    # record that something collided with this WorldObject
    def add_collision(self):
        pass

    # inform caller that this WorldObject should be removed from the GameWorld
    def should_remove(self):
        return False

    # determines if this object can participate in a collision
    def allow_collision(self):
        if self.primed_collision:
            self.primed_collision = False
            return True
        else:
            return False

    # reset the latch to allow for future collisions
    def prime_for_collision(self):
        self.primed_collision = True