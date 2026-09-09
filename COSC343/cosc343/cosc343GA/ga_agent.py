import random
import numpy as np
from feature_encoder import encode_state
from warehouse_env import run_episode, WarehouseEnv


class GAAgent:

    def __init__(self, model=None):
        if model == None:
            self.weights = np.random.uniform(-0.1, 0.1, size=(6, 215))
            self.biases = np.random.uniform(-0.1, 0.1, size=6)

        else:
            self.weights = np.asarray(model["weights"])
            self.biases = np.asarray(model["biases"])

    def __call__(self, state):
        features = encode_state(state)
        action_scores = np.dot(self.weights, features) + self.biases
        return int(np.argmax(action_scores))



def evalFitness(population, opponent, seeds):
    fitnesses = []

    for agent in population:
        deliveries, pickups, steps_right_direction = 0,0,0

        for seed in seeds:
            env = WarehouseEnv(seed=seed)
            states = env.reset()
            done   = False
            while not done:
                was_carrying = states[0]["carrying"]

                actions = {0: agent(states[0]), 1: opponent(states[1])}
                states, _, done, info = env.step(actions)

                # Did it pick something up?
                if not was_carrying and states[0]["carrying"]:
                    pickups += 1
                

            deliveries += info["scores"][0]

        fitness = (
            2 * pickups +
            10 * deliveries
        )

        fitnesses.append(fitness)

    return fitnesses

def random_parent(parents):
    parent = parents[random.randint(0,len(parents)-1)][0]
    return parent

def weighted_parent(parents):
    fitness_values = []
    weights = []
    
    for parent in parents:
        fitness_values.append(parent[1])

    lowest_fitness = min(fitness_values)
    
    for parent in parents:
        weight = parent[1] - lowest_fitness + 1
        weights.append(weight)

    parent = random.choices(parents, weights=weights)[0][0]

    return parent

def make_baby(mum, dad, mutate): # lmao
    weights = np.empty((6, 215))
    biases = np.empty(6)

    for action in range(6): # Crossover
        if random.randint(0, 1) == 0:
            action_weights = mum.weights[action].copy()
            action_bias = mum.biases[action]
        else:
            action_weights = dad.weights[action].copy()
            action_bias = dad.biases[action]

        for feature in range(215): # Weight mutation
            if random.random() < mutate:
                action_weights[feature] += random.uniform(-0.05, 0.05)

        if random.random() < mutate: # Bias mutation
            action_bias += random.uniform(-0.05, 0.05)

        weights[action] = action_weights
        biases[action] = action_bias

    model = {'weights': weights, 'biases': biases}

    child = GAAgent(model)
    return child


def newGeneration(population, fitnesses, mutation_rate):
    static_poulation = population.copy()
    static_fitnesses = fitnesses.copy()
    parents = []
    next_generation = []
    parents_cutoff = 2 # Fraction of parents used for next generation
    mutate =  mutation_rate # Chance to mutate
    
    next_generation.append(population[fitnesses.index(max(fitnesses))]) # Keep a single elite in the next gen

    for i in range(len(population) // parents_cutoff):
        fitness = max(static_fitnesses)
        parent = static_poulation[static_fitnesses.index(fitness)]
        parents.append([parent, fitness])
        static_fitnesses.remove(fitness)
        static_poulation.remove(parent)

    for i in range(len(population) - 1):
        mum = weighted_parent(parents)
        dad = weighted_parent(parents)
        while mum == dad: # avoiding computer incest
            dad = weighted_parent(parents)

        child = make_baby(mum, dad, mutate)
        next_generation.append(child)

    return next_generation

        