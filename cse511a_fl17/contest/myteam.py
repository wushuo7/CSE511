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


depth = 3
#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
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
    return {'successorScore': 1.0}



  def max_value(self, gameState, agentIndex, level, a, b, enemy):
    max_now = ("unknown", float('-inf'))
    if self.isOver(gameState, level):
      return self.evaluate(gameState, "Stop")


    movements = gameState.getLegalActions(enemy[agentIndex])

    for i in movements:
      new_state = gameState.generateSuccessor(enemy[agentIndex], i)
      p =agentIndex +1
      value = self.GetValue(new_state, p, level, a, b, enemy)
      # last ghost choose
      if type(value) is tuple:
        value = value[1]

      if max_now[1] < value:
        max_now = (i, value)
      if max_now[1] >= b:
        return max_now

      a = max(a, max_now[1])
    return max_now

  def min_value(self, gameState, agentIndex, level, a, b, enemy):
    number = len(enemy)
    if self.isOver(gameState, level):
      return self.evaluate(gameState, "Stop")
    min_now = ("unknown", float('inf'))
    movements = gameState.getLegalActions(enemy[agentIndex])

    for i in movements:
      new_state = gameState.generateSuccessor(enemy[agentIndex], i)
      t = agentIndex+1
      value = self.GetValue(new_state, t, level, a, b, enemy)
      # last ghost choose
      if type(value) is tuple:
        value = value[1]

      if min_now[1] > value:
        min_now = (i, value)
      if min_now[1] <= a:
        return min_now
      b = min(b, min_now[1])
    return min_now

  def GetValue(self, Gamestate, agentIndex, level, a, b, enemy):

    length = len(enemy)

    agentIndex = agentIndex % length
    if enemy[agentIndex] == self.index:
      agentIndex = 0
      level += 1

    if self.isOver(Gamestate, level):
      return self.evaluate(Gamestate, "Stop")

    if enemy[agentIndex] == self.index:
      return self.max_value(Gamestate, agentIndex, level, a, b, enemy)
    else:
      return self.min_value(Gamestate, agentIndex, level, a, b, enemy)

  def isOver(self, state, level):
    return level ==4 or state.isOver()



class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  NiuBi = 0

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    self.enemy = []
    self.bad = []

    for bad in self.getOpponents(gameState):
      if not gameState.getAgentState(bad).isPacman:
        loc = gameState.getAgentState(bad).getPosition()
        if loc != None:
          if util.manhattanDistance(loc, gameState.getAgentPosition(self.index)) <= depth:
            self.enemy.append(bad)

      else:
        loc = gameState.getAgentState(bad).getPosition()
        if loc != None:
          self.bad.append(bad)
    value_test = int(0)

    self.enemy.insert(value_test, self.index)
    self.bad.insert(value_test, self.index)



    a = float("-inf")
    b = float("inf")
    if gameState.getAgentState(self.index).isPacman:
      best_move, null = self.GetValue(gameState, value_test, value_test, a, b, self.enemy)

    else:
      best_move, null = self.GetValue(gameState, value_test, value_test, a, b, self.bad)

    return best_move

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    features['status'] =0
    if myState.isPacman:
      features['status'] =10# on offensive
    else:
      features['status'] = -10#on defensive
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      mindist_to_invaders = min([self.getMazeDistance(myPos, a.getPosition()) for a in invaders])
      features['invaderDistance'] =  mindist_to_invaders

    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1
    features['successorScore'] = self.getScore(successor)


    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      everyfood = [self.getMazeDistance(myPos, food) for food in foodList]
      close_food = min(everyfood)
      # if successor is a food, score increase, the more the better
      #if self.getFood(successor)[int(myPos[0])][int(myPos[1])] == True:
      #  features['distanceToFood'] +=100
      # if the, the more the better
      Capsules = self.getCapsules(successor)
      if sum(everyfood) != 0:
        features['distanceToFood'] = 100.0/(close_food)
      # the more, the worse
      if sum(everyfood) !=0:
        features['distanceToAll'] = sum(everyfood)

      if action == Directions.STOP :
        features['stop'] = 1

      # let pacman eat Capsules as more as possible

      # the more, the better features['distanceToCapsule']
      if len(Capsules)==0:
        features['Capsule']= 40

      if len(Capsules)!=0:
        dists_caps_min = min([self.getMazeDistance(myPos, p) for p in Capsules])
        features['distanceToCapsule'] = 10.0/dists_caps_min

      ghosts = [b for b in enemies if not b.isPacman and b.getPosition() != None]
      if len(ghosts) >0:
        dist_ghost_min = min([self.getMazeDistance(myPos, g.getPosition()) for g in ghosts])
      else:
        dist_ghost_min = 10000
      if dist_ghost_min <=1 & myState.isPacman & self.NiuBi<=0 :
        if len(successor.getLegalActions(self.index)) <2:
          features['death_road'] = -100
        if len(Capsules) != 0:
          dists_caps_min = min([self.getMazeDistance(myPos, p) for p in Capsules])
          features['distanceToCapsule'] = dists_caps_min*10
        features['dangerous'] = 10000
        #print ("worse")
      else :
        features['dangerous'] = 0


    return features

  def getWeights(self, gameState, action):

    return {'successorScore': 1000,#20wan
            'distanceToFood': 2.0,
            'status':3,
            'numInvaders':0,
            'invaderDistance':0,
            'distanceToAll':0,
            'distanceToCapsule':5,
            'dangerous':-90000009999.0,
            'Capsule':10,
            'death_road':1,
            'stop':-100,

            }

class DefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  NiuBi = 0

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
    bestAction = random.choice(bestActions)
    if DefensiveReflexAgent.NiuBi > 0:
      DefensiveReflexAgent.NiuBi -= 1
    # if gameState.generateSuccessor(self.index, bestAction).getAgentPosition(self.index) in self.getCapsules(self.getSuccessor(gameState, bestAction)):
    if gameState.generateSuccessor(self.index, bestAction).getAgentPosition(self.index) in self.getCapsules(gameState):
      DefensiveReflexAgent.NiuBi = 40


    return bestAction

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    features['status'] = 1
    if myState.isPacman:
      features['status'] = 0

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      mindist_to_invaders = min([self.getMazeDistance(myPos, a.getPosition()) for a in invaders])
      features['invaderDistance'] = mindist_to_invaders

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1
    features['successorScore'] = self.getScore(successor)

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    food_your_list = self.getFoodYouAreDefending(successor).asList()
    if len(foodList) > 0:  # This should always be True,  but better safe than sorry
      everyfood = [self.getMazeDistance(myPos, food) for food in foodList]
      close_food = min(everyfood)
      if len(food_your_list)<8:
        everyfood_your = [self.getMazeDistance(myPos, food) for food in food_your_list]
        close_your_list = min(everyfood_your)

        if close_your_list !=0:
          features['distanceToFoodMaybeeat'] = 5.0 / (close_your_list)
        features['distanceToAll_you'] = sum(everyfood_your)
      # if successor is a food, score increase, the more the better
      # if self.getFood(successor)[int(myPos[0])][int(myPos[1])] == True:
      #  features['distanceToFood'] +=100
      # if the, the more the better
      if close_food != 0:

        features['distanceToFood'] = 10.0 / (close_food)
      # the more, the worse

      if sum(everyfood) != 0:
        features['distanceToAll'] = sum(everyfood)

      # Computes whether we're on defense (1) or offense (0)
      features['onDefense'] = 1
      if myState.isPacman: features['onDefense'] = 0

      # let pacman eat Capsules as more as possible
      Capsules = self.getCapsules(successor)
      Capsules_YOUR = self.getCapsulesYouAreDefending(successor)
      # the more, the better features['distanceToCapsule']
      if len(Capsules) == 0:
        features['Capsule'] = 40

      if len(Capsules) != 0:
        dists_caps_min = min([self.getMazeDistance(myPos, p) for p in Capsules])
        features['distanceToCapsule'] = dists_caps_min



      if len(food_your_list) < 20 and len(Capsules_YOUR)!=0 and len(food_your_list) > 17 :
        #print len(food_your_list)

        dists_caps_min_YOUR = min([self.getMazeDistance(myPos, p) for p in Capsules_YOUR])
        #print dists_caps_min_YOUR
        features['dists_caps_min_YOUR'] = 100.0/ (dists_caps_min_YOUR+1.0)
        a = 100.0/ (dists_caps_min_YOUR+1.0)
        #print a
      if len(invaders) !=0:
        features['dists_caps_min_YOUR'] =0
      if len(food_your_list)<= 5:
        features['dists_caps_min_YOUR'] = 0


      if action == Directions.STOP: features['stop'] = 1
      rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
      if action == rev: features['reverse'] = 1

      ghosts = [b for b in enemies if not b.isPacman and b.getPosition() != None]
      if len(ghosts) > 0:
        dist_ghost_min = min([self.getMazeDistance(myPos, g.getPosition()) for g in ghosts])
      else:
        dist_ghost_min = 10000
      if dist_ghost_min <= 1 & myState.isPacman:
        if len(successor.getLegalActions(self.index)) < 2:
          features['death_road'] = -100
        if len(Capsules) != 0:
          dists_caps_min = min([self.getMazeDistance(myPos, p) for p in Capsules])
          features['distanceToCapsule'] = dists_caps_min * 100
        features['dangerous'] = 10000
        # print ("worse")
      else:
        features['dangerous'] = 0

    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 0,  # 20wan
            'distanceToFood': 3,
            'status': 0,
            'numInvaders': -1000,
            'invaderDistance': -60,
            'distanceToAll': 0,
            'distanceToCapsule': 0,
            'dangerous': 0,
            'Capsule': 0,
            'death_road': 0,
            'onDefense':100,
            'stop': -100,
            'reverse': -2,
            'distanceToFoodMaybeeat':2,
            'distanceToAll_you':5,
            'dists_caps_min_YOUR':10
            }