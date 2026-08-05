__author__ = "Stefan Hall"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "Halst863@student.otago.ac.nz"

import random
from collections import deque

agentName = "Agent C2"

from functools import lru_cache


@lru_cache(maxsize=None)
def _hex_masks(B):
    ALL = (1 << (B * B)) - 1

    left_col = 0
    right_col = 0
    top_row = 0
    bottom_row = 0

    for y in range(B):
        left_col |= 1 << (y * B)
        right_col |= 1 << (y * B + B - 1)

    for x in range(B):
        top_row |= 1 << x
        bottom_row |= 1 << ((B - 1) * B + x)

    not_left = ALL ^ left_col
    not_right = ALL ^ right_col

    return ALL, left_col, right_col, top_row, bottom_row, not_left, not_right


def _to_bits(cells, B):
    bits = 0
    for x, y in cells:
        bits |= 1 << (y * B + x)
    return bits


def _expand(bits, cells, B, not_left, not_right, ALL):
    return (
        (bits >> B) |
        ((bits << B) & ALL) |
        ((bits & not_left) >> 1) |
        ((bits & not_right) << 1) |
        ((bits & not_right) >> (B - 1)) |
        (((bits & not_left) << (B - 1)) & ALL)
    ) & cells


def has_top_bottom_connection(cells, B):
    ALL, left, right, top, bottom, not_left, not_right = _hex_masks(B)

    cells = _to_bits(cells, B)

    connected = cells & top

    while connected:
        if connected & bottom:
            return True

        expanded = connected | _expand(
            connected, cells, B, not_left, not_right, ALL
        )

        if expanded == connected:
            return False

        connected = expanded

    return False


def has_left_right_connection(cells, B):
    ALL, left, right, top, bottom, not_left, not_right = _hex_masks(B)

    cells = _to_bits(cells, B)

    connected = cells & left

    while connected:
        if connected & right:
            return True

        expanded = connected | _expand(
            connected, cells, B, not_left, not_right, ALL
        )

        if expanded == connected:
            return False

        connected = expanded

    return False

def rotate_board(cells):
    cells = [(b, a) for (a, b) in cells]
    return cells

def heuristic(mine, opp, empty, B):
    rules = [ (0,-1),(-1,0),(-1,1),(1,0),(0,1),(1,-1)]

    queue = deque()
    distance = {}

    for x in range(B):
        start = (x,0)
        if start in mine:
            distance[start] = 0
            queue.appendleft(start)
        elif start in empty:
            distance[start] = 1
            queue.append(start)

    while queue:
        current = queue.popleft()

        if current[1] == B-1: # This is the win condition
            return distance[current]

        for diff in rules:
            neighbour = (current[0] + diff[0], current[1] + diff[1])

            if neighbour in mine:
                cost = 0
            elif neighbour in empty:
                cost = 1
            else:
                continue

            total_distance = distance[current] + cost
            if (neighbour not in distance) or (total_distance < distance[neighbour]):
                distance[neighbour] = total_distance
                if cost == 0:
                     queue.appendleft(neighbour)
                else:
                     queue.append(neighbour)

    return (B * B)

def sort(empty, mine, opp):
    mine_adj = set()
    opp_adj = set()

    rules = [ (0,-1),(-1,0),(-1,1),(1,0),(0,1),(1,-1)]

    for hex in empty:
        for diff in rules:
            neighbour = (hex[0] + diff[0] , hex[1] + diff[1])
            if neighbour in mine:
                mine_adj.add(hex)
            elif neighbour in opp:
                opp_adj.add(hex)

    leftover = empty - mine_adj - opp_adj

    return (list(mine_adj) + list(opp_adj) + list(leftover))


class HexAgent():
   """
   A class that encapsulates the code dictating the
   behaviour of the agent playing the game of Hex.

   ...

   Attributes
   ----------
   B : board size
   Cross_Game_Cache : Persistent Cache

   Methods
   -------
   AgentFunction(percepts)
      Returns the position of the board where to place a piece
   """

   def __init__(self, B):
      """
      :B: board size (BxB). 
      
      :D: The depth the partial search should go.

      :cross_game_cache: This determines whether or not the cache is stored per agent instance,
      or per game. As the code plays all games on a single agent instant, persistent cache is an
      enourmous upgrade, but it means knowledge from one game helps another. 
      For a fair per-game test you can turn this off.
      
      """
      self.B = B
      self.D = 4 
      self.cache = {}
      self.board = set()
      self.cross_game_cache = 1 # 1=On, 0=Off
      
      for x in range(B): # Initalize board
         for y in range(B):
            self.board.add((x,y))



   def minimax(self, mine, opp, B):
      mine = set(mine)
      opp = set(opp)
      board = self.board
      best_move = None
      best_score = -float("inf")
      alpha = -float("inf")
      beta = float("inf")
      

      def search(mine, opp, my_turn, alpha, beta, depth): # Recursive min max search
         state = (frozenset(mine), frozenset(opp), my_turn, depth) # Set State search for O(1)
         if state in self.cache:
            return self.cache[state]

         fully_searched = True
         empty = board - mine - opp
         
         if has_top_bottom_connection(mine, B): # Base Cases
            return 1
         if has_left_right_connection(opp, B):
            return -1
         if depth >= self.D:
            m = heuristic(mine,opp,empty,B)
            o = heuristic(rotate_board(opp),rotate_board(mine),rotate_board(empty),B)
            score = 0.99 * ((o-m) / (B * B))
            return score

         if my_turn:
            score = -float("inf")
            empty = sort(empty, mine, opp)
            for move in empty:
               new_mine = mine | {move}
               result = search(new_mine, opp, False, alpha, beta, depth + 1)
               score = max(score, result)
               alpha = max(alpha, score)
               if score == 1:
                  fully_searched = True
                  break
               if alpha >= beta:
                  fully_searched = False
                  break
            
         else:
            score = float("inf")
            empty = sort(empty, mine, opp)
            for move in empty:
               new_opp = opp | {move}
               result = search(mine, new_opp, True, alpha, beta, depth + 1)
               score = min(score, result)
               beta = min(beta, score)
               if score == -1:
                  fully_searched = True
                  break
               if alpha >= beta:
                  fully_searched = False
                  break

         if fully_searched:
            self.cache[state] = score # Update cache if whole state is present
         return score

      empty = board - mine - opp
      empty = sort(empty, mine, opp)
      for move in empty:
         score = search(mine | {move}, opp, False, alpha, beta, 0)
         if score > best_score:
            best_score = score
            best_move = move

         alpha = max(alpha, best_score)
         if best_score == 1:
            break

      return best_move

   def AgentFunction(self, percepts):
      """Returns the hex coordinates where to place the piece

      :param percepts: a tuple of two items: (myHexes, oppHexes), where
      
         - myHexes - is a list of this agent's hexes listed as coordinates (x1,y1),(x2,y2),...

        - oppHexes - is a list of this opponent's hexes listed as coordinates (x1,y1),(x2,y2),...

      :return: (x,y) - coordinates of an unoccupied hex to be taken
      """

      # Extract different parts of percepts.
      myHexes = percepts[0]
      oppHexes = percepts[1]

      # Per game cache reset, determined by
      if self.cross_game_cache == 0:
         if len(myHexes) == 0:
            self.cache = {}

      
      # Make a minimax optimized move
      move = self.minimax(myHexes, oppHexes, self.B)
      return move
      