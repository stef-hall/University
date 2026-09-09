import random
from agents import random_agent
from warehouse_env import run_episode
from greedy_agent import greedy_agent
from smart_custom_agent import smart_custom_agent
from ga_agent import GAAgent
from ga_agent import evalFitness, newGeneration

bot_a = greedy_agent #Has a fitness of 400
bot_b = GAAgent()

render = False

bots = []
for i in range(50):
    bot = GAAgent()
    bots.append(bot)

for i in range(200):
    fitnesses = evalFitness(bots, greedy_agent, seeds=[1,2])
    print(f"[{i}] Average Fitness:", sum(fitnesses) / len(fitnesses))
    bots = newGeneration(bots, fitnesses, 0.6)


bot_a = greedy_agent
bot_b = bots[0]
for i in range(5):
    seed = random.randint(1,100)
    score_a, score_b = run_episode(bot_a, bot_b, seed=seed, render=render)
    print(f"Score: {score_a}-{score_b} | Seed: {seed}")

