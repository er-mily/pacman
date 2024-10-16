"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util import stack, queue, priorityQueue


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    frontier = stack.Stack()
    visited = []
    frontier.push((problem.startingState(), []))

    while not frontier.isEmpty():
        pos, path = frontier.pop()
        if pos not in visited:  # might not need this
            visited.append(pos)

        if problem.isGoal(pos):
            return path

        for new_pos, direction, cost in problem.successorStates(pos):
            if new_pos not in visited:
                visited.append(new_pos)
                new_path = path + [direction]
                frontier.push((new_pos, new_path))

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    frontier = queue.Queue()
    visited = []
    frontier.push((problem.startingState(), []))\

    while not frontier.isEmpty():
        pos, path = frontier.pop()
        if pos not in visited:  # might not need this
            visited.append(pos)

        if problem.isGoal(pos):
            return path

        for new_pos, direction, cost in problem.successorStates(pos):
            if new_pos not in visited:
                visited.append(new_pos)
                new_path = path + [direction]
                frontier.push((new_pos, new_path))


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    frontier = priorityQueue.PriorityQueue()
    visited = []
    cost = 0
    frontier.push((problem.startingState(), [], 0), 0)

    while not frontier.isEmpty():
        pos, path, orig_cost = frontier.pop()
        if pos not in visited:  # might not need this
            visited.append(pos)

        if problem.isGoal(pos):
            return path

        for new_pos, direction, cost in problem.successorStates(pos):
            if new_pos not in visited:
                visited.append(new_pos)
                new_path = path + [direction]  # dunno
                new_cost = orig_cost + cost
                frontier.push((new_pos, new_path, new_cost), new_cost)


def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***

    frontier = priorityQueue.PriorityQueue()
    visited = []
    cost = 0
    frontier.push((problem.startingState(), [], 0), 0)

    while not frontier.isEmpty():
        pos, path, orig_cost = frontier.pop()
        if pos not in visited:  # might not need this
            visited.append(pos)

        if problem.isGoal(pos):
            return path

        for new_pos, direction, new_cost in problem.successorStates(pos):
            if new_pos not in visited:
                visited.append(new_pos)
                new_path = path + [direction]  # dunno
                cost = orig_cost + new_cost
                frontier.push((new_pos, new_path, cost), cost + heuristic(new_pos, problem))
