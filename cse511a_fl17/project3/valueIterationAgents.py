# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    for x in range(0,iterations):
      all_state = self.mdp.getStates()
      all_value = util.Counter()
      for state in all_state:
        best_value = float("-inf")
        actions = self.mdp.getPossibleActions(state)
        if self.mdp.isTerminal(state):
          continue
        for action in actions:
          value_right_now = self.getQValue(state,action)
          if value_right_now > best_value:
            best_value = value_right_now
        all_value[state] = best_value
      self.values = all_value
      
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    possible_next = self.mdp.getTransitionStatesAndProbs(state,action)
    value = 0
    for i in possible_next:
      nextstate = i[0]
      possibilaty = i[1]
      reward = self.mdp.getReward(state, action, nextstate)
      value = value + possibilaty*(reward + self.discount*(self.values[nextstate]))
    return value  

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    best_value  = float("-inf")
    best_action = None
    actions = self.mdp.getPossibleActions(state)
    for action in actions:
      action_value = self.getQValue(state, action)
      if action_value > best_value:
        best_value = action_value
        best_action = action
    return best_action    
    
  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
