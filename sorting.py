'''
File: sorting.py
Description: Demonstrate how we can sort a list of numbers
using evolutionary computing WITHOUT implementing a sorting algorithm.
'''

import random as rnd
import evo

# an objective

def stepdowns(L):
    return sum([ x - y for x, y in zip(L, L[1:]) if y > x])

def sumratio(L):
    sz = len(L)


# an agent that works on ONE input solution - COPIED from the pop
def swapper(solutions):
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L


def main():

    # create the framework object
    E = evo.Evo()
    E.add_agent("swapper", swapper)
    E.add_objective("stepdowns", stepdowns)
    E.add_objective("sumratio", sumratio)

    # initialize with one random solution
    L = [rnd.randrange(1, 99) for _ in range(20)]
    E.add_solution(L)
    print(E)

    E.evolve(n=10000, dom=100, status=1000)
    print(E)

main()



