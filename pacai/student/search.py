"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import *
from pacai.core.actions import *

"""
i think the issue is that rn i have frontier as a list/stack of coordinates, but it looks like the pacman
wants it as a list of directions?? cus it goes through directionToVector.
problem.startingState() returns the coordinates. which i do need, so i can check if i've gone there before.
i think i'll use path to record the corresponding directions, and then at the end that's what i'll return

ok another thing i don't understand is that dfs 
so the explored nodes are the ones that have been pospped off the stack. but what happens if it goes down a route but ends in a dead end? all of those nodes have already been added to explored. since the algorithm avoids going to nodes that it's already been before, it abruptly jumps from the dead end to the other choice node in that intersection. so how do i get the actual path? i feel like this is something i've learned...
i suppose dfs isn't the most optimal path so this is ok. maybe like.. if it runs into a dead end, it'll delete nodes (in explored) until it gets to a node that does have an alternate route? ah but i would have to do this in path, so explored can tell us that we've laready visited that dead path. (is tis right?)

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


# make continuous  will be different
# instead of stack it'll be queue
# extracting the path will be different
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
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


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # *** Your Code Here ***
    raise NotImplementedError()
