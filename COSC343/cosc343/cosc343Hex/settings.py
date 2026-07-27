__author__ = "Lech Szymanski"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "lech.szymanski@otago.ac.nz"

# You can manipulate these settings to change how the game is played.

game_settings = {

   # agent files that play the game
   "players": ("my_agent.py", "random_agent.py"), 

   "B": 4,                      # board size is BxB
   
   "totalNumberOfGames": 1,   # total number of games played

   "verboseLevel": 2,           # level of verbosity:
                                # 0 - no output, 
                                # 1 - summary of the game, 
                                # 2 - detailed output   
}


# If main is run, create an instance of the game and run it
if __name__ == "__main__":
   from hex import HexGame

   game = HexGame(B=game_settings['B'],
                  verbose=game_settings['verboseLevel'])
   
   game.run(agentFiles=game_settings['players'],
            num_games=game_settings['totalNumberOfGames'])