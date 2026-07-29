__author__ = "Stefan Hall"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "Halst863@student.otago.ac.nz"

import random
import heapq

agentName = "Agent C3P0"

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


def advanced_heuristic(mine, opp, B):
   mine = set(mine)
   opp = set(opp)

   rules = [(0, -1), (-1, 0), (-1, 1), (1, 0), (0, 1), (1, -1)]

   def on_board(cell):
      x, y = cell
      return x >= 0 and x < B and y >= 0 and y < B


   def shortest_connection(stones, blocked):
      distances = {}
      queue = []

      # Start from every cell on the top edge.
      for x in range(B):
         cell = (x, 0)

         if cell in blocked:
            continue

         if cell in stones:
            cost = 0
         else:
            cost = 1

         distances[cell] = cost
         heapq.heappush(queue, (cost, cell))

      while len(queue) > 0:
         cost, cell = heapq.heappop(queue)

         if cost != distances[cell]:
            continue

         x, y = cell

         # Reaching the bottom edge completes a route.
         if y == B - 1:
            return cost

         for xd, yd in rules:
            neighbour = (x + xd, y + yd)

            if not on_board(neighbour):
               continue

            if neighbour in blocked:
               continue

            if neighbour in stones:
               next_cost = cost
            else:
               next_cost = cost + 1

            if neighbour not in distances or next_cost < distances[neighbour]:
               distances[neighbour] = next_cost
               heapq.heappush(queue, (next_cost, neighbour))

      # The opponent has completely blocked every possible route.
      return B * B


   def bridge_count(stones, blocked):
      stones = list(stones)
      bridges = 0

      for i in range(len(stones)):
         first = stones[i]
         first_neighbours = set()

         for xd, yd in rules:
            neighbour = (first[0] + xd, first[1] + yd)

            if on_board(neighbour):
               first_neighbours.add(neighbour)

         for j in range(i + 1, len(stones)):
            second = stones[j]
            second_neighbours = set()

            for xd, yd in rules:
               neighbour = (second[0] + xd, second[1] + yd)

               if on_board(neighbour):
                  second_neighbours.add(neighbour)

            shared = first_neighbours & second_neighbours

            # Two shared empty cells means a Hex bridge:
            # if the opponent takes one, you can take the other.
            if len(shared) == 2:
               empty_bridge = True

               for cell in shared:
                  if cell in stones or cell in blocked:
                     empty_bridge = False

               if empty_bridge:
                  bridges += 1

      return bridges


   def link_count(stones):
      links = 0

      for cell in stones:
         x, y = cell

         for xd, yd in rules:
            neighbour = (x + xd, y + yd)

            if neighbour in stones and cell < neighbour:
               links += 1

      return links


   def edge_count(stones):
      count = 0

      for x, y in stones:
         if y == 0 or y == B - 1:
            count += 1

      return count


   # My route is already top-to-bottom in the agent's coordinates.
   my_cost = shortest_connection(mine, opp)
   my_bridges = bridge_count(mine, opp)
   my_links = link_count(mine)
   my_edges = edge_count(mine)

   # Flip the opponent so their left-to-right goal becomes top-to-bottom.
   flipped_mine = set()
   flipped_opp = set()

   for x, y in mine:
      flipped_mine.add((y, x))

   for x, y in opp:
      flipped_opp.add((y, x))

   opp_cost = shortest_connection(flipped_opp, flipped_mine)
   opp_bridges = bridge_count(flipped_opp, flipped_mine)
   opp_links = link_count(flipped_opp)
   opp_edges = edge_count(flipped_opp)

   # Fewer empty cells required for my route is good.
   score = (opp_cost - my_cost) / B

   # A one-cell route is an immediate, serious threat.
   if my_cost == 1:
      score += 0.25

   if opp_cost == 1:
      score -= 0.25

   # Reward resilient virtual connections and real connected chains.
   score += 0.10 * (my_bridges - opp_bridges) / B
   score += 0.02 * (my_links - opp_links) / B

   # Stones already touching a goal edge are more valuable.
   score += 0.08 * (my_edges - opp_edges) / B

   # Terminal wins/losses remain +1/-1 in minimax.
   # Keep heuristic values strictly inside that range.
   if score > 0.99:
      return 0.99

   if score < -0.99:
      return -0.99

   return score


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
      self.D = 3 
      self.cache = {}
      self.board = set()
      self.cross_game_cache = 1 # 1=On, 0=Off
      
      for x in range(B): # Initalize board
         for y in range(B):
            self.board.add((x,y))


   def sort(self, empty, mine, opp):
      mine_adjacent = set()
      opp_adjacent = set()

      rules = [(0, -1), (-1, 0), (-1, 1), (1, 0), (0, 1), (1, -1)]

      for cell in empty:
         x, y = cell

         for xd, yd in rules:
            neighbour = (x + xd, y + yd)

            if neighbour in mine:
               mine_adjacent.add(cell)

            if neighbour in opp:
               opp_adjacent.add(cell)

      remainder = empty - mine_adjacent - opp_adjacent

      return (
         list(mine_adjacent)
         + list(opp_adjacent - mine_adjacent)
         + list(remainder)
      )


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
            return advanced_heuristic(mine, opp, B)

         fully_searched = True
         empty = board - mine - opp

         if my_turn:
            score = -float("inf")
            empty = self.sort(empty, mine, opp)
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
            empty = self.sort(empty, mine, opp)
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
      empty = self.sort(empty, mine, opp)
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
      