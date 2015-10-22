__author__ = 'connor'
import random
from sat import SAT


class Initialization():
    @staticmethod
    def uniform_random(equation, num_parents):
        return [SAT(equation.num_variables) for x in range(num_parents)]


class ParentSelection():
    @staticmethod
    def uniform_random(population, num_parents):
        return [population.pop(random.randint(0, len(population) - 1)) for x in range(num_parents)]