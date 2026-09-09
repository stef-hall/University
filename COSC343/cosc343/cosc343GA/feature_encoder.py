"""
feature_encoder.py  ─  PROVIDED TO STUDENTS (do not modify)

Converts a WarehouseEnv state dict (as returned by env.get_state()) into
a fixed-length structured feature vector. Use encode_state(state) to
turn any robot's raw state into a numeric array suitable as input to a
linear model, neural network, or any other parametric agent function.

FEATURE LAYOUT  (total length = FEATURE_SIZE = 215)
──────────────────────────────────────────────────────────────────────
[0]        self x, normalised to [0, 1]
[1]        self y, normalised to [0, 1]
[2]        self carrying status (0 or 1)

[3:12]     opponent block — up to MAX_OTHER_ROBOTS (3) competitors,
           3 values each (x_norm, y_norm, carrying). Slots for robots
           that don't exist are zero-padded. This keeps the feature
           vector a FIXED size regardless of how many robots are
           actually in the environment.

[12:112]   packages grid — flattened 10x10 occupancy grid, row-major.
           1.0 at (row, col) if an unclaimed package sits there, else 0.0

[112:212]  dispatch grid — flattened 10x10 occupancy grid, row-major.
           1.0 at (row, col) if a dispatch station sits there, else 0.0

[212]      crowding metric — number of OTHER robots within Manhattan
           distance 3 of me, normalised by dividing by MAX_OTHER_ROBOTS.
           A proxy for local collision risk.

[213]      on_package — 1.0 if MY position exactly matches a package
           cell, else 0.0.

[214]      on_dispatch — 1.0 if MY position exactly matches a dispatch
           station cell, else 0.0.

NOTE ON FEATURES [213] AND [214]
──────────────────────────────────
Whether a PICKUP or DISPATCH action succeeds depends entirely on
whether your current position exactly matches a cell in the packages
grid or dispatch grid respectively. In principle that information is
already present in features [12:112] and [112:212] (the two 10x10
occupancy grids) combined with your own position in [0:2] — but
recovering it requires effectively performing a coordinate lookup:
checking whether the specific grid cell at (my_row, my_col) is set to
1. Any model consuming this feature vector has to either learn or
compute that lookup itself. Features [213] and [214] simply provide
that already-computed answer directly, which is a common and
reasonable piece of feature engineering for exactly this kind of
"is my position a member of this set" condition. They do not add any
information that wasn't already implicitly present in the grids —
they just make it explicit and immediately usable.
"""

import numpy as np

MAX_OTHER_ROBOTS = 3     # fixed capacity; padded with zeros if fewer exist
GRID_SIZE         = 10
PACKAGES_CELLS    = GRID_SIZE * GRID_SIZE   # 100
DISPATCH_CELLS    = GRID_SIZE * GRID_SIZE   # 100

FEATURE_SIZE = (
    3                               # self block
    + MAX_OTHER_ROBOTS * 3          # opponent block
    + PACKAGES_CELLS                # packages grid
    + DISPATCH_CELLS                # dispatch grid
    + 1                             # crowding metric
    + 2                             # on_package, on_dispatch
)   # = 3 + 9 + 100 + 100 + 1 + 2 = 215


def _manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def encode_state(state):
    """
    state : dict, as returned by WarehouseEnv.get_state(robot_id)
        {
          "position": (row, col),
          "carrying": bool,
          "packages": [(row, col), ...],
          "dispatch_stations": [(row, col), ...],
          "other_robots": {robot_id: {"position":.., "carrying":..}, ...},
          "grid_size": int,
          "step": int,
        }

    Returns
    -------
    np.array of shape (FEATURE_SIZE,) dtype float32
    """
    g   = state["grid_size"]
    pos = state["position"]

    feat = np.zeros(FEATURE_SIZE, dtype=np.float32)

    # ── 1. self-state ────────────────────────────────────────────────────
    feat[0] = pos[0] / (g - 1)
    feat[1] = pos[1] / (g - 1)
    feat[2] = 1.0 if state["carrying"] else 0.0

    # ── 2. opponent state (flattened, padded/truncated to fixed size) ────
    others = list(state["other_robots"].values())
    for i in range(MAX_OTHER_ROBOTS):
        base = 3 + i * 3
        if i < len(others):
            opos = others[i]["position"]
            feat[base]     = opos[0] / (g - 1)
            feat[base + 1] = opos[1] / (g - 1)
            feat[base + 2] = 1.0 if others[i]["carrying"] else 0.0
        # else leave as zero padding

    # ── 3. packages grid (flattened 10x10 occupancy) ─────────────────────
    pkg_offset = 3 + MAX_OTHER_ROBOTS * 3
    for (r, c) in state["packages"]:
        idx = pkg_offset + r * g + c
        if 0 <= idx < pkg_offset + PACKAGES_CELLS:
            feat[idx] = 1.0

    # ── 4. dispatch grid (flattened 10x10 occupancy) ─────────────────────
    disp_offset = pkg_offset + PACKAGES_CELLS
    for (r, c) in state["dispatch_stations"]:
        idx = disp_offset + r * g + c
        if 0 <= idx < disp_offset + DISPATCH_CELLS:
            feat[idx] = 1.0

    # ── 5. crowding metric ─────────────────────────────────────────────
    crowd_offset = disp_offset + DISPATCH_CELLS
    crowding_count = sum(
        1 for info in others if _manhattan(pos, info["position"]) <= 3
    )
    feat[crowd_offset] = crowding_count / MAX_OTHER_ROBOTS

    # ── 6. engineered lookup features (see module docstring) ─────────────
    on_package_offset  = crowd_offset + 1
    on_dispatch_offset = crowd_offset + 2
    feat[on_package_offset]  = 1.0 if pos in state["packages"] else 0.0
    feat[on_dispatch_offset] = 1.0 if pos in state["dispatch_stations"] else 0.0

    return feat
