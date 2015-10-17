# Written by Connor McBride
# Evolutionary Algorithms Assignment 1c
# Self Adaptive EAs with Restarts

# Library
import sys    # For command line arguments
import json   # For config file parsing

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
for i in range(config_data["num parents"]):
  parents.append(SAT(equation.num_variables))

for parent in parents:
  parent.setFitness(equation)