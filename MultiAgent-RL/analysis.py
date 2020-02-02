# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    """
    Removing noise from the environment/world makes it a straightforward task for the agent as it
    can now walk across the path with confidence of not falling into the pit. This will change the
    Q-values and hence utility values such that the path will have all positive values as there is
    no chance of falling into the pit.
    """
    answerDiscount = 0.9
    answerNoise = 0.0
    return answerDiscount, answerNoise


def question3a():
    """
    Lower discount value decreases the value of the final reward/terminal reward every action the agent takes.
    Hence choosing a earlier but lower reward will optimal rather than a higher but farther reward (which will
    eventually be of a lower value by the time our agent reaches that state.
    """
    answerDiscount = 0.3
    answerNoise = 0
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3b():
    """
    Keeping the discount value same as previous we introduce noise so that our agent does not risk the cliff route
    as the actions are non deterministic and there is a possibility of falling into cliff if it takes the cliff route
    """
    answerDiscount = 0.3
    answerNoise = 0.2
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3c():
    """
    We can keep discount at 1 as we need to reache the farther reward state/terminal.
    We introduce -1 living reward as we want our agent to take the fastest route possible.
    """
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = -1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3d():
    """
    Adding some noise helps our agent take the longer route by avoiding the cliffs as the actions are
    non deterministic and there is a possibility of falling into cliff if it takes the cliff route
    """
    answerDiscount = 1
    answerNoise = 0.4
    answerLivingReward = 0
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question3e():
    """
    Introducing even a small positive living reward makes our agent to not enter the terminal state,
    but to keep exploring and maximize its rewards as it gets a reward for every action it takes
    eventually exceeding that of the terminating state reward.
    """
    answerDiscount = 1
    answerNoise = 0
    answerLivingReward = 0.1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'


def question6():
    answerEpsilon = None
    answerLearningRate = None
    return 'NOT POSSIBLE'
    # If not possible, return 'NOT POSSIBLE'


if __name__ == '__main__':
    print 'Answers to analysis questions:'
    import analysis

    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print '  Question %s:\t%s' % (q, str(response))
