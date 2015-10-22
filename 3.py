# Written by Connor McBride
# Evolutionary Algorithms Assignment 1c
# Self Adaptive EAs with Restarts

# Library
import sys  # For command line arguments
import json  # For config file parsing
import random  # For process

# Local
from cnf import CNF
from sat import SAT
from implementations import *


def generateAverageFitness(population):
    pop_size = len(population)
    total_fitness = 0
    for i in range(pop_size):
        total_fitness += population[i].fitness
    return total_fitness / pop_size

# Initialize variables
population = []
parents = []
children = []
fitnesses = []
mating_pool = []
mutation_pool = []
recombination_pool = []
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
population.extend(Initialization.uniform_random(equation, config_data["pop size"]))

for evaluation in range(config_data["evaluations"]):
    if terminate:
        break

    # Parent Selection
    ## Uniform Random
    mating_pool = ParentSelection.uniform_random(population, config_data["num parents"])

    # Recombination
    ## Uniform Crossover
    children = Recombination.uniform_crossover(mating_pool, 2)
    # Mutation
    for parent in mutation_pool:
        mutation_variables = []
        for j in range(equation.num_variables):
            if random.randint(0, equation.num_variables) == equation.num_variables:
                if parent.variables[j] == 0:
                    mutation_variables.append(1)
                else:
                    mutation_variables.append(0)
            else:
                mutation_variables.append(parent.variables[j])
        children.append(SAT(equation.num_variables, mutation_variables))

    # Survival Strategy
    ## Plus
    if config_data["survival strat"] == "plus":
        population = children + parents
    elif config_data["survival strat"] == "comma":
        population = children
    else:
        #print("For survival strat, select either plus or comma")
        break

    for individual in population:
        individual.setFitness(equation)

    # Survival Selection
    parents[:] = []
    ## Uniform Random
    for i in range(config_data["num parents"]):
        selection = random.randint(0, len(population) - 1)
        parents.append(population[selection])
        population.pop(selection)
    fitnesses.append(generateAverageFitness(parents))
    #print(fitnesses[-1])

    # Termination Condition
    num_fitnesses = len(fitnesses)
    if num_fitnesses > config_data["n"]:
        n = config_data["n"]
        for i in range(n):
            if fitnesses[num_fitnesses - i - 1] != fitnesses[num_fitnesses - 1]:
                break
            elif i == (n - 1):
                terminate = True






