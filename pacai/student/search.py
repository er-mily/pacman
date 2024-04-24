"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import *
from pacai.util.queue import *
from pacai.util.priorityQueue import *
from pacai.core.actions import *

"""
    - goes to one corner, then stops since it thinks its reached its goal
    - isGoal for CornerProblem checks if pacman has visited all four corners in isGoal. so what happens is it has explored all four corners, but the path only contains teh nodes from the start to the last corner.
    - not sure how to fix this (its same issue for q5)
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
                    #print(path)
                    directions = [Actions.vectorToDirection((path[i+1][0]-path[i][0], path[i+1][1]-path[i][1])) for i in range(0, len(path)-1)]
                    #print(directions)
                    
                    return directions
                frontier.push(coord)


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    frontier = Queue()
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
                new_path = path + [direction]  # dunno
                frontier.push((new_pos, new_path))


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
#queue
#visisted =[]
#cost=0
#push ((position, [], cost), cost)
#while pq
    #pos, path, orig_cost = pq.pop()
    #append to visited
    #if position is goal
        #return path
    #get successor states
    #iterate through successors (for new_pos, path, cost in succ)
        #if new_pos not in visited
            #append to visited
            #new_path = 
            #new_cost = 
            #push to pq

    frontier = PriorityQueue()
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

    frontier = PriorityQueue()
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
                new_cost = orig_cost + cost + heuristic(new_pos, problem)
                frontier.push((new_pos, new_path, new_cost), new_cost)

