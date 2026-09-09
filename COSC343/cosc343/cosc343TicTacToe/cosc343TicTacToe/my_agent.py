__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

# Import the random number generation library
import random
import numpy as np



def check_win(mine, opp):
        state = np.zeros((3, 3), dtype=int)
        for r, c in mine:
            state[r, c] = 1

        for r, c in opp:
            state[r, c] = -1

        winner = 0
        for i in range(3):
            s = np.sum(state[i, :])
            if np.abs(s)==3:
                winner = np.sign(s)
                break

            s = np.sum(state[:,i])
            if np.abs(s)==3:
                winner = np.sign(s)
                break

        s = state[0,0]+state[1,1]+state[2,2]
        if np.abs(s)==3:
            winner = np.sign(s)

        s = state[2,0]+state[1,1]+state[0,2]
        if np.abs(s)==3:
            winner = np.sign(s)

        return winner

def minimax(mine, opp, state, B):
   mine = set(mine)
   opp = set(opp)
   board = set()
   cache = {}
   best_move = None
   best_score = -float("inf")
   
   for x in range(B): # Initalize board
      for y in range(B):
         board.add((x,y))

   def search(mine, opp, my_turn): # Recursive min max search
      state = (frozenset(mine), frozenset(opp), my_turn) # Set State search for O(1)
      if state in cache:
         return cache[state]
      
      winner = check_win(mine, opp)
      if winner == 1:
          return 1
      if winner == -1:
          return -1 
      if winner == -1:
          return -1  
      
      empty = board - mine - opp

      if my_turn:
         score = -float("inf")
         for move in empty:
            new_mine = mine | {move}
            result = search(new_mine, opp, False)
            score = max(score, result)
            if score == 1:
               break
         
      else:
         score = float("inf")
         for move in empty:
            new_opp = opp | {move}
            result = search(mine, new_opp, True)
            score = min(score, result)
            if score == -1:
               break

      cache[state] = score # Update cache
      return score


   empty = board - mine - opp
   for move in empty:
      score = search(mine | {move}, opp, False)
      if score > best_score:
         best_score = score
         best_move = move

   return best_move

class TicTacToeAgent():
    """
           A class that encapsulates the code dictating the
           behaviour of the TicTacToe playing agent

           Methods
           -------
           AgentFunction(percepts)
               Returns the move made by the agent given state of the game in percepts
           """

    def __init__(self, h):
        """Initialises the agent

        :param h: Handle to the figures showing state of the board -- only used
                  for human_agent.py to enable selecting next move by clicking
                  on the matplotlib figure.
        """
        pass



    def AgentFunction(self, percepts):
        """The agent function of the TicTacToe agent -- returns action
         relating the row and column of where to make the next move

        :param percepts: the state of the board a list of rows, each
        containing a value of three columns, where 0 identifies the empty
        suare, 1 is a square with this agent's mark and -1 is a square with
        opponent's mark
        :return: tuple (r,c) where r is the row and c is the column index
                 where this agent wants to place its mark
        """

        # This agent is awesome
        myMoves = set()
        oppMoves = set()

        for r in range(3):
            for c in range(3):
                pos = percepts[r][c]
                if pos == 1:
                    myMoves.add((r,c))
                if pos == -1:
                    oppMoves.add((r,c))

        move = minimax(myMoves,oppMoves,percepts,3)
        return move

        


