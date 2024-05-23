from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection
from pacai.util import probability
import random

# QUESTIONS
# foro #6, how do i know that the policy is optimal? i think it's supposed to cross the bridge
# from left -> right

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.values = {}

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """

        return self.values.get((state, action), 0.0)

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        maxVal = 0
        for i, action in enumerate(self.getLegalActions(state)):
            q = self.getQValue(state, action)
            if i == 0:
                maxVal = q
            else:
                maxVal = max(q, maxVal)
        return maxVal

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """
        maxVal = 0
        maxAction = None
        for i, action in enumerate(self.getLegalActions(state)):
            q = self.getQValue(state, action)
            if i == 0:
                maxVal = q
                maxAction = action
            else:
                if q > maxVal:
                    maxVal = q
                    maxAction = action

        return maxAction

    def getAction(self, state):
        """
        Compute the action to take in the current state.
        With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
        we should take a random action and take the best policy action otherwise.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should choose None as the action.
        """
        # [EPISILON] chance --> random action
        if probability.flipCoin(self.getEpsilon()):
            actions = self.getLegalActions(state)
            if len(actions) == 0:
                return None
            return random.choice(self.getLegalActions(state))
        else:  # follow the policy
            return self.getPolicy(state)
    
    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a state transition and reward.
        You should do your Q-Value update here.
        Note that you should never call this function, it will be called on your behalf.
        """
        a = self.getAlpha()
        d = self.getDiscountRate()

        # a(new) + (1-a)(old)
        self.values[(state, action)] = (a * (reward + d * self.getValue(nextState))) +\
        ((1 - a) * self.getQValue(state, action))


class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action


class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    DESCRIPTION: <Write something here so we know what you did.>
    """

    def __init__(self, index, 
        extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.
        self.weights = {}

    def final(self, state):
        """
        Called at the end of each game.
        .. what is this supposed to do ?
        is it supposed to return anything? the parent final() doesn't return anything so..
        maybe it's just for debugging?
        """

        # Call the super-class final method.
        super().final(state)

        # Did we finish training?
        if self.episodesSoFar == self.numTraining:
            # You might want to print your weights here for debugging.
            # *** Your Code Here ***
            print("done training!")

            # raise NotImplementedError()

    def getQValue(self, state, action):
        """
        `QLearningAgent.getQValue`:
        Should return `Q(state, action) = w * featureVector`,
        where `*` is the dotProduct operator.
        if weights are empty, it should be 1
        """
        dotProd = 0
        features = self.featExtractor.getFeatures(state, state, action)
        for feature in features.keys():
            dotProd += features[feature] * self.weights.get(feature, 1.0)
        return dotProd

    def update(self, state, action, nextState, reward):
        """
        Should update your weights based on transition.
        """
        features = self.featExtractor.getFeatures(state, state, action)
        print("update: features", features)
        a = self.getAlpha()
        d = self.getDiscountRate()
        for feature in features.keys():
            if feature not in self.weights.keys():
                self.weights[feature] = 0
            self.weights[feature] += a * (reward + d * self.getValue(nextState) \
            - self.getQValue(state, action)) * features[feature]
