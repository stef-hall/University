__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

import sys
import readchar

agentName = "human"

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
      
      print("(",end="")
      sys.stdout.flush()
      # Get the input
      action = []
      digits = []
      while True:
         c = readchar.readchar()
         if c=='\x03':
            # Ctrl-C exits the entire program
            sys.exit(-1)
         elif c=='\x7f':
            # Backspace removes last character written
            if len(digits) > 0:
               digits.pop()
               sys.stdout.write(" \b\b_\b")
            elif len(action) == 1:
               digits = list(str(action[0]))
               digits.pop()
               action = []
               sys.stdout.write(" \b\b\b_ \b\b")
            sys.stdout.flush()

         elif (c=='\r' or c=='\n' or c==')'):
            if len(action)==1:
               number = int(''.join(map(str, digits)))
               action.append(number)
               print(")")
               break

         if c == ',' and len(action)==0:
            number = int(''.join(map(str, digits)))
            action.append(number)
            digits = []
            sys.stdout.write(",")
            sys.stdout.write("_")
            sys.stdout.write("\b")
            sys.stdout.flush()


         if c.isdigit():
            digits.append(c)
            sys.stdout.write(c)
            sys.stdout.write("_")
            sys.stdout.write("\b")
            sys.stdout.flush()

      sys.stdout.write("\r\n")
      sys.stdout.flush()

      return tuple(action)
