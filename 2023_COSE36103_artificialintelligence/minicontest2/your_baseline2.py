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
               first = 'ReflexOffAgent', second = 'ReflexDefAgent'):
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

class ReflexBaseAgent(CaptureAgent):
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
    self.start = gameState.getAgentPosition(self.index)                   # 시작 지점
    self.foodNum = len(self.getFood(gameState).asList())                  # 음식의 개수(가변)
    self.foodLimit = 1                                                    # 에이전트가 한번에 가질 수 있는 음식의 수(가변)
    self.teamColor = 'BLUE' if self.getTeam(gameState)[0] % 2 else 'RED'  # 팀 색깔

    # 음식 그리드, 벽 그리드, 아군의 최전선(아군 영역의 가장 바깥쪽 x좌표), 최전선 그리드, 최전선 좌표들
    self.foods = self.getFood(gameState)
    walls = gameState.getWalls()
    border_x = walls.width // 2 - 1 if self.teamColor == 'RED' else walls.width // 2
    self.borderList = [(border_x, y) for y in range(walls.height) if not walls[border_x][y]]

    # 자신과 음식, 적과 음식 거리를 구해서 그 차이가 가장 큰 음식을 쫓아간다
    distDif = float('inf')
    self.initFood = None
    for food in self.foods.asList():
      dist_team = self.getMazeDistance(self.start, food)
      dist_opp = self.getMazeDistance(gameState.getAgentState(self.getOpponents(gameState)[0]).getPosition(), food)
      if distDif > dist_opp - dist_team:
        self.initFood = food
        distDif = dist_team - dist_opp

    global changemode, def_marking, off_marking
    changemode = False
    def_marking, off_marking = self.getOpponents(gameState)

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    # start = time.time()

    global changemode
    if self.getScore(gameState) < 1 and changemode:
      changemode = False

    # 공격자 팩맨은 두 가지 모드로 활동한다
    # 첫 번째 모드는 getFeatures()와 getWeights()에 정의된 일반적 공격 행동
    # 두 번째 모드는 getDifFeatures()와 getDifWeights()에 정의된 수비적 행동
    # 수비적 모드는 우위를 점하고(getScore>=1) 방어를 하는 동안 나타난다
    weights = self.getWeights()
    if changemode:
      weights = self.getDifWeights()
    # 가장 최적의 행동을 결정한다
    # 같은 값을 가지는 행동이 여럿이면 랜덤으로 결정하긴 하는데,
    # 사실 엄밀히 말해서 Uniform Distribution은 아니다
    # 그래도 큰 상관은 없을 듯
    bestValue = -float('inf')
    bestAction = Directions.STOP
    for a in actions:
      if changemode:
        features = self.getDifFeatures(gameState, a)
      else:
        features = self.getFeatures(gameState, a)
      value = np.dot(features, weights)
      if value > bestValue:
        bestValue = value
        bestAction = a
      elif value == bestValue:
        bestAction = random.choice([a, bestAction])


    # print ('eval time for agent %d: %.8f' % (self.index, time.time() - start))

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
    features = np.zeros(1)
    successor = self.getSuccessor(gameState, action)
    features[0] = self.getScore(successor)
    return features
  
  def getWeights(self):
    # 가중치를 얻어오는 함수
    return np.array([1])
  
  def getDifFeatures(self, gameState, action):
    # 두 번째 모드의 피처를 얻어오는 함수
    return self.getFeatures(gameState, action)

  def getDifWeights(self):
    # 두 번째 모드의 가중치를 얻어오는 함수
    return self.getWeights()

