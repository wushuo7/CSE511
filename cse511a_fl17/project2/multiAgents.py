# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
import math
from game import Directions
import random, util

from game import Agent


def absoluteDistance(xy1, xy2):
  a = math.pow((xy1[0] - xy2[0]), 2)
  b = math.pow((xy1[1] - xy2[1]), 2)
  c = a + b
  return math.pow(c, 0.5)

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
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



  def evaluationFunction (self, currentGameState, action):
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

    "*** YOUR CODE HERE ***"
    foodlist = newFood.asList()
    food_number = len(foodlist)
    distance_ghost = []
    min_distance1 = float(0)
    for ghost in newGhostStates:
      distance_ghost.append(absoluteDistance(newPos, ghost.getPosition()))
      min_distance1 = min(distance_ghost)
    # be away from the ghost
    if min_distance1 < 1.5:
      return -10000000000

    min_distance2 = float(0)
    distance_food = []
    for food in foodlist:
      distance_food.append(absoluteDistance(newPos, food))
      min_distance2 = min(distance_food)
    a = min_distance2+1
    #encourage pacman to eat dots
    return  -a -100*(len(foodlist)+1)+successorGameState.getScore()
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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    def max_value(gameState, agentIndex, level):

      if level == self.depth:
        return self.evaluationFunction(gameState)
      max1 = float('-inf')
      movements = gameState.getLegalActions(agentIndex)

      # none successor, stay
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      for i in movements:
        next = gameState.generateSuccessor(agentIndex, i)
        now = min_value(next,agentIndex+1,level)
        if now >= max1:
          max1 = now

      return max1

    def min_value(gameState, agentIndex ,level):
      if level == self.depth:
        return self.evaluationFunction(gameState)
      min1 = float('inf')
      movements = gameState.getLegalActions(agentIndex)

      # none successor, stay
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      for i in movements:
        next = gameState.generateSuccessor(agentIndex, i)
        #last ghost choose
        if agentIndex == gameState.getNumAgents()-1:
          now = max_value(next,0,level+1)
          #first ghost - (last-1) ghost choose
        else:
          now = min_value(next, agentIndex+1,level)
        if now <= min1:
          min1 = now
      return min1


    max2 = float('-inf')

    movement = gameState.getLegalActions(0)

    for i in movement:
      next1 = gameState.generateSuccessor(0,i)
      now = min_value(next1,1, 0)
      if now >= max2:
        best = i
        max2 = now
    return best


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def max_value(gameState, agentIndex, level,a,b):
      if level == self.depth:
        return self.evaluationFunction(gameState)
      movements = gameState.getLegalActions(agentIndex)
      # none successor, stay
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      max1 = float('-inf')
      for i in movements:
        next = gameState.generateSuccessor(agentIndex, i)
        now = min_value(next, agentIndex + 1, level,a, b)
        if now >= max1:
          max1 = now
        #above is to get the max value of successors right now
        if max1 >= b:
          return max1
        #stop finding the useless steps
        if max1 >= a:
          a = max1
      return max1

    def min_value(gameState, agentIndex, level,a,b):
      if level == self.depth:
        return self.evaluationFunction(gameState)
      min1 = float('inf')
      movements = gameState.getLegalActions(agentIndex)

      # none successor, stay
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      for i in movements:
        next = gameState.generateSuccessor(agentIndex, i)
        # last ghost choose
        if agentIndex == gameState.getNumAgents() - 1:
          now = max_value(next, 0, level + 1,a,b)
          # first ghost - (last-1) ghost choose
        else:
          now = min_value(next, agentIndex + 1, level,a ,b)
        if now <= min1:
          min1 = now
        if min1 <= a:
          return min1
        if min1 <= b:
          b = min1
      return min1

    a = float("-inf") # max's best option in the whole game, the biggest
    b = float("inf")  # min's best option in the whole game, the smallest


    # none successor, stay
    movements = gameState.getLegalActions(0)
    max2 = float('-inf')
    for i in movements:
      next1 = gameState.generateSuccessor(0, i)
      now = min_value(next1,  1, 0, a, b)
      if now >= max2:
        max2 = now
        nice_move = i
      # above is to get the max value of successors right now
      if max2 >= b:
        return max2
      # stop finding the useless steps
      if max2 >= a: # update the value
        a = max2
    return nice_move


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
    def max_value(gameState, agentIndex, level):

      if level == self.depth:
        return self.evaluationFunction(gameState)
      max1 = float('-inf')
      movements = gameState.getLegalActions(agentIndex)

      # none successor, stay
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      for i in movements:
        next = gameState.generateSuccessor(agentIndex, i)
        now = min_value(next,agentIndex+1,level)
        if now >= max1:
          max1 = now

      return max1

    def min_value(gameState, agentIndex ,level):
      all_value = 0
      if level == self.depth:
        return self.evaluationFunction(gameState)

      movements = gameState.getLegalActions(agentIndex)

      # none successor, stay
      if gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

      for i in movements:
        next = gameState.generateSuccessor(agentIndex, i)
        #last ghost choose
        if agentIndex == gameState.getNumAgents()-1:
          now = max_value(next,0,level+1)
          #first ghost - (last-1) ghost choose
        else:
          now = min_value(next, agentIndex+1,level)
        all_value = all_value + now
      length = len(movements)

      random_value = float(all_value)/float(length)
      return random_value


    # none successor, stay
    movements = gameState.getLegalActions(0)
    max2 = float('-inf')
    for i in movements:
      next1 = gameState.generateSuccessor(0, i)
      now = min_value(next1,  1, 0,)
      if now >= max2:
        max2 = now
        nice_move = i
      # above is to get the max value of successors right now
    return nice_move

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    use current score
  """
  "*** YOUR CODE HERE ***"

  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  food_list = newFood.asList()
  distance_ghost = []
  min_distance1 = float(0)

  for ghost in newGhostStates:
    distance_ghost.append(absoluteDistance(newPos, ghost.getPosition()))
    min_distance1 = min(distance_ghost)
  # be away from the ghost
  if min_distance1 < 1:
    return -10000000

  distance_food1 = [1,]

  # push the pacman to move
  for food in food_list:
    distance_food1.append(absoluteDistance(newPos, food))
  avgerage = sum(distance_food1) / float(len(distance_food1))
  #calculate the distance
  min_distance2 = float(0)
  distance_food = []
  for food in food_list:
    if absoluteDistance(newPos, food) != 0:
      distance_food.append(absoluteDistance(newPos, food))
      min_distance2 = min(distance_food)
  a = min_distance2 + 1
  #
  notScared = float(0)
  for i in newScaredTimes:
    if i == 0:
      notScared += 1
  leng = len(newGhostStates)
  return  0.4*currentGameState.getScore() + 1.0/a +1.0/avgerage-1.0/(min_distance1+1)-20*notScared-200*leng
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    newPos = gameState.getPacmanPosition()
    newFood = gameState.getFood()
    newGhostStates = gameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    food_list = newFood.asList()
    distance_ghost = []
    min_distance1 = float(0)

    for ghost in newGhostStates:
      distance_ghost.append(absoluteDistance(newPos, ghost.getPosition()))
      min_distance1 = min(distance_ghost)
    # be away from the ghost
    if min_distance1 < 1:
      return -10000000

    distance_food1 = [1, ]

    # push the pacman to move
    for food in food_list:
      distance_food1.append(absoluteDistance(newPos, food))
    avgerage = sum(distance_food1) / float(len(distance_food1))

