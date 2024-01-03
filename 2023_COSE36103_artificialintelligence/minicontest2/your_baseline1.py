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
    self.wait = 0                                                         # 상대 유령이 있어 도망친 이후 기다리는 시간(가변)


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    # start = time.time()

    self.wait = max(self.wait - 1, 0)                 # 매 틱마다 대기 시간을 1 감소시킨다
    foodLeft = len(self.getFood(gameState).asList())  # 남은 음식의 개수를 구한다

    if not gameState.getAgentState(self.index).isPacman: # 에이전트가 유령인 동안 = 자기 영역에 있는 동안
      self.foodNum = foodLeft                            # 음식의 개수를 갱신
      # .008 - 가진 음식의 수*.002 확률로 가질 수 있는 음식의 개수를 1개씩 최대 4개까지 증가시킴
      self.foodLimit = min(self.foodLimit + (1 if random.random() > 0.992 + (0.002 * self.foodLimit) else 0), 4)

    # 이전 상태 보기
    previous = self.getPreviousObservation()
    # 이전 상태에 팩맨이고 이제는 유령이라면 = 이전 상태까지 상대 영역에 있다가 자기 영역으로 돌아오면
    if previous != None and previous.getAgentState(self.index).isPacman and not gameState.getAgentState(self.index).isPacman:
      if gameState.getAgentState(self.index).getPosition() == self.start: # 만약 돌아온 위치가 시작점이라면 = 잡아먹힌 거라면
        self.foodLimit = max(self.foodLimit//2, 1)                        # 가질 수 있는 음식의 수를 절반으로 한다(최소 1)
      else:                                                               # 만약 잡아먹힌 게 아니라 적 유령을 피해서 돌아온 거라면
        self.wait = 10                                                    # 10틱간 대기 : 대기하는 동안은 수비

    if foodLeft <= self.foodNum - self.foodLimit or foodLeft <= 2:        # 가질 수 있는 음식 수를 채우거나 남은 음식이 2개 이하라면
      # 최단거리로 시작점으로 돌아간다
      bestDist = float('inf')
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist and successor.getAgentState(self.index).getPosition() != self.start:
          bestAction = action
          bestDist = dist
      return bestAction

    # 공격자 팩맨은 두 가지 모드로 활동한다
    # 첫 번째 모드는 getFeatures()와 getWeights()에 정의된 일반적 공격 행동
    # 두 번째 모드는 getDifFeatures()와 getDifWeights()에 정의된 수비적 행동
    # 수비적 모드는 적 유령에게서 도망쳐나온 10틱 간, 또는 우위를 점하고(getScore>2) 방어를 하는 동안 나타난다
    weights = self.getWeights()
    if self.getScore(gameState) > 2 or self.wait:
      weights = self.getDifWeights()
    # 가장 최적의 행동을 결정한다
    # 같은 값을 가지는 행동이 여럿이면 랜덤으로 결정하긴 하는데,
    # 사실 엄밀히 말해서 Uniform Distribution은 아니다
    # 그래도 큰 상관은 없을 듯
    bestValue = -float('inf')
    bestAction = Directions.STOP
    for a in actions:
      if self.getScore(gameState) > 2 or self.wait:
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
  # 공격적인 에이전트
  def getFeatures(self, gameState, action):
    features = np.zeros(8)
    successor = self.getSuccessor(gameState, action)

    # 0번 피처. 음식의 개수 : 많을수록 안좋음
    foodList = self.getFood(successor).asList()
    features[0] = len(foodList)

    myPos = successor.getAgentState(self.index).getPosition()                     # 에이전트의 위치
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]  # 적들의 위치
    # 음식이 있다면
    # 반드시 음식이 있을 것 같지만, 음식을 2개 남기고 돌아오는 길에 나머지 음식들도 먹어버릴 수 있으므로 확인해야 한다
    if foodList:
      # 1, 2번 피처. 음식까지의 거리를 구한 후 최소값과 평균값
      foodDists = np.array([self.getMazeDistance(myPos, food) for food in foodList])
      features[1] = min(foodDists)
      features[2] = np.mean(foodDists)
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None] # 적 유령의 위치
    if gameState.getAgentState(self.index).isPacman:                            # 팩맨인 동안 = 적의 영역에 있는 동안
      if ghosts:                                                                # 유령이 있다면
        ghostDists = np.array([self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts]) # 유령과의 거리를 구함
        # 3, 4번 피처. 유령과 인접하지 않았는지와 가장 가까운 유령과의 거리
        features[3] = not min(ghostDists) <= 1
        features[4] = min(ghostDists)
    else:                                                                       # 유령인 동안 = 아군 영역에 있는 동안
      invaders = [a for a in enemies if a.isPacman and a.getPosition() != None] # 적 팩맨의 위치
      if invaders:                                                              # 적 팩맨이 있다면
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]# 적 팩맨과의 거리를 구해서
        # 5번 피처. 적 팩맨과의 거리: 로그를 취해서 멀수록 효과가 약하게 만듦
        features[5] = np.log(min(dists))
      # 6번 피처. 적 팩맨의 수
      features[6] = len(invaders)
    # 6번 피처. 정지에 대한 패널티
    features[7] = not action == Directions.STOP
    return features
  
  def getWeights(self):
    return np.array([-100, -1, -0.1, 1000, 0.1, -5, -1000, 10])
  
  def getDifFeatures(self, gameState, action):
    # 공격 에이전트의 대체(수비 모드) 피쳐들
    # 점수가 2점 초과로 앞서거나 적 유령을 보고 잠시 아군 영역으로 피신한 경우 발동한다
    features = np.zeros(5)
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # 0번 피처. 팩맨이 아니어야 함: 즉, 아군 영역에 계속 머물러야 함
    features[0] = not myState.isPacman

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]  # 적들의 위치
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]     # 침입한 적 팩맨의 위치
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]   # 적 유령의 위치
    if successor.getAgentState(self.index).isPacman:                                                # 내가 지금 혹시라도 팩맨이라면
      ghostDists = np.array([self.getMazeDistance(myPos, ghost.getPosition()) for ghost in ghosts]) # 적 유령과의 거리를 구해서
      if len(ghostDists) > 0:                                                                       # 적 유령이 있다면 빨리 멀어진다
        # 1번 피처. 팩맨인 상태에서 유령과의 거리
        features[1] = min(ghostDists)
    else:
      # 2번 피처. 유령인 상태에서 적 팩맨의 수
      features[2] = len(invaders)
      # 만약 침입한 팩맨이 있다면 거리를 구한다
      if invaders:
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
        # 3번 피처. 침입한 가장 가까운 팩맨과의 거리
        features[3] = min(dists)
      
      # 보호해야 하는 캡슐과의 거리를 구한다
      capsules = [c for c in self.getCapsulesYouAreDefending(gameState)]
      # 만약 캡슐이 있다면
      if capsules:
        # 피처 4. 캡슐들의 중간 지점에 위치한다: 캡슐을 공격당하면 크게 불리해지기 때문
        features[4] = np.mean([self.getMazeDistance(myPos, capsule) for capsule in capsules])

    return features
  
  def getDifWeights(self):
    return np.array([100, 10, -1000, -10, -3])

class ReflexDefAgent(ReflexBaseAgent):
  def getFeatures(self, gameState, action):
    features = np.zeros(5)
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
    dists2 = [self.getMazeDistance(myPos, a.getPosition()) for a in enemies]
    # 3번 피처. 적들과의 거리: 이게 필요한 이유는 팩맨이 될 수 있는 잠재적인 적 유령에 대해 방어하기 위해서임
    features[3] = min(dists2)

    # 만약 적이 캡슐을 먹어서 유령이 공포 모드라면
    if gameState.getAgentState(self.index).scaredTimer and len(invaders) > 0:
      # 4번 피처. 도망간다
      features[4] = min(dists)

    return features
  
  def getWeights(self):
    return np.array([100, -1000, -10, -3, 2000])