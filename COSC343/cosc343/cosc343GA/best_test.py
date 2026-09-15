import random
import time
import numpy as np
from agents import random_agent
from warehouse_env import run_episode
from greedy_agent import greedy_agent
from smart_custom_agent import smart_custom_agent
from ga_agent import GAAgent
from ga_agent import evalFitness, newGeneration

data = np.load("best_ga_agent1.npz")

model = {
    "weights": data["weights"],
    "biases": data["biases"]
}

Best_Descendant = GAAgent(model)


x = 2**31
ties = []
while True:
    score_a, score_b = run_episode(Best_Descendant, greedy_agent, seed=1362929405, render=True)
    break


input("Press Enter to Close...")

"""
Extradionary Results:
Score: 6-5 | Seed: 469422092


"""