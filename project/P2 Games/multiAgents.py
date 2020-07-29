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
import math
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
        """ Strategy:
        1) Distance metric: compute difference of total distance to foods in new state and current state
           and take reciprocal
        2) Ghost metric: distance to ghost
        3) evaluationFuction: distance metric + ghost metric
        """
        currentPos = currentGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()
        
        newDistanceToFoods = 0
        for x in range(newFood.width):
            for y in range(newFood.height):
                if newFood[x][y]:
                    newDistanceToFoods += math.sqrt(math.pow(newPos[0]-x, 2) + math.pow(newPos[1]-y, 2))
        foodMetric = 1/abs(1+newDistanceToFoods)

        distanceToGhosts = 0
        for ghostState in newGhostStates:
            ghostPosition = ghostState.getPosition()
            distanceToGhosts += math.sqrt(math.pow(newPos[0]-ghostPosition[0],2) + math.pow(newPos[1]-ghostPosition[1],2))
        if distanceToGhosts > math.sqrt(4):
            ghostMetric = 0
        else:
            ghostMetric = -abs(foodMetric)*2
        if action == Directions.STOP:
            return -100
        return successorGameState.getScore() + foodMetric + ghostMetric

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
    @staticmethod
    def isPacman(agentIndex):
        return agentIndex == 0

    """
    Return best value and the corresponding action 
    """
    @staticmethod
    def computeMiniMax(agentIndex, gameState, remainSteps):
        if gameState.isWin() or gameState.isLose() or remainSteps==0:
            return scoreEvaluationFunction(gameState), Directions.STOP
        if MinimaxAgent.isPacman(agentIndex): # pacman selects max score in successor
            return MinimaxAgent.computeMax(agentIndex, gameState, remainSteps)
        else:                                 # ghost selects min score in successor
            return MinimaxAgent.computeMin(agentIndex, gameState, remainSteps)

    @staticmethod
    def computeMax(agentIndex, gameState, remainSteps):
        v = -math.inf
        a = Directions.STOP
        successorIndex = (agentIndex+1)%gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            s = MinimaxAgent.computeMiniMax(successorIndex, successorGameState, remainSteps-1)
            if v < s[0]:
                v = s[0]
                a = action
        return v,a

    @staticmethod
    def computeMin(agentIndex, gameState, remainSteps):
        v = math.inf
        a = Directions.STOP
        successorIndex = (agentIndex+1)%gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            s = MinimaxAgent.computeMiniMax(successorIndex, successorGameState, remainSteps-1)
            if v > s[0]:
                v = s[0]
                a = action
        return v,a
        
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        value, action = MinimaxAgent.computeMiniMax(self.index, gameState, gameState.getNumAgents()*self.depth)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    @staticmethod
    def isPacman(agentIndex):
        return agentIndex == 0
    
    """
    Return best value and the corresponding action of a game state
    """
    @staticmethod
    def computeAlphaBeta(agentIndex, gameState, alpha, beta, remainSteps):
        if gameState.isWin() or gameState.isLose() or remainSteps==0:
            return scoreEvaluationFunction(gameState), Directions.STOP
        if AlphaBetaAgent.isPacman(agentIndex): # pacman selects max score in successors
            return AlphaBetaAgent.computeMax(agentIndex, gameState, alpha, beta, remainSteps)
        else:                                  # ghost select min score in successors
            return AlphaBetaAgent.computeMin(agentIndex, gameState, alpha, beta, remainSteps)

    @staticmethod
    def computeMax(agentIndex, gameState, alpha, beta, remainSteps):
        v = -math.inf
        a = Directions.STOP
        successorIndex = (agentIndex+1)%gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            s = AlphaBetaAgent.computeAlphaBeta(successorIndex, successorGameState, alpha, beta, remainSteps-1)
            if v < s[0]:
                v = s[0]
                a = action
            if v > beta:
                return v,a
            alpha = max(alpha, v)            
        return v,a

    @staticmethod
    def computeMin(agentIndex, gameState, alpha, beta, remainSteps):
        v = math.inf
        a = Directions.STOP
        successorIndex = (agentIndex+1)%gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            s = AlphaBetaAgent.computeAlphaBeta(successorIndex, successorGameState, alpha, beta, remainSteps-1)
            if v > s[0]:
                v = s[0]
                a = action
            if v < alpha:
                return v,a
            beta = min(beta, v)
        return v,a

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value, action = AlphaBetaAgent.computeAlphaBeta(self.index, gameState, -math.inf, math.inf, gameState.getNumAgents()*self.depth)
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    @staticmethod
    def isPacman(agentIndex):
        return agentIndex==0

    """
    Return best value and the corresponding action of a game state
    """
    @staticmethod
    def computeExpectimax(agentIndex, gameState, remainSteps):
        if gameState.isWin() or gameState.isLose() or remainSteps==0:
            return scoreEvaluationFunction(gameState), Directions.STOP
        if ExpectimaxAgent.isPacman(agentIndex):
            return ExpectimaxAgent.computeMax(agentIndex, gameState, remainSteps)
        else:
            return ExpectimaxAgent.computeExpectation(agentIndex, gameState, remainSteps)
    
    @staticmethod
    def computeMax(agentIndex, gameState, remainSteps):
        v = -math.inf
        a = Directions.STOP
        successorIndex = (agentIndex+1)%gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            s = ExpectimaxAgent.computeExpectimax(successorIndex, successorGameState, remainSteps-1)
            if v < s[0]:
                v = s[0]
                a = action
        return v,a

    @staticmethod
    def computeExpectation(agentIndex, gameState, remainSteps):
        v = 0
        cnt = 0
        successorIndex = (agentIndex+1)%gameState.getNumAgents()
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            s = ExpectimaxAgent.computeExpectimax(successorIndex, successorGameState, remainSteps-1)
            v += s[0]
            cnt += 1
        return v/cnt, Directions.STOP # expectation node does not pick action, just assignment an arbitrary action to ensure correct syntax

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        value, action = ExpectimaxAgent.computeExpectimax(self.index, gameState, self.depth*gameState.getNumAgents())
        return action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    """ Strategy:
    1) Distance metric: compute difference of total distance to foods in new state and current state
        and take reciprocal
    2) Ghost metric: distance to ghost
    3) evaluationFuction: distance metric + ghost metric
    """
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    
    newDistanceToFoods = 0
    for x in range(newFood.width):
        for y in range(newFood.height):
            if newFood[x][y]:
                newDistanceToFoods += math.sqrt(math.pow(newPos[0]-x, 2) + math.pow(newPos[1]-y, 2))
    foodMetric = 1/abs(1+newDistanceToFoods)

    distanceToGhosts = 0
    for ghostState in newGhostStates:
        ghostPosition = ghostState.getPosition()
        distanceToGhosts += math.sqrt(math.pow(newPos[0]-ghostPosition[0],2) + math.pow(newPos[1]-ghostPosition[1],2))
    if distanceToGhosts > math.sqrt(4):
        ghostMetric = 0
    else:
        ghostMetric = -abs(foodMetric)*2
    if action == Directions.STOP:
        return -100
    return successorGameState.getScore() + foodMetric + ghostMetric

# Abbreviation
better = betterEvaluationFunction