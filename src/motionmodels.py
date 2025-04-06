
from enum import Enum, auto


class MotionModels(Enum):

    # initial motion code with simplified calculations and clock.tick(fps) to time the update loop
    SIMPLE_1 = auto()

    # motion calculations using POS/VEL/ACC vectors and the clock.tick() returned delta time, so the motion is unlinked
    # from the frame rate - can set a MAX_FPS_VECTOR to limit the fps a bit (rather than letting it run all out)
    VECTOR_1 = auto()

