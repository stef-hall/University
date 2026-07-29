__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

import os,sys
import numpy as np
import importlib.util
import time
from settings import game_settings

class bcolors:
   RED = '\033[1;30;41m'
   BLUE = '\033[1;30;44m'
   ENDC = '\033[0m'


def time_to_str(time_in_seconds):
   timeStr = ''
   if time_in_seconds > 3600:
      hours = int(np.floor(time_in_seconds / 3600))
      timeStr += "%d h, " % hours
      time_in_seconds %= 3600

   if time_in_seconds > 60:
      minutes = int(np.floor(time_in_seconds / 60))
      timeStr += "%d min, " % minutes
      time_in_seconds %= 60

   if time_in_seconds < 1:
      timeStr += "%.3f s" % time_in_seconds
   else:
      timeStr += "%d s" % time_in_seconds

   return timeStr

# Class player is a wrapper for a player agent
class Player:
   def __init__(self, game, playerFile, jointname=False):
      self.playerFile = playerFile
      self.game = game

      # Player file must be in same folder as hex.py
      game_folder = os.path.dirname(os.path.realpath(__file__))
      playerFile = os.path.join(game_folder,playerFile)

      if not os.path.exists(playerFile):
         raise RuntimeError("Error! Agent file '%s' not found" % self.playerFile)

      if len(self.playerFile) > 3 and self.playerFile[-3:].lower() == '.py':
         playerModule = self.playerFile[:-3]
      else:
         raise RuntimeError("Error! Agent file %s needs a '.py' extension" % self.playerFile)


      try:

         spec = importlib.util.spec_from_file_location(playerModule, playerFile)
         self.exec = importlib.util.module_from_spec(spec)
         sys.modules["module.name"] = self.exec
         spec.loader.exec_module(self.exec)
      except Exception as e:
         raise RuntimeError(str(e))

      try:
         self.agent = self.exec.HexAgent(game.B)
      except Exception as e:
         raise RuntimeError(str(e))

      if hasattr(self.exec, 'agentName') and self.exec.agentName[0] != '<':
         self.name = self.exec.agentName
      else:
         if self.game.in_tournament and self.playerFile != 'random_agent.py':
            self.name = self.playerFile.split('/')[-2]# playerFile.split('.')[1]
         else:
            self.name = self.playerFile

      if jointname and self.game.in_tournament:
         self.pname = self.playerFile.split('/')[-2]

def print_board(B, oB, oR):
    for i in range(B):
       print(f' {i}', end="")
    print("")
    for i in range(B):
        print(" " * i, end="")  # indentation
        print(f'{i}',end=" ")
        for j in range(B):
            cell = (i,j)
            if cell in oB:
                sys.stdout.write(f"{bcolors.BLUE}B{bcolors.ENDC}")
            elif cell in oR:
                sys.stdout.write(f"{bcolors.RED}R{bcolors.ENDC}")
            else:
                sys.stdout.write(f".")
            print("", end=" ")
        print()

def print_board_flipped(B, oB, oR):
    for j in range(B):
       print(f' {j}', end="")
    print("")
    for j in range(B):
        print(" " * j, end="")  # indentation
        print(f'{j}',end=" ")
        for i in range(B):
            cell = (i,j)
            if cell in oB:
                sys.stdout.write(f"{bcolors.BLUE}B{bcolors.ENDC}")
            elif cell in oR:
                sys.stdout.write(f"{bcolors.RED}R{bcolors.ENDC}")
            else:
                sys.stdout.write(f".")
            print("", end=" ")
        print()


def has_left_right_connection(cells, B):

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

