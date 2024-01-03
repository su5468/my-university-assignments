# myAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
import search


"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        global going, gopath, goidx

        problem = AnyFoodSearchProblem(state, self.index)
        
        if going[self.index] == (-1, -1)\
            or not problem.food[going[self.index][0]][going[self.index][1]]:
            self.bfs(problem, self.index)
            goidx[self.index] = -1
        goidx[self.index] += 1
        return gopath[self.index][goidx[self.index]]

    def bfs(self, problem, index):
        global going, gopath
        fringe = util.Queue()
        current = (problem.getStartState(), [], 0)
        fringe.push(current)
        closed = set()

        while not fringe.isEmpty():
            node, path, depth = fringe.pop()
            if problem.isGoalState(node):
                going[index] = node
                gopath[index] = path
                return
            if not node in closed:
                closed.add(node)
                for coord, move, cost in problem.getSuccessors(node):
                    fringe.push((coord, path + [move], depth + 1))
        going[index] = problem.getStartState()
        gopath[index] = ['Stop']

    # below are my some attempts. you can ignore them.

    # def iterative_deepening(self, problem, index):
    #     global going, gopath
    #     fringe = util.Stack()
    #     current = (problem.getStartState(), [], 0)
    #     fringe.push(current)
    #     closed = set()
    #     candidate = []
    #     fullDepth = 0
    #     while 1:
    #         fullDepth += 1
    #         fringe.list.extend(candidate)
    #         candidate = []
    #         while not fringe.isEmpty():
    #             node, path, depth = fringe.pop()
    #             if problem.isGoalState(node):
    #                 going[index] = node
    #                 gopath[index] = path
    #                 return
    #             if not node in closed:
    #                 closed.add(node)
    #                 if depth >= fullDepth:
    #                     for coord, move, cost in problem.getSuccessors(node):
    #                         candidate.append((coord, path + [move], depth + 1))
    #                     continue
    #                 for coord, move, cost in problem.getSuccessors(node):
    #                     fringe.push((coord, path + [move], depth + 1))
    #         if not candidate:
    #             break
    #     going[index] = problem.getStartState()
    #     gopath[index] = ['Stop']

    # def heuristic(self, state, problem):
    #     return 0

    # def astar(self, problem, index, heuristic):
    #     global going, gopath
    #     fringe = util.PriorityQueue()
    #     counts = util.Counter()
    #     current = (problem.getStartState(), [])    
    #     counts[str(current[0])] += heuristic(current[0], problem)
    #     fringe.push(current, counts[str(current[0])])
    #     closed = set()
        
    #     while not fringe.isEmpty():
    #         node, path = fringe.pop()
    #         if problem.isGoalState(node):
    #             going[index] = node
    #             gopath[index] = path
    #             return
    #         if not node in closed:
    #             closed.add(node)
    #             for coord, move, cost in problem.getSuccessors(node):
    #                 newpath = path + [move]
    #                 counts[str(coord)] = problem.getCostOfActions(newpath)
    #                 counts[str(coord)] += heuristic(coord, problem)
    #                 fringe.push((coord, newpath), counts[str(coord)]) 
    #     going[index] = problem.getStartState()
    #     gopath[index] = ['Stop']

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE"
        global going, gopath, goidx
        if 'going' not in globals():
            going = []
            gopath = []
            goidx = []
        going.append((-1, -1))
        gopath.append(['Stop'])
        goidx.append(-1)
        
        # raise NotImplementedError()

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"

        pacmanCurrent = [problem.getStartState(), [], 0]
        visitedPosition = set()
        # visitedPosition.add(problem.getStartState())
        fringe = util.PriorityQueue()
        fringe.push(pacmanCurrent, pacmanCurrent[2])
        while not fringe.isEmpty():
            pacmanCurrent = fringe.pop()
            if pacmanCurrent[0] in visitedPosition:
                continue
            else:
                visitedPosition.add(pacmanCurrent[0])
            if problem.isGoalState(pacmanCurrent[0]):
                return pacmanCurrent[1]
            else:
                pacmanSuccessors = problem.getSuccessors(pacmanCurrent[0])
            Successor = []
            for item in pacmanSuccessors:  # item: [(x,y), 'direction', cost]
                if item[0] not in visitedPosition:
                    pacmanRoute = pacmanCurrent[1].copy()
                    pacmanRoute.append(item[1])
                    sumCost = pacmanCurrent[2]
                    Successor.append([item[0], pacmanRoute, sumCost + item[2]])
            for item in Successor:
                fringe.push(item, item[2])
        return pacmanCurrent[1]

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        if self.food[x][y] == True:
            return True
        return False

