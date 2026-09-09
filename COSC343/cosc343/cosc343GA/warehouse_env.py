"""
warehouse_env.py

10x10 grid warehouse environment for multi-robot package delivery.

Actions (6 discrete choices):
    0: UP
    1: DOWN
    2: LEFT
    3: RIGHT
    4: PICKUP
    5: DISPATCH

Rules:
    - If two robots attempt to enter the same cell simultaneously,
      both moves fail and both robots remain in their current positions.
    - PICKUP succeeds only if the robot is standing on an unclaimed package
      and is not already carrying one.
    - DISPATCH succeeds only if the robot is carrying a package AND is
      standing on a dispatch station cell. A successful DISPATCH awards +1
      point and the robot is no longer carrying a package.
"""

import numpy as np

UP       = 0
DOWN     = 1
LEFT     = 2
RIGHT    = 3
PICKUP   = 4
DISPATCH = 5

ACTION_NAMES = ["UP", "DOWN", "LEFT", "RIGHT", "PICKUP", "DISPATCH"]


class WarehouseEnv:
    """
    Shared 10x10 warehouse grid. Multiple robots compete to collect
    packages and dispatch them at fixed dispatch stations.
    """

    def __init__(self, grid_size=10, n_packages=15, n_robots=2,
                 max_steps=200, seed=None):
        self.grid_size  = grid_size
        self.n_packages_init = n_packages
        self.n_robots   = n_robots
        self.max_steps  = max_steps
        self.rng        = np.random.RandomState(seed)

        # dispatch stations fixed at two opposite corners
        self.dispatch_stations = [(0, 0), (grid_size - 1, grid_size - 1)]

        self.reset()

    # ── setup ────────────────────────────────────────────────────────────

    def reset(self):
        """Start a new episode. Returns dict {robot_id: state}."""
        self.step_count = 0

        # packages: dict (row, col) -> True (unclaimed)
        self.packages = {}
        while len(self.packages) < self.n_packages_init:
            r = self.rng.randint(0, self.grid_size)
            c = self.rng.randint(0, self.grid_size)
            if (r, c) not in self.dispatch_stations and (r, c) not in self.packages:
                self.packages[(r, c)] = True

        # robots
        self.robot_pos      = {}   # robot_id -> (row, col)
        self.robot_carrying = {}   # robot_id -> bool
        self.robot_scores   = {}   # robot_id -> int

        occupied = set(self.packages.keys())
        for rid in range(self.n_robots):
            while True:
                r = self.rng.randint(0, self.grid_size)
                c = self.rng.randint(0, self.grid_size)
                if (r, c) not in occupied and (r, c) not in self.robot_pos.values():
                    self.robot_pos[rid]      = (r, c)
                    self.robot_carrying[rid] = False
                    self.robot_scores[rid]   = 0
                    break

        return {rid: self.get_state(rid) for rid in range(self.n_robots)}

    # ── observation ──────────────────────────────────────────────────────

    def get_state(self, robot_id):
        """
        Return a dict describing the world from robot_id's perspective.
        This is intentionally simple (not a flat vector) so students can
        access fields directly by name: state['position'], state['packages'], etc.
        """
        return {
            "position":          self.robot_pos[robot_id],
            "carrying":          self.robot_carrying[robot_id],
            "packages":          list(self.packages.keys()),
            "dispatch_stations": list(self.dispatch_stations),
            "other_robots": {
                rid: {
                    "position": pos,
                    "carrying": self.robot_carrying[rid],
                }
                for rid, pos in self.robot_pos.items() if rid != robot_id
            },
            "grid_size": self.grid_size,
            "step":      self.step_count,
        }

    # ── stepping ─────────────────────────────────────────────────────────

    def step(self, actions: dict):
        """
        actions: dict {robot_id: action(int 0-5)}
        Returns (states, rewards, done, info)
        """
        self.step_count += 1
        rewards = {rid: 0.0 for rid in range(self.n_robots)}

        # ── 1. compute intended new positions for movement actions ───────
        new_pos = dict(self.robot_pos)  # default: stay where they are
        for rid, action in actions.items():
            r, c = self.robot_pos[rid]
            if action == UP:
                nr, nc = r - 1, c
            elif action == DOWN:
                nr, nc = r + 1, c
            elif action == LEFT:
                nr, nc = r, c - 1
            elif action == RIGHT:
                nr, nc = r, c + 1
            else:
                nr, nc = r, c  # PICKUP / DISPATCH don't move

            nr = max(0, min(self.grid_size - 1, nr))
            nc = max(0, min(self.grid_size - 1, nc))
            new_pos[rid] = (nr, nc)

        # ── 2. detect collisions: two+ robots targeting the same cell ────
        cell_claims = {}
        for rid, pos in new_pos.items():
            cell_claims.setdefault(pos, []).append(rid)

        for pos, rids in cell_claims.items():
            if len(rids) > 1:
                # collision: all robots involved stay at their OLD position
                for rid in rids:
                    new_pos[rid] = self.robot_pos[rid]

        # also prevent a robot from moving into another robot's OLD
        # (unmoving) position if that would create an overlap
        occupied_after = {}
        for rid, pos in new_pos.items():
            occupied_after.setdefault(pos, []).append(rid)
        for pos, rids in occupied_after.items():
            if len(rids) > 1:
                for rid in rids:
                    new_pos[rid] = self.robot_pos[rid]

        self.robot_pos = new_pos

        # ── 3. handle PICKUP / DISPATCH ───────────────────────────────────
        for rid, action in actions.items():
            pos = self.robot_pos[rid]

            if action == PICKUP:
                if (not self.robot_carrying[rid]) and pos in self.packages:
                    del self.packages[pos]
                    self.robot_carrying[rid] = True

            elif action == DISPATCH:
                if self.robot_carrying[rid] and pos in self.dispatch_stations:
                    self.robot_carrying[rid] = False
                    self.robot_scores[rid]  += 1
                    rewards[rid]            += 1.0

        # ── 4. termination ────────────────────────────────────────────────
        all_delivered = (
            len(self.packages) == 0
            and not any(self.robot_carrying[rid] for rid in range(self.n_robots))
        )
        done = all_delivered or self.step_count >= self.max_steps

        states = {rid: self.get_state(rid) for rid in range(self.n_robots)}
        info = {
            "scores":             dict(self.robot_scores),
            "packages_remaining": len(self.packages),
            "step":               self.step_count,
        }
        return states, rewards, done, info

    # ── rendering ────────────────────────────────────────────────────────

    def render(self):
        canvas = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for (r, c) in self.dispatch_stations:
            canvas[r][c] = "D"
        for (r, c) in self.packages:
            canvas[r][c] = "P"
        for rid, (r, c) in self.robot_pos.items():
            canvas[r][c] = str(rid) + ("*" if self.robot_carrying[rid] else "")

        print(f"\nStep {self.step_count} | packages left: {len(self.packages)} "
              f"| scores: {self.robot_scores}")
        for row in canvas:
            print(" ".join(f"{cell:>2}" for cell in row))


# ── convenience runner ───────────────────────────────────────────────────────

def run_episode(agent_a, agent_b, grid_size=10, n_packages=15, seed=None,
                render=False):
    """
    Run one full episode between two agent functions.
    Each agent is a callable: state (dict) -> action (int 0-5).
    Returns (score_a, score_b).
    """
    env = WarehouseEnv(grid_size=grid_size, n_packages=n_packages,
                       n_robots=2, seed=seed)
    states = env.reset()
    done   = False

    while not done:
        actions = {0: agent_a(states[0]), 1: agent_b(states[1])}
        states, _, done, info = env.step(actions)
        if render:
            env.render()

    return info["scores"][0], info["scores"][1]
