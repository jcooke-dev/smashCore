"""
    This utils.py provides a kind of global/singleton module (not a class) that should
    be available to any other module that imports it.  This can be helpful in situations
    such as this where we want to maintain some global data and useful functions on that, but
    without actually creating and passing around objects.
"""


import collections
import statistics


# these are queues used to store the shifting window of recorded values for the dev overlay
fps_q = collections.deque(maxlen=60)
loop_time_q = collections.deque(maxlen=60)

# this just fills the queues, shifting the oldest values out as newer ones are added, and
# calculates the running averages for display
def calculate_timing_averages(fps, loop_time):
    fps_q.appendleft(fps)
    loop_time_q.appendleft(loop_time)
    return statistics.mean(fps_q), statistics.mean(loop_time_q)


