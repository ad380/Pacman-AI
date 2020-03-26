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
        foodDists = []
        score = 0
        foodList = newFood.asList()
        for f in foodList:
            foodDists.append(manhattanDistance(f,newPos))
        ghostDists = []
        for g in newGhostStates:
            ghostDists.append(manhattanDistance(g.getPosition(),newPos))
        minGhost = min(ghostDists)
        if(minGhost>2):
            if(len(foodDists)>0):
                minToFood = min(foodDists)+1
                score = 1/minToFood
        else:
            score = -float('inf')
        return successorGameState.getScore()+2*score

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
        val = MinimaxAgent.max_value(self,gameState,0)
        return val[1]
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
    def max_value(self,gameState,depth):
        if(gameState.isWin() or gameState.isLose() or self.depth<=(depth)):
            return (self.evaluationFunction(gameState),None)
        v = -float('inf')
        u = (-float('inf'),None)
        depth+=1
        for d in gameState.getLegalActions(0):
            val = MinimaxAgent.min_value(self,gameState.generateSuccessor(0,d),depth,1)
            if (val>=v):
                v = val
                u = (v,d)
        return u
    
    def min_value(self,gameState,depth,g):
        if(gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        v = float('inf')
        
        if g==(gameState.getNumAgents()-1):
            for d in gameState.getLegalActions(g):
                val = MinimaxAgent.max_value(self,gameState.generateSuccessor(g,d),depth)[0]
                v = min(v,val)
        else:
            for d in gameState.getLegalActions(g):
                val = MinimaxAgent.min_value(self,gameState.generateSuccessor(g,d),depth,g+1)
                v = min(v,val)
        return v
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        val = AlphaBetaAgent.max_value(self,gameState,0,-float('inf'),float('inf'))
        return val[1]
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
    def max_value(self,gameState,depth,alpha,beta):
        if(gameState.isWin() or gameState.isLose() or self.depth<=(depth)):
            return (self.evaluationFunction(gameState),None)
        v = -float('inf')
        u = (-float('inf'),None)
        depth+=1
        for d in gameState.getLegalActions(0):
            val = AlphaBetaAgent.min_value(self,gameState.generateSuccessor(0,d),depth,alpha,beta,1)
            if (val>=v):
                v = val
                u = (v,d)
            if v>beta:
                return u
            alpha = max(alpha,v)
        return u
    
    def min_value(self,gameState,depth,alpha,beta,g):
        if(gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        v = float('inf')
        
        if g==(gameState.getNumAgents()-1):
            for d in gameState.getLegalActions(g):
                val = AlphaBetaAgent.max_value(self,gameState.generateSuccessor(g,d),depth,alpha,beta)[0]
                v = min(v,val)
                if v < alpha:
                    return v
                beta = min(beta,v)
        else:
            for d in gameState.getLegalActions(g):
                val = AlphaBetaAgent.min_value(self,gameState.generateSuccessor(g,d),depth,alpha,beta,g+1)
                v = min(v,val)
                if v < alpha:
                    return v
                beta = min(beta,v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        val = ExpectimaxAgent.max_value(self,gameState,0)
        return val[1]
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
    def max_value(self,gameState,depth):
        if(gameState.isWin() or gameState.isLose() or self.depth<=(depth)):
            return (self.evaluationFunction(gameState),None)
        v = -float('inf')
        u = (-float('inf'),None)
        depth+=1
        for d in gameState.getLegalActions(0):
            val = ExpectimaxAgent.min_value(self,gameState.generateSuccessor(0,d),depth,1)
            if (val>=v):
                v = val
                u = (v,d)
        return u
    
    def min_value(self,gameState,depth,g):
        if(gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        v = float('inf')
        expect = 0
        count = 0
        for d in gameState.getLegalActions(g):
            count+=1
            if g==(gameState.getNumAgents()-1):
                val = ExpectimaxAgent.max_value(self,gameState.generateSuccessor(g,d),depth)[0]
            else:
                val = ExpectimaxAgent.min_value(self,gameState.generateSuccessor(g,d),depth,g+1)
            expect += val
        expect = expect/count
        return expect

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsules = currentGameState.getCapsules()

    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():  return float("inf")
    if currentGameState.isLose(): return float("-inf")
  
    foodDists = []
    score = 0
    foodList = food.asList()
    for f in foodList:
        foodDists.append(manhattanDistance(f,pos))
    ghostDists = []
    for g in ghostStates:
        ghostDists.append(manhattanDistance(g.getPosition(),pos))
    minGhost = min(ghostDists)
    capsulesD = []
    #for c in capsules:
    #    capsulesD.append(manhattanDistance(c.getPosition(),pos))
    #minCap = min(capsulesD)
    for f in foodList:
        foodDists.append(manhattanDistance(f,pos))
    if(minGhost>2):
        if(len(foodDists)>0):
            minToFood = min(foodDists)+1
            score = 1/minToFood
    else:
        score = -float('inf')
    return currentGameState.getScore()+2*score -3*len(foodList)-50*len(capsules)

# Abbreviation
better = betterEvaluationFunction
