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
      while True:
         hex = (random.randint(0,self.B-1), random.randint(0,self.B-1))
         if hex not in myHexes and hex not in oppHexes:
            break

      return hex
      