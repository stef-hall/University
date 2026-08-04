__author__ = "Stefan Hall"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "Halst863@student.otago.ac.nz"

import random

agentName = "Agent C"

def has_top_bottom_connection(cells, B): # I borrowed your connection checking code
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


def has_left_right_connection(cells, N):
   cells = [(b, a) for (a, b) in cells]
   return has_top_bottom_connection(cells, N)


def heuristic(mine, opp, B):
   return 0


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
         
         if has_top_bottom_connection(mine, B): # Base Cases
            return 1
         if has_left_right_connection(opp, B):
            return -1
         if depth >= self.D:
            return heuristic(mine, opp, B)

         fully_searched = True
         empty = board - mine - opp

         if my_turn:
            score = -float("inf")
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
      