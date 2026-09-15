import random
import time
import numpy as np
from agents import random_agent
from warehouse_env import run_episode
from greedy_agent import greedy_agent
from smart_custom_agent import smart_custom_agent
from ga_agent import GAAgent
from ga_agent import evalFitness, newGeneration


data = np.load("best_ga_agent.npz")

model = {
    "weights": data["weights"],
    "biases": data["biases"]
}

Best_Descendant = GAAgent(model)



initial_population = 200
generations = 200
mutation_rate = 0.04
save_best = 1

bots = []
for i in range(initial_population):
    bot = GAAgent(model)
    bots.append(bot)

print("Pre-training evaluation:")
wins, draws, losses = 0, 0, 0
for bot in bots:
    score_a, score_b = run_episode(bot, Best_Descendant, seed=random.randint(1, 1000), render=False)
    if score_a > score_b:
        wins += 1
    elif score_a == score_b:
        draws += 1
    else:
        losses += 1
print(f"Wins: {wins} | Draws: {draws} | Losses: {losses}")
print(f"Win rate: {(wins / len(bots)) * 100:.2f}%")

print("Generation, Average Fitness, Best Fitness")
for i in range(generations):
    offset = random.randint(1,1000)
    fitnesses = evalFitness(bots, greedy_agent, seeds=[1+offset, 2+offset, 3+offset])
    #print(f"[{i}] Average Fitness:", sum(fitnesses) / len(fitnesses))
    #print(f"[{i}] Round:", fitnesses)
    #print(sum(fitnesses) / len(fitnesses))
    print(f"{i}, {sum(fitnesses) / len(fitnesses)}, {max(fitnesses)}")
    bots = newGeneration(bots, fitnesses, mutation_rate)

final_fitnesses = evalFitness(bots, greedy_agent, seeds=[1, 2, 3])
Best_Descendant = bots[final_fitnesses.index(max(final_fitnesses))]
if save_best == 1:
    np.savez("best_ga_agent.npz", weights=Best_Descendant.weights, biases=Best_Descendant.biases)

print("Results agaisnt Greedy Agent:")
for seed in range(10):
    score_a, score_b = run_episode(Best_Descendant, greedy_agent, seed=seed, render=False)
    print(f"Score: {score_a}-{score_b} | Seed: {seed}")

print("Results agaisnt Smart Custom Agent:")
for seed in range(10):
    score_a, score_b = run_episode(Best_Descendant, smart_custom_agent, seed=seed, render=False)
    print(f"Score: {score_a}-{score_b} | Seed: {seed}")


input("Press Enter to close...")