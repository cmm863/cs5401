__author__ = 'connor'
import random
import operator
from sat import SAT


class Initialization():
    @staticmethod
    def uniform_random(equation, pop_size):
        return [SAT(equation.num_variables) for x in range(pop_size)]


class ParentSelection():
    @staticmethod
    def uniform_random(population, num_parents):
        return [population.pop(random.randint(0, len(population) - 1)) for x in range(num_parents)]


class Recombination():
    @staticmethod
    def uniform_crossover(mating_pool, num_children):
        if num_children % 2:
            print("Num children not even")
            return
        children = []
        pool_size = len(mating_pool)
        variable_length = mating_pool[0].num_variables
        while len(children) != num_children:
            parent_one = parent_two = None
            child_one = []
            child_two = []
            while parent_one == parent_two:
                parent_one = mating_pool[random.randint(0, pool_size - 1)]
                parent_two = mating_pool[random.randint(0, pool_size - 1)]
            for i in range(variable_length):
                inheritance_factor = random.randint(0, 1)
                if inheritance_factor == 1:
                    child_one.append(parent_one.variables[i])
                    child_two.append(parent_two.variables[i])
                else:
                    child_one.append(parent_two.variables[i])
                    child_two.append(parent_one.variables[i])
            children.extend([SAT(variable_length, child_one), SAT(variable_length, child_two)])
        return children


class Mutation():
    @staticmethod
    def bitwise(mating_pool, num_children, pm):  # pm is probability of mutation
        children = []
        pool_size = len(mating_pool)
        variable_length = mating_pool[0].num_variables
        while len(children) < num_children:
            parent = mating_pool[random.randint(0, pool_size - 1)]
            print(parent.variables)
            child = []
            for i in range(variable_length):
                if random.random() <= pm:
                    if not parent.variables[i]:
                        child.append(1)
                    else:
                        child.append(0)
                else:
                    child.append(parent.variables[i])
            print(child)
            children.extend([SAT(variable_length, child)])
        return children


class SurvivorSelection():
    @staticmethod
    def uniform_random(population, num_survivors):
        return [population.pop(random.randint(0, len(population) - 1)) for x in range(num_survivors)]

    @staticmethod
    def truncation(population, num_survivors):
        return sorted(population, key=operator.attrgetter("fitness"))[(len(population)-num_survivors):]