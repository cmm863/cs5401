import random
from cnf import CNF


class SAT:
    def __init__(self, num_variables, variables=None):
        self.num_variables = num_variables
        self.variables = list()
        self.real_var_count = 0
        if variables is not None:
            self.variables = variables
        else:
            for i in range(self.num_variables):
                var = random.randint(0, 2)
                if var < 2:
                    self.variables.append(var)
                else:
                    self.variables.append('x')
        for var in self.variables:
            if var is not 'x':
                self.real_var_count += 1

    def prettyPrint(self):
        return_string = ""
        for i in range(self.num_variables):
            if self.variables[i] == 1:
                return_string += " " + str(i + 1)
            elif self.variables[i] == 0:
                return_string += " -" + str(i + 1)
            else: # Don't care
                pass
        return return_string

    def setFitness(self, cnf_equation):
        current_fitness = 0
        for clause in cnf_equation.clauses:
            clause_sum = 0

            for var in clause:
                if var == '0':
                    break
                # Reset index
                index = 0

                # If NOT
                if var[0] == '-':
                    index = int(var[1:]) - 1
                    if self.variables[index] == 'x':
                        continue
                    clause_sum += int(not self.variables[index])
                else:
                    index = int(var) - 1
                    if self.variables[index] == 'x':
                        continue
                    clause_sum += int(self.variables[index])

            if clause_sum > 0:
                current_fitness += 1

        self.fitness = current_fitness

    def dominates(self, sat_solution):
        return self.fitness >= sat_solution.fitness and self.real_var_count <= sat_solution.real_var_count