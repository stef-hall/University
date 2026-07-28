__author__ = "Stefan Hall"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "Halst863@student.otago.ac.nz"

import random

agentName = "Agent A"

def has_left_right_connection(cells, B): # I borrowed your connection checking code

   cells = set(cells)
   paths = []

   for x,y in list(cells):
      if y==0:
         paths.append((x,y))
         cells.discard((x,y))

   rules = [ (0,-1),(-1,0),(-1,1),(1,0),(0,1),(1,-1)]

   i = 0
   while i<len(paths):
      x,y = paths[i]
      for xd,yd in rules:
         ncell = (x+xd,y+yd)
         if ncell in cells:
            if ncell[1] == B-1:
               return True
            paths.append(ncell)
            cells.discard(ncell)

      i += 1

   return False

def has_top_bottom_connection(cells, N):
   cells = [(b, a) for (a, b) in cells]
   return has_left_right_connection(cells, N)



def minimax(mine, opp, B):
   mine = set(mine)
   opp = set(opp)
   board = set()
   cache = {}
   best_move = None
   best_score = -69
   
   for x in range(B): # Initalize board
      for y in range(B):
         board.add((x,y))

   def search(mine, opp, my_turn): # Recursive min max search
      state = (frozenset(mine), frozenset(opp), my_turn)

      if state in cache:
         return cache[state]
      
      if has_left_right_connection(mine, B):
         return 1
      if has_top_bottom_connection(opp, B):
         return -1
      
      empty = board - mine - opp

      if my_turn:
         scores = []
         for move in empty:
            new_mine = mine | {move}
            result = search(new_mine, opp, False)
            scores.append(result)
         score = max(scores)

      else:
         scores = []
         for move in empty:
            new_opp = opp | {move}
            result = search(mine, new_opp, True)
            scores.append(result)
         score = min(scores)

      cache[state] = score
      return score

   
   empty = board - mine - opp
   for move in empty:
      score = search(mine | {move}, opp, False)
      if score > best_score:
         best_score = score
         best_move = move

   return best_move

class HexAgent():
   """
   A class that encapsulates the code dictating the
   behaviour of the agent playing the game of Hex.

   ...

   Attributes
   ----------
   B : board size

   Methods
   -------
   AgentFunction(percepts)
      Returns the position of the board where to place a piece
   """

   def __init__(self, B):
      """
      :B: board size (BxB). 
 
      """
      self.B = B

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
      
      # Make a random choice of the card to bid with
      move = minimax(myHexes, oppHexes, self.B)
      print(move)
      return move
      