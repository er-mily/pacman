"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import *
from pacai.util.queue import *
from pacai.util.priorityQueue import *
from pacai.core.actions import *

"""

"""


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
    # will this change the arr inputted?? i feel like not
    def makeContinuous(path):
        if len(path) == 1:
            return
        node = path.pop()
        while True:
            last_node = path.pop()
            if abs(node[0]-last_node[0]) + abs(node[1]-last_node[1]) == 1:
                path.append(last_node)
                path.append(node)
                return


    # *** Your Code Here ***
    #print("Start: %s" % (str(problem.startingState())))
    #print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    #print("Start's successors: %s" % (problem.successorStates(problem.startingState())))

    node = problem.startingState()
    if problem.isGoal(node):
        return []  # empty list cus it's already complete?
    frontier = Stack() 
    frontier.push(node)
    explored = []
    path = []

    while True:
        if frontier.isEmpty():
            return  # failure... don't return anything
        node = frontier.pop()
        explored.append(node)
        path.append(node)
        makeContinuous(path)
        for successor_state in problem.successorStates(node):
            coord, direction, cost = successor_state
            if coord not in explored:  # not sure if this will work for set.. also check frontier??
                if problem.isGoal(coord):
                    path.append(coord)
                    print(path)
                    directions = [Actions.vectorToDirection((path[i+1][0]-path[i][0], path[i+1][1]-path[i][1])) for i in range(0, len(path)-1)]
                    print(directions)
                    
                    return directions
                frontier.push(coord)


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***

    def tracePath(explored, parents):
        path = []
        node = (explored[-1], parents[-1])
        path.append(node[0])
        for i in range(len(explored)-1, -1, -1):
            if explored[i] == node[1]:
                node = (explored[i], parents[i])
                path.append(node[0])
            if node[1] is None:
                return path


    node = problem.startingState()
    if problem.isGoal(node):
        return []  # empty list cus it's already complete?
    frontier = Queue() 
    frontier.push((node, None))  # current node, parent (None)
    explored = []
    path = []
    parents = []  # parents[i] is the parent of frontier[i]

    while True:
        if frontier.isEmpty():
            return  # failure... don't return anything
        node = frontier.pop()
        explored.append(node[0])
        parents.append(node[1])
        for successor_state in problem.successorStates(node[0]):
            coord, direction, cost = successor_state
            if coord not in explored: 
                if problem.isGoal(coord):
                    explored.append(coord)
                    parents.append(node[0])
                    path = tracePath(explored, parents)
                    directions = [Actions.vectorToDirection((path[i-1][0]-path[i][0], path[i-1][1]-path[i][1])) for i in range(len(path)-1, 0, -1)]
                    
                    return directions
                frontier.push((coord, node[0]))


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***

    def tracePath(explored, parents):
        path = []
        node = (explored[-1], parents[-1])
        path.append(node[0])
        for i in range(len(explored)-1, -1, -1):
            if explored[i] == node[1]:
                node = (explored[i], parents[i])
                path.append(node[0])
            if node[1] is None:
                return path


    node = problem.startingState()
    if problem.isGoal(node):
        return []  # empty list cus it's already complete?
    frontier = PriorityQueue() 
    frontier.push((node, None), 0)  # current node, parent (None)
    explored = []
    path = []
    parents = []  # parents[i] is the parent of frontier[i]

    while True:
        if frontier.isEmpty():
            return  # failure... don't return anything
        node = frontier.pop()
        explored.append(node[0])
        parents.append(node[1])
        for successor_state in problem.successorStates(node[0]):
            coord, direction, cost = successor_state
            if coord not in explored: 
                if problem.isGoal(coord):
                    explored.append(coord)
                    parents.append(node[0])
                    path = tracePath(explored, parents)
                    directions = [Actions.vectorToDirection((path[i-1][0]-path[i][0], path[i-1][1]-path[i][1])) for i in range(len(path)-1, 0, -1)]
                    
                    return directions
                frontier.push((coord, node[0]), cost)

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    def tracePath(explored, parents):
        path = []
        node = (explored[-1], parents[-1])
        path.append(node[0])
        for i in range(len(explored)-1, -1, -1):
            if explored[i] == node[1]:
                node = (explored[i], parents[i])
                path.append(node[0])
            if node[1] is None:
                return path


    node = problem.startingState()
    if problem.isGoal(node):
        return []  # empty list cus it's already complete?
    frontier = PriorityQueue() 
    frontier.push((node, None), 0)  # current node, parent (None)
    explored = []
    path = []
    parents = []  # parents[i] is the parent of frontier[i]

    while True:
        if frontier.isEmpty():
            return  # failure... don't return anything
        node = frontier.pop()
        explored.append(node[0])
        parents.append(node[1])
        for successor_state in problem.successorStates(node[0]):
            coord, direction, cost = successor_state
            if coord not in explored: 
                if problem.isGoal(coord):
                    explored.append(coord)
                    parents.append(node[0])
                    path = tracePath(explored, parents)
                    directions = [Actions.vectorToDirection((path[i-1][0]-path[i][0], path[i-1][1]-path[i][1])) for i in range(len(path)-1, 0, -1)]
                    
                    return directions
                frontier.push((coord, node[0]), cost + heuristic(coord, problem))
