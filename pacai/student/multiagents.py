import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core import distance

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.

        """


        # Useful information you can extract.
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***

        # find dist to nearest food
        foodDist = 10000
        for food in oldFood.asList():
            foodDist = min(foodDist, distance.manhattan(newPosition, food)+1)
        score = 1/foodDist * 10
        
        # find dist to nearest ghost, find scareTimer of that nearest ghost
        ghostDist = 10000
        scaredTimer = 0
        for ghostState in newGhostStates:
            ghostPos = (int(ghostState.getPosition()[0]), int(ghostState.getPosition()[1]))
            if ghostDist > distance.manhattan(newPosition, ghostPos)+1:
                ghostDist = distance.manhattan(newPosition, ghostPos)+1
                scaredTimer = ghostState.getScaredTimer()
        
        if scaredTimer > 0:
            # if it's possible to catch up to them, then head in their direction
            if ghostDist < scaredTimer:
                score += 1/ghostDist * 50
        else:
            if ghostDist < 3:
                score -= 1/ghostDist * 30

        return score

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        actions = gameState.getLegalActions()
        actions.remove('Stop')
        bestVal = -10000
        bestAction = ''
        for action in actions:
           val = self.minVal(gameState.generateSuccessor(0, action), 0)
           if val > bestVal:
               bestVal = val
               bestAction = action
        
        return bestAction

    def maxVal(self, gameState, depth):
        if depth >= self.getTreeDepth() or gameState.isOver():
            return self.getEvaluationFunction()(gameState)
        val = -100000  # is this ok for negative infinite?
        
        actions = gameState.getLegalActions()
        actions.remove('Stop')
        for action in actions:
            val = max(val, self.minVal(gameState.generateSuccessor(0, action), depth+1))
        print("maxVal, depth", depth, "val:", val)
        return val

    def minVal(self, gameState, depth):
        if depth >= self.getTreeDepth() or gameState.isOver():
            return self.getEvaluationFunction()(gameState)
        val = 100000  # is this ok for infinite?
        
        for agentIndex in range(1, gameState.getNumAgents()):
            actions = gameState.getLegalActions(agentIndex=agentIndex)
            for action in actions:
                val = min(val, self.maxVal(gameState.generateSuccessor(agentIndex, action), depth+1))
        print("minVal, depth", depth, "val:", val)
        return val

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
