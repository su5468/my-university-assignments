# myTeam.py
# ---------
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
import random, time, util
from game import Directions
import game
import numpy as np

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OpportunistAgent', second = 'OpportunistAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class OpportunistAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''
    # 벽 그리드, 아군 팀 색, 팀원의 인덱스, 마킹하는 적의 인덱스, 전선(경계, 아군 팀의 최전선) x 좌표, 전선의 좌표들, 방문 횟수 그리드
    self.walls = gameState.getWalls()
    self.teamColor = 'BLUE' if self.getTeam(gameState)[0] % 2 else 'RED'
    self.teamMate = (self.index + 2) % 4
    self.marking = (self.index + 1) % 4
    self.border_x = self.walls.width // 2 - 1 if self.teamColor == 'RED' else self.walls.width // 2
    self.borderList = [(self.border_x, y) for y in range(self.walls.height) if not self.walls[self.border_x][y]]
    self.visited = [[0 for _ in range(self.walls.height)] for _ in range(self.walls.width)]


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    # start = time.time()
    weights = self.getWeights()
    if gameState.getAgentState(self.teamMate).isPacman:
      weights = self.getDefWeights()
    elif gameState.getAgentState(self.index).isPacman:
      weights = self.getOffWeights()
    # 가장 최적의 행동을 결정한다
    # 같은 값을 가지는 행동이 여럿이면 랜덤으로 결정하긴 하는데,
    # 사실 엄밀히 말해서 Uniform Distribution은 아니다
    # 그래도 큰 상관은 없을 듯
    bestValue = -float('inf')
    bestAction = Directions.STOP
    for a in actions:
      if gameState.getAgentState(self.teamMate).isPacman:
        features = self.getDefFeatures(gameState, a)
      elif gameState.getAgentState(self.index).isPacman:
        features = self.getOffFeatures(gameState, a)
      else:
        features = self.getFeatures(gameState, a)
      value = np.dot(features, weights)
      if value > bestValue:
        bestValue = value
        bestAction = a
      elif value == bestValue:
        bestAction = random.choice([a, bestAction])
    # print ('eval time for agent %d: %.8f' % (self.index, time.time() - start))

    x, y = util.nearestPoint(gameState.getAgentState(self.index).getPosition())
    self.visited[x][y] += 1
    return bestAction
  
  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    # Successor를 찾는 함수
    # Baseline의 그것과 동일하다
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != util.nearestPoint(pos):
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def getFeatures(self, gameState, action):
    # 피쳐를 얻어오는 함수
    features = np.zeros(7)
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()
    curPos = gameState.getAgentState(self.index).getPosition()

    # 0번 피처. 유령 상태를 유지해야 함
    features[0] = not myState.isPacman

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]  # 적들의 위치
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]     # 침입한 적 팩맨의 위치
    # 1번 피처. 적 팩맨의 수
    features[1] = len(invaders)
    
    # 2번 피처. 팩맨인 적과의 거리: 자신이 마킹하지 않더라도 팩맨인 상대의 위치를 따라감
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features[2] = min(dists)

    # 3번 피처. 적과의 거리: 각각 자신이 마킹하는 상대의 위치를 따라감
    # features[3] = self.getMazeDistance(myPos, successor.getAgentState(self.marking).getPosition())
    if enemies:
      temp = float('inf')
      enemyNearestBorder = None
      for border in self.borderList:
        if temp > self.getMazeDistance(border, successor.getAgentState(self.marking).getPosition()):
          temp = self.getMazeDistance(border, successor.getAgentState(self.marking).getPosition())
          enemyNearestBorder = border
      features[3] = self.getMazeDistance(myPos, enemyNearestBorder)

    # 4번 피처. 경계(아군의 영역 중 최전선)에 있고 점수를 얻어야 하는 경우 북쪽 혹은 남쪽으로 조금씩 움직임
    if self.getScore(gameState) < 1 and curPos[0] == self.border_x:
      features[4] = action == Directions.NORTH if self.index == self.getTeam(gameState)[0] else action == Directions.SOUTH

    enemies = [gameState.getAgentState(i) for i in self.getOpponents(successor)]   # 현재 적들의 위치
    enemyDists = [self.getMazeDistance(curPos, a.getPosition()) for a in enemies]  # 현재 적들과의 거리
    foods = self.getFood(gameState).asList()                                       # 현재 음식의 위치
    foodDists = [self.getMazeDistance(curPos, food) for food in foods]             # 현재 음식과의 거리
    food_borderDists = [[self.getMazeDistance(food, border) for food in foods] for border in self.borderList] # 음식과 복귀지점과의 거리
    capsules = [c for c in self.getCapsules(gameState)]                            # 현재 캡슐의 위치
    capusleDists = [self.getMazeDistance(curPos, c) for c in capsules]             # 현재 캡슐과의 거리


    # oppDead는 최근에 죽어서 복귀하는 중인 적의 수 * 5 + 1
    # 이 수에 따라 에이전트가 공격적이 될 조건이 완화된다
    oppDead = 1
    for opp in self.getOpponents(gameState):
      if self.teamColor == 'RED':
        oppDead += (gameState.getAgentState(opp).getPosition()[0] > self.walls.width * 3 / 4) * 2
      else:
        oppDead += (gameState.getAgentState(opp).getPosition()[0] < self.walls.width * 1 / 4) * 2

    if self.getScore(gameState) < 1 and\
        curPos[0] == self.border_x and\
          gameState.getAgentState(self.teamMate).getPosition()[0] == self.border_x and\
            enemyDists and foodDists:
      if not capusleDists: capusleDists = [float('inf')]
      if min(enemyDists) > min(min(foodDists) + min(map(min, food_borderDists)), min(capusleDists)) // oppDead:
        # 5번 피처. 전진 여부: 이기고 있지 않고, 팀이 전부 경계선에서 대치 중이고, 상대가 충분히 멀리 있다면 공격적으로 전환
        temp = [self.getMazeDistance(myPos, c) for c in capsules]
        if not temp: temp = [float('inf')]
        features[5] = min(min([self.getMazeDistance(myPos, food) for food in foods]), min(temp))

    # 6번 피처. 계속 같은 위치에 있지 않고 탐험을 하기
    if self.getScore(gameState) < 1:
      posInt = util.nearestPoint(myPos)
      features[6] = self.visited[posInt[0]][posInt[1]]

    return features
  
  def getWeights(self):
    # 가중치를 얻어오는 함수
    return np.array([1000, -10000000, -200, -20, 60, -2500, -3])
  
  def getDefFeatures(self, gameState, action):
    # 방어 모드의 피처를 얻어오는 함수
    # 방어 모드 : 팀원이 공격 모드일 때
    # 방어 모드에서는 공격 모드가 될 수 없다
    features = np.zeros(4)
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # 0번 피처. 유령 상태를 유지해야 함
    features[0] = not myState.isPacman

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]  # 적들의 위치
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]     # 침입한 적 팩맨의 위치
    # 1번 피처. 적 팩맨의 수
    features[1] = len(invaders)
    
    # 2번 피처. 팩맨인 적과의 거리: 자신이 마킹하지 않더라도 팩맨인 상대의 위치를 따라감
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features[2] = min(dists)
    
    # 3번 피처. 적과의 거리: 각각 자신이 마킹하는 상대의 위치를 따라감
    features[3] = self.getMazeDistance(myPos, successor.getAgentState(self.marking).getPosition())
    # temp = float('inf')
    # enemyNearestBorder = None
    # for border in self.borderList:
    #   if temp > self.getMazeDistance(border, successor.getAgentState(self.marking).getPosition()):
    #     temp = self.getMazeDistance(border, successor.getAgentState(self.marking).getPosition())
    #     enemyNearestBorder = border
    # features[3] = self.getMazeDistance(myPos, enemyNearestBorder)

    return features

  def getDefWeights(self):
    # 방어 모드의 가중치를 얻어오는 함수
    # 방어 모드 : 팀원이 공격 모드일 때
    # 방어 모드에서는 공격 모드가 될 수 없다
    return np.array([100, -1000000, -500, -20])
  
  def getOffFeatures(self, gameState, action):
    # 공격 모드의 피처를 얻어오는 함수
    # 공격 모드 : 적 에이전트로부터 멀어져서 음식 탈취를 시도해볼만 할 때
    features = np.zeros(8)
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()


    # 0번 피처. 음식의 개수 : 많을수록 안좋음
    foodList = self.getFood(successor).asList()
    features[0] = len(foodList)

    # 음식이 있다면
    # 반드시 음식이 있을 것 같지만, 음식을 2개 남기고 돌아오는 길에 나머지 음식들도 먹어버릴 수 있으므로 확인해야 한다
    if foodList:
      # 1번 피처. 음식까지의 거리를 구한 후 최소값
      foodDists = np.array([self.getMazeDistance(myPos, food) for food in foodList])
      features[1] = min(foodDists)
      

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]  # 적들의 위치
    ghosts = [a for a in enemies if not a.isPacman and not a.scaredTimer and a.getPosition() != None]   # 공포 상태가 아닌 적 유령의 위치
    if gameState.getAgentState(self.index).isPacman:                              # 팩맨인 동안 = 적의 영역에 있는 동안 // 불필요하긴 할 듯
      if ghosts:                                                                  # 유령이 있다면
        ghostDists = np.array([self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts]) # 유령과의 거리를 구함
        # 2, 3번 피처. 유령과 인접하지 않았는지와 가장 가까운 유령과의 거리
        features[2] = not min(ghostDists) <= 1
        features[3] = np.log10(min(ghostDists))

    capsules = [c for c in self.getCapsules(successor)]
    # 4번 피처. 캡슐의 개수: 적을수록 좋음
    features[4] = len(capsules)
    if capsules:
      capsuleDists = [self.getMazeDistance(myPos, c) for c in capsules]
      # 5번 피처. 캡슐과의 최소 거리
      features[5] = np.log(min(capsuleDists))

    # 만약 음식을 들고 있다면
    if gameState.getAgentState(self.index).numCarrying:
      # 6번 피처. 아군 영역과의 거리
      borderDists = np.array([self.getMazeDistance(myPos, border) for border in self.borderList])
      features[6] = np.log(min(borderDists))

      # 0, 1번 피처의 가중치가 감소한다
      features[0] *= 0.2
      features[1] *= 1    # 왜 넣었는가? 튜닝의 여지를 남기기 위해(하이퍼파라미터)

      # 7번 피처. 막다른 골목으로 가지 않기
      # 이게 음식을 들고 있는 동안만 적용되는 이유는 음식이 없으면 막다른 골목에 가서 죽더라도 음식을 조금 옮겨야 할 수도 있기 때문이다
      features[7] = len(successor.getLegalActions(self.index)) > 2
    

    # if gameState.getAgentState(self.index).isPacman: print(gameState.getAgentState(self.index).getPosition(), action, features)
    return features

  def getOffWeights(self):
    # 공격 모드의 가중치를 얻어오는 함수
    # 공격 모드 : 적 에이전트로부터 멀어져서 음식 탈취를 시도해볼만 할 때
    return np.array([-30, -1, 1000, 20, -1500, -15, -100, 100])