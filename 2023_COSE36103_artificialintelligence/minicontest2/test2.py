# baselineTeam.py
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


from captureAgents import CaptureAgent
import distanceCalculator
import random
import time
import util
import sys
from game import Directions
import game
from util import nearestPoint
import numpy

#################
# Team creation #
#################


def createTeam(firstIndex, secondIndex, isRed,
               first='MinMaxAgent', second='MinMaxAgent'):
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########


class MinMaxAgent(CaptureAgent):

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

    self.agents = [self.index] + self.getOpponents(gameState)
    self.depth = 2

  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)

    foodLeft = len(self.getFood(gameState).asList())

    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start, pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    successors = [gameState.generateSuccessor(self.index, action) for action in actions]
    values = [self.getValue(successor, self.depth, 1) for successor in successors]

    return actions[values.index(max(values))]


  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def getValue(self, successor, depth, index):
    if self.agents[index] == self.index:
      depth -= 1

    if depth == 0 or successor.isOver():
      return self.evaluate(successor)

    if self.agents[index] == self.index:
      return self.maxValue(successor, depth, index)
    else:
      return self.expValue(successor, depth, index)

  def maxValue(self, successor, depth, index):
    actions = successor.getLegalActions(self.agents[index])
    nextSuccessors = [successor.generateSuccessor(self.agents[index], action) for action in actions]
    nextIndex = (index + 1) % len(self.agents)
    values = [self.getValue(nextSuccessor, depth, nextIndex) for nextSuccessor in nextSuccessors]

    return max(values)

  def expValue(self, successor, depth, index):
    actions = successor.getLegalActions(self.agents[index])
    nextSuccessors = [successor.generateSuccessor(self.agents[index], action) for action in actions]
    nextIndex = (index + 1) % len(self.agents)
    values = [self.getValue(nextSuccessor, depth, nextIndex) for nextSuccessor in nextSuccessors]

    normalize = [1 / len(actions) for action in actions]
    return sum(n * v for n, v in zip(normalize, values))

  def evaluate(self, gameState):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState)
    return features * weights

  def getFeatures(self, gameState):
    features = util.Counter()
    features['curScore'] = gameState.getScore()

    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()

    features['isPacman'] = 0
    if myState.isPacman:
      features['isPacman'] = 1

    foodList = self.getFood(gameState).asList()
    features['successorScore'] = -len(foodList)

    if len(foodList) > 0:
      minDistance = min([self.getMazeDistance(myPos, food)
                         for food in foodList])
      features['distanceToFood'] = minDistance

    capsuleList = self.getCapsules(gameState)
    features['numCapsulesLeft'] = len(capsuleList)
    if features['numCapsulesLeft'] > 0:
      minDistance = min([self.getMazeDistance(myPos, food)
                         for food in capsuleList])
      features['distanceToCapsule'] = minDistance

    foodCarried = myState.numCarrying
    halfway = self.getFood(gameState).width // 2
    x, y = myPos
    if myState.isPacman and x > halfway:
        features['depositFood'] = foodCarried * abs(x - (halfway + 1))
    else:
        features['depositFood'] = foodCarried * abs(x - halfway)

    features['enemyGhosts'] = 0
    features['numScaredGhosts'] = 0
    features['enemyPacman'] = 0
    features['numEatPacman'] = 0

    enemyIndexList = self.getOpponents(gameState)
    enemyList = [gameState.getAgentState(index) for index in enemyIndexList]
    for enemy in enemyList:
        if not enemy.isPacman:
            if enemy.scaredTimer > 0:
                features['enemyGhosts'] += self.getMazeDistance(
                    myPos, enemy.getPosition())
                features['numScaredGhosts'] += 1
            else:
                features['enemyGhosts'] -= self.getMazeDistance(
                    myPos, enemy.getPosition())
        else:
            features['enemyPacman'] += self.getMazeDistance(
                myPos, enemy.getPosition())
            features['numEatPacman'] += 1
            if myState.scaredTimer > 0:
                features['enemyPacman'] = -features['enemyPacman']

    return features

  def getWeights(self, gameState):
    return {'isPacman': 0, 'successorScore': 10000, 'distanceToFood': -100,
            'distanceToCapsule': -120, 'numCapsulesLeft': -15000,
            'depositFood': -5, 'numScaredGhosts': -70, 'enemyGhosts': -105,
            'numEatPacman': -190, 'enemyPacman': -100, 'curScore': 1}