__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

import random

agentName = "random"

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
