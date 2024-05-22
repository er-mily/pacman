"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    I ran the agent on Discount grid with the default values, and in 10/10 episodes it already
    preferred the close exit, risking the cliff. So I didn't change anything here.
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    Since the game will end quick (low discount), it tries to get to an exit as fast as possible, which is why it chooses the closer exit. Since the agent is able to move precisely (noise is 0), it'll choose to take the cliff since it's faster and it's safe.
    """

    answerDiscount = 0.3
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    Since the game will end quick (low discount), it tries to get to an exit as fast as possible, which is why it chooses the closer exit. Since the agent is NOT able to move precisely (noise is 0.2), it'll avoid the cliff since that's safer.
    """

    answerDiscount = 0.3
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    When the agent is able to move precisely (so noise is 0), it doesn't need to worry about accidently falling off the cliff, so it chooses to take that route since it's faster.
    """

    answerDiscount = 0.7
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    Since there is a slight reward for living, the agent is more likely to start by going upwards since it's further away from the cliff.
    """

    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = 0.2

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    I made the living reward very high, so the agent is incentivized to live forever, staying away from the cliffs and never going to either exits.
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 1.0

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    Don't know if (1, 0.8) is right, but the logic is that high epsilon -> it'll try out all the routes, 
    even if they aren't optimal; this helps reinforce the agent's knowledge that the cliff is bad.
    and.. there was no logic behind the learning rate
    
    """

    answerEpsilon = 1.0 # 0.3
    answerLearningRate = 0.8 # 0.5

    return answerEpsilon, answerLearningRate

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
