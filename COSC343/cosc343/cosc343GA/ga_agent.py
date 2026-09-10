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


def manhattan_distance(pos_a, pos_b):
    """Manhattan (grid) distance between two (row, col) positions."""
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

def find_closest(pos, options):
    least_distance = float("inf")
    goal = pos
    for option in options:
        distance = manhattan_distance(pos, option)
        if distance < least_distance:
            least_distance = distance
            goal = option

    return goal, least_distance


def evalFitness(population, opponent, seeds):
    fitnesses = []

    for agent in population:
        deliveries, pickups, steps_to_package, steps_to_dispatch, invalid_actions = 0,0,0,0,0

        for seed in seeds:
            env = WarehouseEnv(seed=seed)
            states = env.reset()
            done   = False
            while not done:
                old_position = states[0]["position"]
                was_carrying = states[0]["carrying"]

                closest_package, package_distance = find_closest(states[0]["position"], states[0]["packages"])
                closest_dispatch, dispatch_distance = find_closest(states[0]["position"], states[0]["dispatch_stations"])

                # Choose Actions
                agent_action = agent(states[0])
                actions = {0: agent_action, 1: opponent(states[1])}

                # Did it try to pick up when it couldnt?
                if agent_action == 4:
                    if was_carrying:
                        invalid_actions += 1
                    elif states[0]["position"] not in states[0]["packages"]:
                        invalid_actions += 1

                # Did it try to dispatch when it couldnt?
                if agent_action == 5:
                    if not was_carrying:
                        invalid_actions += 1
                    elif states[0]["position"] not in states[0]["dispatch_stations"]:
                        invalid_actions += 1

                states, _, done, info = env.step(actions)

                # Did it pick something up?
                if not was_carrying and states[0]["carrying"]:
                    pickups += 1

                # Did it move towards a package?
                if not was_carrying and states[0]["packages"]:
                    if manhattan_distance(states[0]["position"], closest_package) < package_distance:
                        steps_to_package += 1
                    elif manhattan_distance(states[0]["position"], closest_package) > package_distance:
                        steps_to_package -= 1

                # Did it move towards a dispatch?
                if was_carrying:
                    if manhattan_distance(states[0]["position"], closest_dispatch) < dispatch_distance:
                        steps_to_dispatch += 1
                    elif manhattan_distance(states[0]["position"], closest_dispatch) > dispatch_distance:
                        steps_to_dispatch -= 1

                if agent_action in [0, 1, 2, 3]:
                    if states[0]["position"] == old_position:
                        invalid_actions += 1

    

            deliveries += info["scores"][0]

        fitness = (
            2 * pickups +
            20 * deliveries +
            0.1 * steps_to_package +
            0.15 * steps_to_dispatch -
            0.1 * invalid_actions
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

    features = [
        (0, 1),       # Self X
        (1, 2),       # Self Y
        (2, 3),       # Self carrying

        (3, 12),      # Opponents

        (12, 112),    # Packages grid

        (112, 212),   # Dispatch grid

        (212, 213),   # Crowding
        (213, 214),   # On package
        (214, 215),   # On dispatch
    ]

    # Crossover on movment habits per feature across all movment actions 0-3
    for feature in features:
        parent = random.choice((mum, dad))
        weights[0:4, feature[0]:feature[1]] = parent.weights[0:4, feature[0]:feature[1]]
    biases[0:4] = parent.biases[0:4]

    # Pick up Behaviour:
    for feature in features:
        parent = random.choice((mum, dad))
        weights[4:5, feature[0]:feature[1]] = parent.weights[4:5, feature[0]:feature[1]]
    parent = random.choice((mum, dad))
    biases[4] = parent.biases[4]

    # Dispatch Behaviour:
    for feature in features:
        parent = random.choice((mum, dad))
        weights[5:6, feature[0]:feature[1]] = parent.weights[5:6, feature[0]:feature[1]]
    parent = random.choice((mum, dad))
    biases[5] = parent.biases[5]

    # Mutation
    for action in range(6):
        # Mutate Weights
        for weight in range(215):
            if random.random() < mutate:
                weights[action,weight] += random.uniform(-0.05, 0.05)
        # Mutate Biases
        if random.random() < mutate:
            biases[action] += random.uniform(-0.05, 0.05)

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

        