class ReflexOffAgent(ReflexBaseAgent):
  def chooseAction(self, gameState):

    if self.getScore(gameState) >= 1:
      global changemode
      changemode = True

    return super().chooseAction(gameState)

  def getFeatures(self, gameState, action):
    features = np.zeros(7)
    successor = self.getSuccessor(gameState, action)

    # 0번 피처. 음식의 개수 : 많을수록 안좋음
    foodList = self.getFood(successor).asList()
    features[0] = len(foodList)

    myPos = successor.getAgentState(self.index).getPosition()                     # 에이전트의 위치
    # 음식이 있다면
    # 반드시 음식이 있을 것 같지만, 음식을 2개 남기고 돌아오는 길에 나머지 음식들도 먹어버릴 수 있으므로 확인해야 한다
    if foodList:
      # 1, 2번 피처. 음식까지의 거리를 구한 후 최소값과 평균값
      foodDists = np.array([self.getMazeDistance(myPos, food) for food in foodList])
      if self.getFood(gameState)[self.initFood[0]][self.initFood[1]]:
        features[1] = self.getMazeDistance(myPos, self.initFood)
      else:
        features[1] = min(foodDists)
      features[2] = np.mean(foodDists)

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]  # 적들의 위치
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]   # 적 유령의 위치
    if gameState.getAgentState(self.index).isPacman:                              # 팩맨인 동안 = 적의 영역에 있는 동안
      if ghosts:                                                                  # 유령이 있다면
        ghostDists = np.array([self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts]) # 유령과의 거리를 구함
        # 3, 4번 피처. 유령과 인접하지 않았는지와 가장 가까운 유령과의 거리
        features[3] = not min(ghostDists) <= 1
        features[4] = np.log10(min(ghostDists))
    
    # 음식을 하나라도 들고 있는 경우
    if gameState.getAgentState(self.index).numCarrying:
      # 5번 피처. 아군 영역과의 거리
      borderDists = np.array([self.getMazeDistance(myPos, border) for border in self.borderList])
      features[5] = min(borderDists)

      # 6번 피처. 아군 영역으로 돌아왔는지?
      features[6] = not successor.getAgentState(self.index).isPacman

    return features
  
  def getWeights(self):
    return np.array([-100, -1, -0.1, 1000, 5, -5, 1000])
  
  def getDifFeatures(self, gameState, action):
    # 공격 에이전트의 대체(수비 모드) 피쳐들
    # 점수가 앞서는 경우 발동한다
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
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      # 2번 피처. 적 팩맨이 있다면 가장 가까운 팩맨과의 거리
      features[2] = min(dists)
    
    # 3번 피처. 적들과의 거리: 이게 필요한 이유는 팩맨이 될 수 있는 잠재적인 적 유령에 대해 방어하기 위해서임
    # 그 중에서도 off_marking은 현재 공격 에이전트가 마킹하는 적 에이전트의 인덱스를 의미함
    # features[3] = self.getMazeDistance(myPos, successor.getAgentState(off_marking).getPosition())
    temp = float('inf')
    enemyNearestBorder = None
    for border in self.borderList:
      if temp > self.getMazeDistance(border, successor.getAgentState(off_marking).getPosition()):
        temp = self.getMazeDistance(border, successor.getAgentState(off_marking).getPosition())
        enemyNearestBorder = border
    features[3] = self.getMazeDistance(myPos, enemyNearestBorder)

    return features
  
  def getDifWeights(self):
    return np.array([100, -1000, -10, -3])

class ReflexDefAgent(ReflexBaseAgent):
  def chooseAction(self, gameState):
    # 모드가 바뀌면
    if changemode:
      # def_marking과 off_marking을 정의
      # 원래 방어 에이전트가 마킹하던 적이 def_marking, 반대쪽이 off_marking
      global def_marking, off_marking
      def_marking, off_marking = (self.getOpponents(gameState)[0], self.getOpponents(gameState)[1])\
          if self.getMazeDistance(gameState.getAgentState(self.getOpponents(gameState)[0]).getPosition(), gameState.getAgentState(self.index).getPosition())\
          < self.getMazeDistance(gameState.getAgentState(self.getOpponents(gameState)[1]).getPosition(), gameState.getAgentState(self.index).getPosition())\
          else (self.getOpponents(gameState)[1], self.getOpponents(gameState)[0])
    return super().chooseAction(gameState)


  def getFeatures(self, gameState, action):
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
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      # 2번 피처. 적 팩맨이 있다면 가장 가까운 팩맨과의 거리
      features[2] = min(dists)
    
    # 적들과의 거리
    # dists2 = [self.getMazeDistance(myPos, a.getPosition()) for a in enemies]
    # 3번 피처. 적들과의 거리: 이게 필요한 이유는 팩맨이 될 수 있는 잠재적인 적 유령에 대해 방어하기 위해서임
    # features[3] = min(dists2)
    temp = float('inf')
    enemyNearestBorder = None
    for enemy_i in self.getOpponents(successor):
      for border in self.borderList:
        if temp > self.getMazeDistance(border, successor.getAgentState(enemy_i).getPosition()):
          temp = self.getMazeDistance(border, successor.getAgentState(enemy_i).getPosition())
          enemyNearestBorder = border
      features[3] = self.getMazeDistance(myPos, enemyNearestBorder)

    return features
  
  def getWeights(self):
    return np.array([100, -1000, -10, -3])
  
  def getDifFeatures(self, gameState, action):
    # changemode가 되면 적용되는 피처들
    # 마지막 3번을 제외하고는 모두 그대로
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
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      # 2번 피처. 적 팩맨이 있다면 가장 가까운 팩맨과의 거리
      features[2] = min(dists)
    
    # 적들과의 거리
    # 3번 피처. 적들과의 거리: 이게 필요한 이유는 팩맨이 될 수 있는 잠재적인 적 유령에 대해 방어하기 위해서임
    # 그 중에서도 def_marking은 현재 수비 에이전트가 마킹하는 적 에이전트의 인덱스를 의미함
    # features[3] = self.getMazeDistance(myPos, successor.getAgentState(def_marking).getPosition())
    temp = float('inf')
    enemyNearestBorder = None
    for border in self.borderList:
      if temp > self.getMazeDistance(border, successor.getAgentState(def_marking).getPosition()):
        temp = self.getMazeDistance(border, successor.getAgentState(def_marking).getPosition())
        enemyNearestBorder = border
    features[3] = self.getMazeDistance(myPos, enemyNearestBorder)

    return features

  def getDifWeights(self):
    return np.array([100, -1000, -10, -3])