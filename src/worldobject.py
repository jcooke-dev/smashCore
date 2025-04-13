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
    """ This is a parent class for the specific world objects (Ball, Paddle, Bricks) """

    def __init__(self):

        self.can_react = False # can this object react to collisions with other objects?
        self.primed_collision = True

    def update_wo(self, gs, ps, lb):
        """
        Update the WorldObject's pos, vel, acc, etc. (and possibly GameState)

        :param lb:
        :param gs:
        :param ps:
        :return:
        """
        pass

    def draw_wo(self, screen):
        """
        Draw the WorldObject to the screen

        :param screen:
        :return:
        """
        pass

    def detect_collision(self, hitbox, gs):
        """
        Function to detect collisions

        :param hitbox: the other Rect in the collision detection check
        :param gs: GameState
        :return:
        """
        pass

    def add_collision(self):
        """
        Record that something collided with this WorldObject

        :return:
        """
        pass

    def should_remove(self):
        """
        Inform caller that this WorldObject should be removed from the GameWorld

        :return:
        """
        return False

    def allow_collision(self):
        """
        Determines if this object can participate in a collision

        :return:
        """
        if self.primed_collision:
            self.primed_collision = False
            return True
        else:
            return False

    def prime_for_collision(self):
        """
        Reset the latch to allow for future collisions

        :return:
        """
        self.primed_collision = True