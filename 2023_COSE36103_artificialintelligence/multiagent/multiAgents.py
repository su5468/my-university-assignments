# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        newGhostPositions = successorGameState.getGhostPositions()
        newCapsulePositions = successorGameState.getCapsules()
        currentScaredTimes = [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]

        "*** YOUR CODE HERE ***"
        # print("start", successorGameState, newPos, newFood.asList(), newGhostStates, newGhostPositions, newScaredTimes, sep="\n")

        import math

        def frac(val1, val2=1):
            if val1 == val2 == 0:
                return 1
            if val1 == 0:
                return float('inf')
            return val2 / val1
        
        f = []
        w = []

        foodDist = []
        for food in newFood.asList():
            foodDist.append(manhattanDistance(newPos, food))

        ghostDist = []
        for ghost in newGhostPositions:
            ghostDist.append(manhattanDistance(newPos, ghost))

        capsuleDist = []
        for capsule in newCapsulePositions:
            capsuleDist.append(manhattanDistance(newPos, capsule))

        # 0. reciprocal of average distance to food
        f.append(frac(sum(foodDist), len(foodDist)))
        w.append(0.00001)

        # 1. reciprocal of nearest food distance
        f.append(frac(min(foodDist if foodDist else [0])))
        w.append(0.01)

        # 2. reciprocal of the number of foods
        f.append(frac(len(newFood.asList())))
        w.append(100)

        # 3. distance to nearest ghost
        nearGhost = min(ghostDist)
        nearGhostIndex = ghostDist.index(nearGhost)
        f.append(math.log(nearGhost, 100) if nearGhost else 0)
        w.append(0.001)

        # 4. if distance to nearest ghost is too near
        f.append(0 if nearGhost <= 2 else 1)
        w.append(100)

        # 5. reciprocal of distance to nearest capsule
        f.append(frac(min(capsuleDist if capsuleDist else [float("inf")])))
        w.append(0.01)

        # 6. reciprocal of the number of capsules
        f.append(frac(len(newCapsulePositions)) if newCapsulePositions else 10)
        w.append(100)

        # 7. score
        f.append(successorGameState.getScore())
        w.append(1)

        if currentScaredTimes[nearGhostIndex]:
            w[3] = -0.1
            w[4] = -100

        # print(action, sum([e * w[i] for i, e in enumerate(f)]))

        # return successorGameState.getScore()
        return sum([e * w[i] for i, e in enumerate(f)])

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def get_value(state, i, maxAgentNumber, remain):
            """
            recursive function that gets min/max value respectively.
            state is current state.
            i is index of current agent.
            maxAgentNumber is the number of agents.
            remain is the remaining depth of the tree.
            """
            if not state.getLegalActions(i) or (not remain and i == 0): # if leaf node
                return self.evaluationFunction(state), "_"              # return value of node
            action = "Stop"                                             # initialize action
            if i == 0:                                                  # if pacman
                func = lambda x, y: x < y                               # func determine min or max
                v = -float("inf")
                newRemain = remain - 1                                  # decrease remain tree depth
            else:                                                       # if ghost
                func = lambda x, y: x > y                               # same as above
                v = float("inf")
                newRemain = remain                                      # but don't decrease depth
            for nextAction in state.getLegalActions(i):                 # for successor in state
                successor = state.generateSuccessor(i, nextAction)
                tempV, _ = get_value(successor, (i + 1) % maxAgentNumber, maxAgentNumber, newRemain)
                if func(v, tempV):                                      # if value is smaller/larger
                    v = tempV                                           # change value and action
                    action = nextAction
            return v, action
        
        return get_value(gameState, 0, gameState.getNumAgents(), self.depth)[1] # returns action

        # util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def get_value(state, i, maxAgentNumber, remain, alpha, beta):
            """
            just added two args(alpha, beta) and several lines to minimax version.
            """
            if not state.getLegalActions(i) or (not remain and i == 0): # if leaf node
                return self.evaluationFunction(state), "_"              # return value of node
            action = "Stop"                                             # initialize action
            if i == 0:                                                  # if pacman
                func = lambda x, y: x < y                               # func determine min or max
                v = -float("inf")
                newRemain = remain - 1                                  # decrease remain tree depth
            else:                                                       # if ghost
                func = lambda x, y: x > y                               # same as above
                v = float("inf")
                newRemain = remain                                      # but don't decrease depth
            for nextAction in state.getLegalActions(i):                 # for successor in state
                successor = state.generateSuccessor(i, nextAction)
                tempV, _ = get_value(successor, (i + 1) % maxAgentNumber, maxAgentNumber, newRemain, alpha, beta)
                if func(v, tempV):                                      # if value is smaller/larger
                    v = tempV                                           # change value and action
                    action = nextAction
                if func(beta if i == 0 else alpha, v):                  # added from here
                    return v, action
                if i == 0:
                    alpha = max(alpha, v)
                else:
                    beta = min(beta, v)                                 # to here
            return v, action
        
        return get_value(gameState, 0, gameState.getNumAgents(), self.depth, -float("inf"), float("inf"))[1] # returns action
    
        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
