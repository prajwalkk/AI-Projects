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
import sys

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"
        if action == Directions.STOP:
            return -1e6
        foodPosition = newFood.asList()

        if len(foodPosition) == 0 or successorGameState.isWin():
            # Pacman Won
            return 1e6

        currentPosition = currentGameState.getPacmanPosition()
        currentFoodPosition = currentGameState.getFood().asList()
        minFoodFromCurrent = min([manhattanDistance(currentPosition, foodPos) for foodPos in currentFoodPosition])

        foodDistance = [manhattanDistance(foodPos, newPos) for foodPos in foodPosition]
        minFoodDistance = min(foodDistance)

        ghostDistance = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        currentDirection = currentGameState.getPacmanState().getDirection()

        # Try not to go near the ghost
        if min(ghostDistance) <= 1:
            return -1e6
        # Try maximising the score at each move
        if scoreEvaluationFunction(successorGameState) > scoreEvaluationFunction(currentGameState):
            return 1e6
        # Go towards nearest food
        if minFoodDistance < minFoodFromCurrent:
            return 1e4
        # Do dame action to reduce thrashing
        if action == currentDirection:
            return 1e3
        # Random action if anything does not occur
        return 1e1


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        """
        "*** YOUR CODE HERE ***"

        def maxValue(agent, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth + 1 == self.depth:
                return self.evaluationFunction(gameState)
            val = -sys.maxint
            if agent == 0:
                successors = [gameState.generateSuccessor(agent, action) for action in gameState.getLegalActions(agent)]
                for successor in successors:
                    nextAgent = agent + 1
                    val = max(val, minValue(nextAgent, depth + 1, successor))
            return val

        def minValue(agent, depth, gameState):
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            val = sys.maxint
            successors = [gameState.generateSuccessor(agent, action) for action in gameState.getLegalActions(agent)]
            for successor in successors:
                if agent == gameState.getNumAgents() - 1:
                    val = min(val, maxValue(0, depth, successor))
                else:
                    nextAgent = agent + 1
                    val = min(val, minValue(nextAgent, depth, successor))
            return val

        actionTaken = max(gameState.getLegalActions(0),
                          key=lambda action: minValue(1, 0, gameState.generateSuccessor(0, action)))
        return actionTaken


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def maxValue(agent, depth, gameState, alpha, beta):
            val = -sys.maxint
            for action in gameState.getLegalActions(agent):
                val = max(val, prune(1, depth, gameState.generateSuccessor(agent, action), alpha, beta))
                if val > beta:
                    return val
                alpha = max(alpha, val)
            return val

        def minValue(agent, depth, gameState, alpha, beta):  # minimizer function
            val = sys.maxint

            nextAgent = agent + 1  # calculate the next agent and increase depth accordingly.
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
                depth += 1

            for newState in gameState.getLegalActions(agent):
                val = min(val, prune(nextAgent, depth, gameState.generateSuccessor(agent, newState), alpha, beta))
                if val < alpha:
                    return val
                beta = min(beta, val)
            return val

        def prune(agent, depth, gameState, alpha, beta):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:  # return the utility in case the defined depth is reached or the game is won/lost.
                return self.evaluationFunction(gameState)

            if agent == 0:  # maximize for pacman
                return maxValue(agent, depth, gameState, alpha, beta)
            else:  # minimize for ghosts
                return minValue(agent, depth, gameState, alpha, beta)

        validAction = None
        currentSore = -sys.maxint
        alpha = -sys.maxint
        beta = sys.maxint
        actions = gameState.getLegalActions(0)
        for action in actions:
            score = prune(1, 0, gameState.generateSuccessor(0, action), alpha, beta)
            if score > currentSore:
                validAction = action
                currentSore = score
            if score > beta:
                return validAction
            alpha = max(alpha, score)
        return validAction


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

        def maxValue(gameState, depth):
            # This is for Pacman only
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)

            successors = [gameState.generateSuccessor(0, action) for action in gameState.getLegalActions(0)]
            val = max(expValue(1, depth + 1, successor) for successor in successors)
            return val

        def expValue(agentIndex, depth, gameState):
            # This method is for Ghosts only
            val = 0
            if gameState.isLose() or gameState.isWin():
                return self.evaluationFunction(gameState)

            # Probability of each action
            actions = gameState.getLegalActions(agentIndex)
            successors = [gameState.generateSuccessor(agentIndex, action) for action in actions]
            # Produce errors if not float
            p = 1 / float(len(actions))
            for successor in successors:
                if agentIndex == gameState.getNumAgents() - 1:
                    # Last Ghost means, next is Pacman and Pacman is a max agent
                    val += maxValue(successor, depth) * p
                else:
                    # Next agent is Ghost
                    val += expValue(agentIndex + 1, depth, successor) * p
            return val

        legalActionsAtRoot = gameState.getLegalActions(0)
        bestAction = max(legalActionsAtRoot, key=lambda action: expValue(1, 1, gameState.generateSuccessor(0, action)))
        return bestAction


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: We can add multiple features like FoodDistance, GhostTimer etc.

      Here we have added the score of only the food distance.
      We return the sum of current game state score and the food distance score which is calculated as follows.
      The maximum out of the reciprocal of manhattan distance of all foods is the score_from_food (feature).
    """
    "*** YOUR CODE HERE ***"

    def scoreFromFood(gameState):
        reciprocalFoodDistance = []
        for food in gameState.getFood().asList():
            reciprocalFoodDistance.append(1.0 / manhattanDistance(gameState.getPacmanPosition(), food))
        if len(reciprocalFoodDistance) > 0:
            return max(reciprocalFoodDistance)
        else:
            return 0

    score = currentGameState.getScore()
    scoreFood = scoreFromFood(currentGameState)
    return score + scoreFood


# Abbreviation
better = betterEvaluationFunction
