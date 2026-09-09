"""
agents.py  ─  PROVIDED TO STUDENTS (do not modify)

Contains RandomAgent (a ready-to-use baseline opponent) plus two small
utility functions you may find useful when implementing your own agents
in later tasks.

Every agent is a plain function:  state (dict)  ->  action (int 0-5)
"""

import random
from warehouse_env import UP, DOWN, LEFT, RIGHT, PICKUP, DISPATCH


def manhattan_distance(pos_a, pos_b):
    """Manhattan (grid) distance between two (row, col) positions."""
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


def _direction_toward(current, target):
    """
    Return the movement action (UP/DOWN/LEFT/RIGHT) that takes one step
    from `current` toward `target`, breaking ties by moving vertically first.

    Returns None if current == target (nothing to move toward).
    """
    dr = target[0] - current[0]
    dc = target[1] - current[1]

    if dr == 0 and dc == 0:
        return None  # already there

    if abs(dr) >= abs(dc):
        return DOWN if dr > 0 else UP
    else:
        return RIGHT if dc > 0 else LEFT


# ── RandomAgent ──────────────────────────────────────────────────────────────

def random_agent(state):
    """
    Ignores the state entirely and returns a uniformly random action
    from the 6 available choices. Use this as your Task 1 baseline
    opponent for GreedyAgent.
    """
    return random.randint(0, 5)
