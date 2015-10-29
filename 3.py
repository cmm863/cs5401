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


def generateAverageReal(population):
    pop_size = len(population)
    total_real = 0
    for i in range(pop_size):
        total_real += population[i].real_var_count
    return total_real / pop_size

# Initialize variables
population = set()
children = set()
fitnesses = []
previous_fronts = []
real_var_counts = []
mating_pool = set()
mutation_pool = set()
recombination_pool = set()
recombination_variables = []
mutation_variables = []
hall_of_fame_fronts = []
terminate = False

# Get command line arguments
if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    config_file = "config/default.cfg"

# Load config file
with open(config_file) as temp_config:
    config_data = json.load(temp_config)


result_log_name = config_file.replace("config/", "").replace(".cfg", "")
result_log = open("output/" + result_log_name + ".log", 'w+')
solution_log = open("output/" + result_log_name + ".sol", 'w+')
# Create CNF instance
equation = CNF(config_data["cnf file"])
for run in range(config_data["runs"]):
    result_log.write("Run " + str(run + 1) + "\n")
    print("Run " + str(run + 1))
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

        fronts = MultiObjective.pareto(population, config_data["true count"])
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

        fronts = MultiObjective.pareto(population, config_data["true count"])
        # Survival Selection
        ## Uniform Random
        if config_data["survival select"] == "trunc":
            population = set(SurvivorSelection.truncation(fronts, config_data["mu"]))
        elif config_data["survival select"] == "uni rand":
            population = set(SurvivorSelection.uniform_random(population, config_data["mu"]))
        elif config_data["survival select"] == "tourn":
            population = set(SurvivorSelection.tournament(population, config_data["mu"], config_data["survival t size"]))
        else:
            print("For survival select, select either trunc, uni rand")

        real_var_counts.append(generateAverageReal(list(population)))
        fitnesses.append(generateAverageFitness(list(population)))
        best_fitness = sorted(population, key=operator.attrgetter("fitness"), reverse=True)[0]
        best_real = sorted(population, key=operator.attrgetter("real_var_count"))[0]
        if config_data["true count"]:
            best_true = sorted(population, key=operator.attrgetter("true_percent"), reverse=True)[0]
            result_log.write(str(evaluation) + "\t" + str(fitnesses[-1]) + "\t" + str(real_var_counts[-1]) + "\t" + str(best_fitness.fitness) + "\t" + str(best_real.real_var_count) + "\t" + str(best_true.true_percent) + "\n")
        else:
            result_log.write(str(evaluation) + "\t" + str(fitnesses[-1]) + "\t" + str(real_var_counts[-1]) + "\t" + str(best_fitness.fitness) + "\t" + str(best_real.real_var_count) + "\n")

        # Termination Condition
        previous_fronts.append(fronts[0])
        num_fronts = len(previous_fronts)
        for front in previous_fronts:
            if front != fronts[0]:
                previous_fronts.remove(front)
        if len(previous_fronts) >= config_data["n"]:
            hall_of_fame_fronts.append(fronts[0])
            terminate = True
    terminate = False
    previous_fronts = []
    result_log.write("\n")

hof_comparisons = []
for i in range(len(hall_of_fame_fronts)):
    hof_comparisons.append([MultiObjective.compare_pareto_front(hall_of_fame_fronts[i], hall_of_fame_fronts), i], config_data["true count"])

best_front = hall_of_fame_fronts[sorted(hof_comparisons, key=operator.itemgetter(0), reverse=True)[0][1]]
solution_log.write("c " + config_data["cnf file"] + "\n")
solution_log.write("c solution num: " + str(len(best_front)) + "\n\n")

for solution in best_front:
    solution_log.write("c MAXSAT value: " + str(solution.fitness) + "\n")
    solution_log.write("c robustness: " + str(solution.real_var_count) + "\n")
    if config_data["true count"]:
        solution_log.write("c true percent: " + str(solution.true_percent) + "\n")
    solution_log.write("v " + solution.prettyPrint() + " 0\n\n")