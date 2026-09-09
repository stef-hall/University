from warehouse_env import UP, DOWN, LEFT, RIGHT, PICKUP, DISPATCH

def manhattan_distance(pos_a, pos_b):
    """Manhattan (grid) distance between two (row, col) positions."""
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


def find_closest(pos, options):
    least_distance = float("inf")
    goal = pos
    for option in options:
        distance = manhattan_distance(pos, option)
        if distance < least_distance:
            least_distance = distance
            goal = option

    return goal, least_distance


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



#────────── My Greedy Agent ──────────────────────────────────
def greedy_agent(state):
    pos = state["position"]
    if state["carrying"] == False:
        goal, distance = find_closest(pos, state["packages"])
        if distance == 0:
            return PICKUP
        else:
            return _direction_toward(pos, goal)
                
    else:
        goal, distance = find_closest(pos, state["dispatch_stations"])
        if distance == 0:
            return DISPATCH
        else:
            return _direction_toward(pos, goal)


