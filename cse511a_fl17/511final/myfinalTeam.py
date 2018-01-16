# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint
SIGHT_RANGE = 5

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DefensiveOffensiveReflexAgent', second = 'MoreDefensiveReflexAgent'):
  # second = 'MoreDefensiveReflexAgent'
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
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

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

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1}


  def value(self, state, agent, depth, alpha, beta, opponent):
      length = len(opponent)

      agent = agent % length
      if opponent[agent] == self.index:
        agent = 0
        depth += 1

      if self.isTerminal(state, depth, opponent[agent], length):
        return self.evaluate(state, "Stop")

      if opponent[agent] == self.index:
        return self.maxValue(state, agent, depth, alpha, beta, opponent)
      else:
        return self.minValue(state, agent, depth, alpha, beta, opponent)

  def minValue(self, state, agent, depth, alpha, beta, opponent):
    v = ("unknown", float("inf"))
    length = len(opponent)
    if self.isTerminal(state, depth, opponent[agent], length):
      return self.evaluate(state, "Stop")

    for action in state.getLegalActions(opponent[agent]):

      Val = self.value(state.generateSuccessor(opponent[agent], action), agent + 1, depth, alpha, beta, opponent)
      if type(Val) is tuple:
        Val = Val[1]

      NewVal = min(v[1], Val)

      if NewVal is not v[1]:
        v = (action, NewVal)

      if v[1] <= alpha:
        return v

      beta = min(beta, v[1])

    return v

  def maxValue(self, state, agent, depth, alpha, beta, opponent):
    v = ("unknown", float("-inf"))
    length = len(opponent)
    if self.isTerminal(state, depth, opponent[agent], length):
      return self.betterEvaluationFunction(state, length)

    for action in state.getLegalActions(opponent[agent]):
      #             if action == "Stop":
      #                 continue

      Val = self.value(state.generateSuccessor(opponent[agent], action), agent + 1, depth, alpha, beta, opponent)
      if type(Val) is tuple:
        Val = Val[1]

      NewVal = max(v[1], Val)

      if NewVal is not v[1]:
        v = (action, NewVal)

      if v[1] >= beta:
        return v

      alpha = max(alpha, v[1])

    return v

  def isTerminal(self, state, depth, agent, length):
    if length == 1:
      return depth == 4 or state.isOver()
    else:
      return depth == 4 or state.isOver()






class MoreDefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """
  onPower = 0
  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    # print '---'
    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    bestAction =  random.choice(bestActions)

    if MoreDefensiveReflexAgent.onPower > 0:
      MoreDefensiveReflexAgent.onPower -= 1
    # if gameState.generateSuccessor(self.index, bestAction).getAgentPosition(self.index) in self.getCapsules(self.getSuccessor(gameState, bestAction)):
    if gameState.generateSuccessor(self.index, bestAction).getAgentPosition(self.index) in self.getCapsules(gameState):
      MoreDefensiveReflexAgent.onPower = 80
    # todo-hy: a bug here

    return bestAction

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dist_min_invaders = min([self.getMazeDistance(myPos, a.getPosition()) for a in invaders])
      features['invaderDistance'] = dist_min_invaders

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    features['successorScore'] = self.getScore(successor)

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = 1.0 / minDistance
    """
    Above comes from the baseline, below is our new feature
    """
    if len(self.getCapsules(successor)) == 0:
      features['distanceToCapsule'] = 50  
    else :
      dists_caps = [self.getMazeDistance(successor.getAgentPosition(self.index), a) for a in self.getCapsules(successor)]
      features['distanceToCapsule'] = 0.5 / min(dists_caps)
    features['siHuTong'] = 1 if len(successor.getLegalActions(self.index)) < 3 else 0

    defenders = [b for b in enemies if not b.isPacman and b.getPosition() != None]
    if len(defenders) > 0:
      dist_min = min([self.getMazeDistance(myPos, b.getPosition()) for b in defenders])
    else:
      dist_min = 9999
    features['runExclamation'] = (dist_min <= 1) * myState.isPacman 
    features['siHuTongAndRunExclamation'] = (dist_min <= 3) * myState.isPacman * (1 if len(successor.getLegalActions(self.index)) < 3 else 0)
    # print dist_min
    # print features['runExclamation']
    # print myState.isPacman 
    # if (dist_min == 1):
    #   print "dist_min"
    # print features['runExclamation']
    #print self.onPower
    return features

  def getWeights(self, gameState, action):
    return {
    'numInvaders': -1000, 
    'onDefense': 100, 
    'invaderDistance': -10, 
    'stop': -100, 
    'reverse': -2, 
    'successorScore': 0,
    'distanceToFood': 5, 
    'distanceToCapsule': 0, 
    'siHuTong': 0, 
    'runExclamation': 0,
    'siHuTongAndRunExclamation': 0
    }

class DefensiveOffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """
  onPower = 0
  # def chooseAction(self, gameState):
  #   actions = gameState.getLegalActions(self.index)
  #   # start = time.time()
  #   values = [self.evaluate(gameState, a) for a in actions]
  #   # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)
  #
  #   maxValue = max(values)
  #   bestActions = [a for a, v in zip(actions, values) if v == maxValue]
  #   bestAction =  random.choice(bestActions)

    # if DefensiveOffensiveReflexAgent.onPower > 0:
    #   DefensiveOffensiveReflexAgent.onPower -= 1
    # # if gameState.generateSuccessor(self.index, bestAction).getAgentPosition(self.index) in self.getCapsules(self.getSuccessor(gameState, bestAction)):
    # if gameState.generateSuccessor(self.index, bestAction).getAgentPosition(self.index) in self.getCapsules(gameState):
    #   DefensiveOffensiveReflexAgent.onPower = 80
    # # todo-hy: maybe a bug here
    #
    # return bestAction


  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    self.opponents = []
    self.InvadePacman = []

    for i in self.getOpponents(gameState):
      if not gameState.getAgentState(i).isPacman:
        position = gameState.getAgentState(i).getPosition()
        if position != None:
          if util.manhattanDistance(position, gameState.getAgentPosition(self.index)) <= SIGHT_RANGE:
            self.opponents.append(i)

      else:
        position = gameState.getAgentState(i).getPosition()
        if position != None:
          self.InvadePacman.append(i)

    self.opponents.insert(0, self.index)
    self.InvadePacman.insert(0, self.index)

    if gameState.getAgentState(self.index).isPacman:
      action, _ = self.value(gameState, 0, 0, float("-inf"), float("inf"), self.opponents)

    else:
      action, _ = self.value(gameState, 0, 0, float("-inf"), float("inf"), self.InvadePacman)

    return action



  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dist_min_invaders = min([self.getMazeDistance(myPos, a.getPosition()) for a in invaders])
      features['invaderDistance'] = dist_min_invaders

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    features['successorScore'] = self.getScore(successor)

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = 1.0 / minDistance
    """
    Above comes from the baseline, below is our new feature
    """
    if len(self.getCapsules(successor)) == 0:
      features['distanceToCapsule'] = 50  
    else :
      dists_caps = [self.getMazeDistance(successor.getAgentPosition(self.index), a) for a in self.getCapsules(successor)]
      features['distanceToCapsule'] = 0.5 / min(dists_caps)
    features['siHuTong'] = 1 if len(successor.getLegalActions(self.index)) < 3 else 0

    defenders = [b for b in enemies if not b.isPacman and b.getPosition() != None]
    if len(defenders) > 0:
      dist_min = min([self.getMazeDistance(myPos, b.getPosition()) for b in defenders])
    else:
      dist_min = 9999
    features['runExclamation'] = (dist_min <= 1) * myState.isPacman * (self.onPower <= 0)
    features['siHuTongAndRunExclamation'] = (dist_min <= 3) * myState.isPacman * (self.onPower <= 0) * (1 if len(successor.getLegalActions(self.index)) < 3 else 0)
    # print dist_min
    # print features['runExclamation']
    # print myState.isPacman 
    # if (dist_min == 1):
    #   print "dist_min"
    # print features['runExclamation']
    # if self.onPower:
    #   print self.onPower
    return features

  def getWeights(self, gameState, action):
    return {
    'numInvaders': 0, 
    'onDefense': 0, 
    'invaderDistance': 0, 
    'stop': -100, 
    'reverse': 0, 
    'successorScore': 1000,
    'distanceToFood': 2, 
    'distanceToCapsule': 4, 
    'siHuTong': -100, 
    'runExclamation': -999999999.0,
    'siHuTongAndRunExclamation': 0
    }


