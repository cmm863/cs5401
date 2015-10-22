__author__ = 'connor'
import random


def uniform_random(population, num_parents):
    return [population.pop(random.randint(0, len(population) - 1)) for x in range(num_parents)]