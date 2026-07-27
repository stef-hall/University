__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

import random
import math
from hex import has_left_right_connection, has_top_bottom_connection

agentName = "blocking"

class HexAgent():

   def __init__(self, B):
      self.B = B


   def AgentFunction(self, percepts):

      myHexes = percepts[0]
      oppHexes = percepts[1]

      occupied = set(myHexes + oppHexes)

      moves = [
         (x,y)
         for x in range(self.B)
         for y in range(self.B)
         if (x,y) not in occupied
      ]


      # 1. Take winning move if available
      for move in moves:
         if has_left_right_connection(myHexes + [move], self.B):
            return move


      # 2. Block opponent winning move
      for move in moves:
         if has_top_bottom_connection(oppHexes + [move], self.B):
            return move


      # 3. Otherwise play closest to centre
      centre = (self.B-1)/2

      best_moves = []
      best_dist = float("inf")

      for move in moves:
         dist = math.sqrt(
            (move[0]-centre)**2 +
            (move[1]-centre)**2
         )

         if dist < best_dist:
            best_dist = dist
            best_moves = [move]
         elif dist == best_dist:
            best_moves.append(move)

      return random.choice(best_moves)
