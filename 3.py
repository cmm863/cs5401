# Written by Connor McBride
# Evolutionary Algorithms Assignment 1c
# Self Adaptive EAs with Restarts

# Library
import sys    # For command line arguments
import json   # For config file parsing
import random # For process

# Local
from cnf import CNF   
from sat import SAT

def generateAverageFitness(population):
  pop_size = len(population)
  total_fitness = 0
  for i in range(pop_size):
    total_fitness += population[i].fitness
  return total_fitness/pop_size

# Initialize variables
parents = []
children = []
fitnesses = []
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
## Uniform Random
for i in range(config_data["num parents"]):
  parents.append(SAT(equation.num_variables))

for evaluation in range(config_data["evaluations"]):
  if(terminate == True):
    break;
  # Recombination
  children[:] = []
  ## Simple Arithmetic Recombination
  for i in range(config_data["num children"]):
    parent_one = parent_two = None
    recombination_variables = list()

    # Parent Selection
    ## Uniform Random
    while(parent_one == parent_two):
      parent_one = parents[random.randint(0, config_data["num parents"] - 1)]
      parent_two = parents[random.randint(0, config_data["num parents"] - 1)]

    for j in range(equation.num_variables):
      if(parent_one.variables[j] == parent_two.variables[j]):
        recombination_variables.append(parent_one.variables[j])
      else:
        recombination_variables.append(random.randint(0, 1))
    children.append(SAT(equation.num_variables, recombination_variables))

  # Survival Strategy
  ## Plus
  if(config_data["survival strat"] == "plus"):
    population = children + parents
  elif(config_data["survival strat"] == "comma"):
    population = children
  else:
    print("For survival strat, select either plus or comma")
    break;

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
  print(fitnesses[-1])

  # Termination Condition
  num_fitnesses = len(fitnesses)
  if(num_fitnesses > config_data["n"]):
    n = config_data["n"]
    for i in range(n):
      if(fitnesses[num_fitnesses - i - 1] != fitnesses[num_fitnesses - 1]):
        break;
      elif(i == (n - 1)):
        terminate = True






