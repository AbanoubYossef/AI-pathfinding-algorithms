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

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        capsules = successorGameState.getCapsules()

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()
        # evaluation = successorGameState.getScore()  
        # capsules = successorGameState.getCapsules()
        # closestFoodDistance = float('inf')
        # closestGhostDistance = float('inf')
        # for food in newFood.asList():
        #     distance = util.manhattanDistance(newPos, food)
        #     if distance < closestFoodDistance:
        #         closestFoodDistance = distance
        # for ghostState in newGhostStates:
        #     ghostPos = ghostState.getPosition()
        #     distance = util.manhattanDistance(newPos, ghostPos)
        #     if distance < closestGhostDistance:
        #         closestGhostDistance = distance
        # evaluation = successorGameState.getScore()  
        # if closestGhostDistance <= 1:
        #     evaluation -= 500 
        # else:
        #     evaluation += 1.0 / (closestFoodDistance + 1)  
        # if newPos in capsules:
        #     evaluation += 500 
        # return evaluation
        # Initialize evaluation score with the successor state score
        evaluation = successorGameState.getScore()
        
        # Distance to closest food
        foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        closestFoodDistance = min(foodDistances) if foodDistances else 0  # Zero if no food left

        # Distance to ghosts
        ghostDistances = [manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates]
        closestGhostDistance = min(ghostDistances)

        # Ghost behavior: scared vs active
        for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
            ghostDistance = manhattanDistance(newPos, ghostState.getPosition())
            if scaredTime > 0:
                # Encourage eating scared ghosts
                evaluation += max(10, 200 - ghostDistance)  # Higher reward for closer scared ghosts
            elif ghostDistance <= 1:
                # Penalize proximity to active ghosts
                evaluation -= 500
        
        # Reward for eating capsules
        if newPos in capsules:
            evaluation += 500

        # Reward for proximity to food
        if closestFoodDistance > 0:
            evaluation += 10 / closestFoodDistance

        # Add penalties for remaining food (encourage clearing the board)
        evaluation -= len(newFood.asList()) * 10

        return evaluation
def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(state, depth, agentIndex):
            # Base case: If depth is 0 or the game is in a terminal state
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None
            
            # Get legal actions for the current agent
            legalActions = state.getLegalActions(agentIndex)
            
            # If no legal actions, return the evaluation of the current state
            if not legalActions:
                return self.evaluationFunction(state), None
            
            # Pacman's turn (maximize)
            if agentIndex == 0:
                bestValue = float("-inf")
                bestAction = None
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value, _ = minimax(successor, depth - 1 if agentIndex == state.getNumAgents() - 1 else depth, 
                                        (agentIndex + 1) % state.getNumAgents())
                    if value > bestValue:
                        bestValue, bestAction = value, action
                return bestValue, bestAction
            
            # Ghosts' turn (minimize)
            else:
                bestValue = float("inf")
                bestAction = None
                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value, _ = minimax(successor, depth - 1 if agentIndex == state.getNumAgents() - 1 else depth, 
                                        (agentIndex + 1) % state.getNumAgents())
                    if value < bestValue:
                        bestValue, bestAction = value, action
                return bestValue, bestAction

        # Start the minimax algorithm with Pacman (agentIndex = 0) and initial depth
        _, bestAction = minimax(gameState, self.depth, 0)
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphaBeta(state, depth, alpha, beta, agentIndex):
            # Base case: stop recursion if depth is 0, or the game state is a win/lose state
            if depth == 0 or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None  # Return the evaluation score and no action
            
            # Pacman's turn (maximizing agent)
            if agentIndex == 0:  
                bestValue = float("-inf")  # Initialize the best value as negative infinity
                for action in state.getLegalActions(agentIndex):  # Loop through all legal actions
                    successor = state.generateSuccessor(agentIndex, action)  # Generate the resulting state after taking the action
                    # Recursively call alphaBeta for the next agent
                    value, _ = alphaBeta(successor, depth - 1, alpha, beta, (agentIndex + 1) % state.getNumAgents())
                    if value > bestValue:  # Update the best value and action if this action leads to a better outcome
                        bestValue = value
                        bestAction = action
                    if bestValue > beta:  # Beta cut-off: stop exploring further as it won't improve the minimizer's outcome
                        return bestValue, bestAction
                    alpha = max(alpha, bestValue)  # Update alpha for the maximizing player
                return bestValue, bestAction  # Return the best value and corresponding action
            
            # Ghost's turn (minimizing agent)
            else:  
                bestValue = float("inf")  # Initialize the best value as positive infinity
                for action in state.getLegalActions(agentIndex):  # Loop through all legal actions
                    successor = state.generateSuccessor(agentIndex, action)  # Generate the resulting state after taking the action
                    # Recursively call alphaBeta for the next agent
                    value, _ = alphaBeta(successor, depth - 1, alpha, beta, (agentIndex + 1) % state.getNumAgents())
                    if value < bestValue:  # Update the best value and action if this action leads to a better outcome
                        bestValue = value
                        bestAction = action
                    if bestValue < alpha:  # Alpha cut-off: stop exploring further as it won't improve the maximizer's outcome
                        return bestValue, bestAction
                    beta = min(beta, bestValue)  # Update beta for the minimizing player
                return bestValue, bestAction  # Return the best value and corresponding action

        # Start the alpha-beta pruning algorithm
        _, bestAction = alphaBeta(gameState, self.depth * gameState.getNumAgents(), float("-inf"), float("inf"), 0)
        return bestAction  # Return the best action for Pacman


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
