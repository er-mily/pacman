from pacai.agents.learning.value import ValueEstimationAgent
import copy

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.

        # Compute the values here.
        
        for i in range(self.iters):
            temp = copy.deepcopy(self.values)
            for state in self.mdp.getStates():
                action = self.getAction(state)
                if self.mdp.isTerminal(state):
                    continue
                temp[state] = self.getQValue(state, action)
            self.values = temp

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)

    def getQValue(self, state, action):
        """
        returns the value of the state??
        how is this different from getValue? what is a q value??
        """
        maxq = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            transitionReward = self.mdp.getReward(state, action, nextState)
            qval = prob * (transitionReward + self.discountRate * self.getValue(nextState))
            maxq += qval
        return maxq

    def getPolicy(self, state):
        """
        Returns the best action to take, given the current state
        best action = has the highest q value
        """

        actions = self.mdp.getPossibleActions(state)
        bestAction = ''
        maxQ = -1
        
        if self.mdp.isTerminal(state) or len(actions) == 0:
            return None
        for i, action in enumerate(actions):
            q = self.getQValue(state, action)
            if i == 0:
                maxQ = q
                bestAction = action
                continue
            if q > maxQ:
                maxQ = q
                bestAction = action
        
        return bestAction
