__author__ = 'connor'
from sat import SAT


def uniform_random(equation, num_parents):
    return [SAT(equation.num_variables) for x in range(num_parents)]

