# Written by Connor McBride
# Evolutionary Algorithms Assignment 1c
# Self Adaptive EAs with Restarts

# Library
import sys  # For command line arguments
import json  # For config file parsing
import math  # For crossover fraction

# Local
from cnf import CNF
from implementations import *


def generateAverageFitness(population):
    pop_size = len(population)
    total_fitness = 0
    for i in range(pop_size):
        total_fitness += population[i].fitness
    return total_fitness / pop_size

# Initialize variables
population = set()
children = set()
fitnesses = []
mating_pool = set()
mutation_pool = set()
recombination_pool = set()
recombination_variables = []
mutation_variables = []
terminate = False

# Get command line arguments
if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    config_file = "config/default.cfg"

# Load config file
with open(config_file) as temp_config:
    config_data = json.load(temp_config)

# Create CNF instance
equation = CNF(config_data["cnf file"])

# Initialization
# # Uniform Random
population = Initialization.uniform_random(equation, config_data["mu"])

# Set Fitness
for individual in population:
    individual.setFitness(equation)

for evaluation in range(config_data["evaluations"]):
    children.clear()
    if terminate:
        break

    # Parent Selection
    while len(children) < config_data["lambda"]:
        if config_data["parent select"] == "uni rand":
            mating_pool = ParentSelection.uniform_random(population, 2)
        elif config_data["parent select"] == "tourn":
            mating_pool = ParentSelection.tournament(population, 2, config_data["parent t size"])
        elif config_data["parent select"] == "fit prop":
            mating_pool = ParentSelection.fitness_proportional(population, 2)
        else:
            print("For parent select, select either uni rand, tourn, or fit prop")
            break
        children_temp = Recombination.uniform_crossover(mating_pool)
        for child in children_temp:
            children.add(Mutation.bitwise(child, 1.0/equation.num_variables))

    # Set Fitness
    for child in children:
        child.setFitness(equation)

    # Survival Strategy
    ## Plus
    if config_data["survival strat"] == "plus":
        population = children.union(population)
    elif config_data["survival strat"] == "comma":
        population = children
    else:
        print("For survival strat, select either plus or comma")
        break

    # Survival Selection
    ## Uniform Random
    if config_data["survival select"] == "trunc":
        population = set(SurvivorSelection.truncation(population, config_data["mu"]))
    elif config_data["survival select"] == "uni rand":
        population = set(SurvivorSelection.uniform_random(population, config_data["mu"]))
    elif config_data["survival select"] == "tourn":
        population = set(SurvivorSelection.tournament(population, config_data["mu"], config_data["survival t size"]))
    else:
        print("For survival select, select either trunc, uni rand")
    fronts = MultiObjective.pareto(population)
    fitnesses.append(generateAverageFitness(list(population)))
    print(fitnesses[-1])
    terminate = True
    # Termination Condition
    num_fitnesses = len(fitnesses)
    if num_fitnesses > config_data["n"]:
        n = config_data["n"]
        for i in range(n):
            if fitnesses[num_fitnesses - i - 1] != fitnesses[num_fitnesses - 1]:
                break
            elif i == (n - 1):
                terminate = True






