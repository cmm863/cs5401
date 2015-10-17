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

# Initialize variables
parents = list()
children = list()

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
for i in range(config_data["num children"]):
  children.append(SAT(equation.num_variables))

for child in children:
  child.setFitness(equation)

# Parent Selection
## Uniform Random
for i in range(config_data["num parents"]):
  selection = random.randint(0, len(children) - 1)
  parents.append(children[selection])
  children.pop(selection)

# Recombination
## Simple Arithmetic Recombination
children = list()
for i in range(config_data["num children"]):
  parent_one = parent_two = None
  recombination_variables = list()
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
plus_pool = children + parents
print(len(plus_pool))