class HexGame:

   def __init__(self,B, verbose=0,tournament=False):

      self.B = B
      self.in_tournament = tournament
      self.verbose = verbose

      if tournament:
         self.throwError = self.errorAndReturn
      else:
         self.throwError = self.errorAndExit 

      if self.verbose:
         print("Hex game settings:")
         print(f' Board size: ({B},{B})')

   def errorAndExit(self,errorStr):
      raise RuntimeError(errorStr)

   def errorAndReturn(self,errorStr):
      self.errorStr = errorStr
      return None

   def play(self,players,pstart):

      score = None

      oB = []
      oR = []

      if pstart == 1:
         players = [players[1], players[0]]

      if self.verbose > 1:
         print("\nBoard:")
         print(f" Blue: {players[0].name}")
         print(f" Red: {players[1].name}")
         print_board(self.B, oB, oR)

      while score is None:

         percepts = (oB, oR)
         for p, player in enumerate(players):

            errStr = None
            while True:

               if player.playerFile == 'human_agent.py':
               
                  if errStr is None:
                     print("\nBoard:")
                     print(f" Blue: {players[0].name}")
                     print(f" Red: {players[1].name}")
                     if p==0:
                        print_board(self.B, oB, oR)
                     else:
                        print_board_flipped(self.B, oB, oR)

                  if errStr is not None:
                     print(errStr)
                  print(f"{'blue' if p==0 else 'red'} player move (row,col):", end="")               


               try:
                  action = player.agent.AgentFunction(percepts)
               except Exception as e:
                  self.throwError(str(e))
            
               if type(action) != tuple:
                  self.throwError("Error! AgentFunction from '%s.py' returned non tuple" % (player.playerFile))

               if len(action) != 2:
                  self.throwError("Error! AgentFunction from '%s.py' must return tuple of two" % (player.playerFile))

               a,b = action
               if p==1:
                  a,b = b,a
                  action = a,b               

               if type(a) != int and type(b) != int:
                  self.throwError("Error! AgentFunction from '%s.py' must return tuple of two ints" % (player.playerFile))

               if a < 0 or a >= self.B:
                  if player.playerFile == 'human_agent.py':
                     errStr = f'!!! Position {action} is outside of the board !!!'
                     continue
                  else:
                     self.throwError(f"Error! AgentFunction from '%s.py' must return tuple of ints between 0 and {self.B-1}" % (player.playerFile))

               if b < 0 or b >= self.B:
                  if player.playerFile == 'human_agent.py':
                     errStr = f'!!! Position {action} is outside of the board !!!'
                     continue
                  else:
                     self.throwError(f"Error! AgentFunction from '%s.py' must return tuple of ints between 0 and {self.B-1}" % (player.playerFile))


               if action in oB or action in oR:
                  if player.playerFile == 'human_agent.py':
                     errStr = f'!!! Position {action} is already taken !!!'
                     continue
                  else:
                     self.throwError("Error! AgentFunction from '%s.py' returned move that was already taken" % (player.playerFile))

               break

            if p==0:
               oB.append(action)
            else:
               oR.append(action)


            if self.verbose > 1:
               print("\nBoard:")
               print(f" Blue: {players[0].name}")
               print(f" Red: {players[1].name}")
               print_board(self.B, oB, oR)

            if p==0:
               if has_left_right_connection(oB, self.B):
                  score = [1,0]
            else:
               if has_top_bottom_connection(oR, self.B):
                  score = [0,1]

            percepts = ([(b, a) for (a, b) in oR],
                        [(b, a) for (a, b) in oB])


            if score is not None:
               if self.verbose > 1:
                  if p==0:
                     c = 'Blue'
                  else:
                     c = 'Red'
                  print(f"{c}: {player.name} wins!")

               break

      if pstart == 1:
         score = [score[1], score[0]]

      if self.verbose:
         print("")
      return score


   def run(self,agentFiles,num_games=1000):

      if self.verbose:
         print("Game play:")
         print("  Num rounds:       %d" % num_games)

      players = []
      for i, agentFile in enumerate(agentFiles):
         try:
            player = Player(game=self, playerFile=agentFile)
            players.append(player)
         except Exception as e:
            self.throwError(str(e))

      score = np.zeros((2, ))
      game_count = 0
      tot_time = 0      
      verbose = self.verbose
      for n in range(num_games):
         if verbose:
            print("\nRound %d/%d" % (game_count+1,num_games))

         start = time.time()
         game_score = self.play(players,pstart=n%2)
         end = time.time()
         score += game_score
         game_count += 1
         score_str = "  Score in game %d: " % game_count
         for i in range(len(players)):
            score_str += "\n    Player %d (%s): %.2f" % (i+1, players[i].name, game_score[i])
         if verbose:
            print(score_str)
 
         if n == num_games-1:
            verbose=max(self.verbose, 1)

         score_str = "\nAverage score after game %d: " % game_count
         for i in range(len(players)):
            score_str += "\n  Player %d (%s): %.2f" % (i+1, players[i].name, score[i]/game_count)
         if verbose:
            print(score_str)
         tot_time += end - start

         if game_count < num_games:
            avg_time = tot_time / game_count
            if verbose:
               print("Average running time per game %s." % (time_to_str(avg_time)))
               print("Time remaining %s." % (time_to_str(avg_time * (num_games-game_count))))
               print("Expected total running time %s." % (time_to_str(avg_time * num_games)))
         elif verbose:
            print("Total running time %s." % (time_to_str(tot_time)))

if __name__ == "__main__":

   game = HexGame(B=game_settings['B'],
                  verbose=game_settings['verboseLevel'])
   
   game.run(agentFiles=game_settings['players'],
            num_games=game_settings['totalNumberOfGames'])



