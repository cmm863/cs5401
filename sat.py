import random
from cnf import CNF

class SAT:
  variables = list()
  fitness = None

  def __init__(self, num_variables, variables = None):
    self.num_variables = num_variables

    if(variables is not None):
      self.variables = variables
    else:
      for i in range(self.num_variables):
        self.variables.append(random.randint(0, 1))

  def prettyPrint(self):
    return_string = ""
    for i in range(self.num_variables):
      if(self.variables[i] == 1):
        return_string += " " + str(i + 1)
      else:
        return_string += " -" + str(i + 1)
    return return_string

  def setFitness(self, cnf_equation):
    current_fitness = 0
    for clause in cnf_equation.clauses:
      clause_sum = 0

      for var in clause:
        if(var == '0'):
          break
        # Reset index
        index = 0

        # If NOT
        if(var[0] == '-'):
          index = int(var[1:]) - 1
          clause_sum += int(not self.variables[index])
        else:
          index = int(var) - 1
          clause_sum += int(self.variables[index])

      if(clause_sum > 0):
        current_fitness += 1

    self.fitness = current_fitness