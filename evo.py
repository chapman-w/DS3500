'''
File: evo.py
Author: wesleychapman
Description: A concise evolutionary computing framework for solving  multi-objective optimization problems.
'''

import random as rnd
import copy # doing deep copies of solutions when generating offspring
from functools import reduce # for discarding dominated (bad) solutions

class Evo:

    def __init__(self):
        """ framework constructor """
        self.pop = {} # population of solutions: evaluation -> solution
        self.fitness = {} # objectives: name -> objective function (f)
        self.agents = {} # agents: name -> (operator/function, num_solutions)

    def add_objective(self, name, f):
        """ register a new objective function for evaluating solutions"""
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ register a new agent that works on k input values"""
        self.agents[name] = (op, k)


    def get_random_solutions(self, k=1):
        """ picks k random solutions from population and
        returns them as a list of deep copies"""
        if len(self.op) == 0: # no solutions - this shouldn't happen
            return []
        else:
            solutions = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(solutions)) for _ in range(k)]


    def add_solution(self, solution):
        ''' adds the solution to the current population, added solutions
        are evaluating with respect to each registered objective'''

        # create the evaluation key
        # key: ( (objname1, objvalue1), (objname2, objvalue2), (objname3, objvalue3), ... )
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
        # add to the dictionary
        self.pop[eval] = sol


    def run_agent(self, name):
        """ invoking a named agent against the current population"""
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    @staticmethod
    def _dominates(p, q):
        """ p = evaluation of solution: ((obj1, score1), (obj2, score2), ... )"""
        pscores = [score for _, score in p]
        qscores = [score for _, score in q]
        score_diffs = list(map(lambda x, y: y - x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p, q)}

    def remove_dominated(self):
        """ remove solutions from pop that are dominated (worse) compared
        to other existing solutions. this is what provides selective pressure
        driving the pop towards the pareto optimal tradeoff curve"""
        nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    def evolve(self, n=1, dom=100, status=1000):
        ''' run the framework (start evolving solutions)
        n = # of agent invocations (# of generations)'''

        agent_names = list(self.agents.keys())
        for i in range(n):
            pick = rnd.choice(agent_names)  # pick an agent to run
            self.run_agent(pick)
            if i % dom == 0:
                self.remove_dominated()
            if i % status == 0:
                self.remove_dominated()
                print("Iteration: ", i)
                print("Pop size: ", len(self.pop))
                print(self)

        self.remove_dominated()

        def __str__(self):
            """ Output the solutions in the population """
            rslt = ""
            for eval, sol in self.pop.items():
                rslt += str(dict(eval)) + ":\t" + str(sol) + "\n"
            return rslt










