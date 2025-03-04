from pacai.core.directions import Directions
from pacai.agents.capture.reflex import ReflexCaptureAgent

# what features to add to offensive agent?
# to defensive agent?

class OffensiveAgent(ReflexCaptureAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        # dist to nearest enemy
        enemyIndices = self.getOpponents(gameState)
        minDist = float('inf')
        closestGhost = 0
        myPos = successor.getAgentState(self.index).getPosition()
        for enemyIndex in enemyIndices:
            enemyPos = gameState.getAgentPosition(enemyIndex)
            dist = self.getMazeDistance(myPos, enemyPos)
            if dist < minDist:
                minDist = dist
                closestGhost = enemyIndex

        if successor.getAgentState(closestGhost).isScared():
            # if minDist == 1:
            #    features['distanceToEnemy'] = -100
            if minDist < 4:
                features['distanceToEnemy'] = -1 * 1 / minDist
        else:
            if minDist == 0:
                features['distanceToEnemy'] = 100
            elif minDist < 4:
                features['distanceToEnemy'] = 1 / minDist
            else:
                features['distanceToEnemy'] = 0
        # features['distanceToEnemy'] = minDist

        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1,
            'distanceToEnemy': -5,
        }

class DefensiveAgent(ReflexCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        # check if we're scared, and if so stop chasing ghost
        # if myState.isScared():
        #    features['invaderDistance'] *= -1
            # features['numInvaders'] *= -1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -2
        }


def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.agents.capture.offense.OffensiveReflexAgent',
        second = 'pacai.agents.capture.defense.DefensiveReflexAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = OffensiveAgent(firstIndex)
    secondAgent = DefensiveAgent(secondIndex)

    return [
        firstAgent,
        secondAgent
    ]
