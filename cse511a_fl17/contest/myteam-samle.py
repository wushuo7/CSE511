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

    features['status'] =1
    if myState.isPacman:
      features['status'] =0

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      mindist_to_invaders = min([self.getMazeDistance(myPos, a.getPosition()) for a in invaders])
      features['invaderDistance'] =  mindist_to_invaders
    if action == Directions.STOP: features['stop'] = 1
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
      if sum(everyfood) != 0:
        features['distanceToFood'] = 100.0/(close_food)
      # the more, the worse
      if sum(everyfood) !=0:
        features['distanceToAll'] = sum(everyfood)

      # let pacman eat Capsules as more as possible
      Capsules = self.getCapsules(successor)
      # the more, the better features['distanceToCapsule']
      if len(Capsules)==0:
        features['Capsule']= 40

      if len(Capsules)!=0:
        dists_caps_min = min([self.getMazeDistance(myPos, p) for p in Capsules])
        features['distanceToCapsule'] = dists_caps_min

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
          features['distanceToCapsule'] = dists_caps_min*100
        features['dangerous'] = 10000
        #print ("worse")
      else :
        features['dangerous'] = 0

    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 1000,#20wan
            'distanceToFood': 1,
            'status':0,
            'numInvaders':0,
            'invaderDistance':0,
            'distanceToAll':-2,
            'distanceToCapsule':-30,
            'dangerous':-9000000,
            'Capsule':10,
            'death_road':10

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
    if len(foodList) > 0:  # This should always be True,  but better safe than sorry
      everyfood = [self.getMazeDistance(myPos, food) for food in foodList]
      close_food = min(everyfood)
      # if successor is a food, score increase, the more the better
      # if self.getFood(successor)[int(myPos[0])][int(myPos[1])] == True:
      #  features['distanceToFood'] +=100
      # if the, the more the better
      if sum(everyfood) != 0:
        features['distanceToFood'] = 10.0 / (close_food)
      # the more, the worse
      if sum(everyfood) != 0:
        features['distanceToAll'] = sum(everyfood)

      # Computes whether we're on defense (1) or offense (0)
      features['onDefense'] = 1
      if myState.isPacman: features['onDefense'] = 0

      # let pacman eat Capsules as more as possible
      Capsules = self.getCapsules(successor)
      # the more, the better features['distanceToCapsule']
      if len(Capsules) == 0:
        features['Capsule'] = 40

      if len(Capsules) != 0:
        dists_caps_min = min([self.getMazeDistance(myPos, p) for p in Capsules])
        features['distanceToCapsule'] = dists_caps_min

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
            'distanceToFood': 1,
            'status': 0,
            'numInvaders': -1000,
            'invaderDistance': -50,
            'distanceToAll': 0,
            'distanceToCapsule': 0,
            'dangerous': 0,
            'Capsule': 10,
            'death_road': 0,
            'onDefense':100,
            'stop': -100,
            'reverse': -2
            }