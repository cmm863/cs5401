__author__ = 'connor'
import random
import operator
from sat import SAT


class Initialization():
    @staticmethod
    def uniform_random(equation, pop_size):
        pop_set = set()
        while len(pop_set) < pop_size:
            pop_set.add(SAT(equation.num_variables))
        return pop_set


class ParentSelection():
    @staticmethod
    def uniform_random(population, num_parents):
        pop_list = list(population)
        return [pop_list.pop(random.randint(0, len(pop_list) - 1)) for x in range(num_parents)]

    @staticmethod
    def tournament(population, num_parents, k):
        parents = set()
        pop_list = list(population)
        while len(parents) < num_parents:
            tournament_group = []
            for j in range(k):
                tournament_group.append(pop_list[random.randint(0, len(pop_list) - 1)])
            parents.add(sorted(tournament_group, key=operator.attrgetter("fitness"))[k - 1])
        return parents

    @staticmethod
    def fitness_proportional(population, num_parents):
        list_pop = list(population)
        fitness_sum = 0.0
        prob_sum = 0.0
        parents = set()
        for i in population:
            fitness_sum += i.fitness
        for i in population:
            prob = i.fitness / fitness_sum
            i.probability = prob_sum + prob
            prob_sum += prob
        while len(parents) < num_parents:
            selection_prob = random.random()
            for i in range(len(list_pop)):
                if list_pop[i].probability > selection_prob:
                    parents.add(list_pop[i-1])
                    break
        return parents


class Recombination():
    @staticmethod
    def uniform_crossover(mating_pool, num_children):
        if num_children % 2:
            print("Num children not even")
            return
        mating_list = list(mating_pool)
        children = set()
        pool_size = len(mating_list)
        variable_length = mating_list[0].num_variables
        while len(children) < num_children:
            parent_one = parent_two = None
            child_one = []
            child_two = []
            while parent_one == parent_two:
                parent_one = mating_list[random.randint(0, pool_size - 1)]
                parent_two = mating_list[random.randint(0, pool_size - 1)]
            for i in range(variable_length):
                inheritance_factor = random.randint(0, 1)
                if inheritance_factor == 1:
                    child_one.append(parent_one.variables[i])
                    child_two.append(parent_two.variables[i])
                else:
                    child_one.append(parent_two.variables[i])
                    child_two.append(parent_one.variables[i])
            children.add(SAT(variable_length, child_one))
            children.add(SAT(variable_length, child_two))
        return children


class Mutation():
    @staticmethod
    def bitwise(mating_pool, num_children, pm):  # pm is probability of mutation
        children = set()
        pool_size = len(mating_pool)
        mating_list = list(mating_pool)
        variable_length = mating_list[0].num_variables
        while len(children) < num_children:
            parent = mating_list[random.randint(0, pool_size - 1)]
            child = []
            for i in range(variable_length):
                if random.random() <= pm:
                    if not parent.variables[i]:
                        child.append(1)
                    else:
                        child.append(0)
                else:
                    child.append(parent.variables[i])
            children.add(SAT(variable_length, child))
        return children


class SurvivorSelection():
    @staticmethod
    def uniform_random(population, num_survivors):
        return [population.pop(random.randint(0, len(population) - 1)) for x in range(num_survivors)]

    @staticmethod
    def truncation(population, num_survivors):
        pop_list = list(population)
        return sorted(pop_list, key=operator.attrgetter("fitness"))[(len(pop_list)-num_survivors):]

    @staticmethod
    def tournament(population, num_survivors, k):
        pop_list = list(population)
        survivors = set()
        for i in range(num_survivors):
            tournament_group = []
            for j in range(k):
                tournament_group.append(pop_list.pop(random.randint(0, len(pop_list) - 1)))
            tournament_group = sorted(tournament_group, key=operator.attrgetter("fitness"))
            survivors.add(tournament_group.pop(k - 1))
            pop_list.extend(tournament_group)
        return survivors