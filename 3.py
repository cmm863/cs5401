# Written by Connor McBride
# Evolutionary Algorithms Assignment 1c
# Self Adaptive EAs with Restarts

# Library
import sys    # For command line arguments
import json   # For config file parsing

# Local
from cnf import CNF   
from sat import SAT

test_cnf = CNF("cnfs/1.cnf")
test_sat = SAT(test_cnf.num_variables)
print(test_sat.variables)
test_sat.setFitness(test_cnf)
print(test_sat.fitness)