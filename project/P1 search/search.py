# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    route = []
    currRoute = []
    visitedState = set()
    visitedState.add(problem.getStartState())
    depthFirstSearch_helper(problem, problem.getSuccessors(problem.getStartState()), currRoute, route, visitedState)
    return route

def depthFirstSearch_helper(problem, successors, currRoute, route, visitedState):
    for currState,action,cost in successors:
        if currState in visitedState:
            continue
        currRoute.append(action)
        visitedState.add(currState)
        if problem.isGoalState(currState): #If we find a goal, immediately return
            for action in currRoute:
                route.append(action)
            return True
        retval = depthFirstSearch_helper(problem, problem.getSuccessors(currState), currRoute, route, visitedState)
        if retval is True:  #Exit searching if a solution is found
            return True
        currRoute.pop()     #If we reach to this line it means no solution goes through currState, so pop it out
    return False            #If we reach to this line it means solution doesn't live in any of the successors above

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    visitedState = set()
    visitedState.add(problem.getStartState())
    stateQueue = Queue()
    stateQueue.push(problem.getStartState())
    routeQueue = Queue()
    routeQueue.push([])
    while not stateQueue.isEmpty():
        currState = stateQueue.pop()
        currRoute = routeQueue.pop()
        if problem.isGoalState(currState):
            return currRoute
        successors = problem.getSuccessors(currState)
        for i in range(len(successors)):
            nextState,action,cost = successors[i]
            if nextState not in visitedState:
                visitedState.add(nextState)
                stateQueue.push(nextState)
                newRoute = currRoute.copy()
                newRoute.append(action)
                routeQueue.push(newRoute)
    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue, Queue
    startState = problem.getStartState()
    route = []
    visitedState = set()
    visitedState.add(startState)
    pq = PriorityQueue()
    #expand start state into priority queue
    for nextState,action,cost in problem.getSuccessors(startState):
        currRoute = []
        currRoute.append(action)
        pq.push((nextState,currRoute,cost),cost)
    #put the rest of the states into queue
    while not pq.isEmpty():
        state,currRoute,cost = pq.pop()
        if problem.isGoalState(state):
            return currRoute
        if state not in visitedState:
            visitedState.add(state)
            for newState,newAction,newCost in problem.getSuccessors(state):
                newRoute = currRoute.copy()
                newRoute.append(newAction)
                pq.push((newState,newRoute,cost+newCost),cost+newCost) #keep in mind this is cumulative cost
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from searchAgents import manhattanHeuristic
    from util import PriorityQueue, Queue
    startState = problem.getStartState()
    visitedState = set()
    visitedState.add(startState)
    pq = PriorityQueue()
    #expand start state into priority queue
    for nextState,action,cost in problem.getSuccessors(startState):
        currRoute = []
        currRoute.append(action)
        pq.push((nextState,currRoute,cost),cost+heuristic(nextState,problem))
    #put the rest of the states into queue
    while not pq.isEmpty():
        state,currRoute,cost = pq.pop()
        if problem.isGoalState(state):
            return currRoute
        if state not in visitedState:
            visitedState.add(state)
            for newState,newAction,newCost in problem.getSuccessors(state):
                newRoute = currRoute.copy()
                newRoute.append(newAction)
                pq.push((newState,newRoute,cost+newCost),cost+newCost+heuristic(newState,problem)) #keep in mind this is cumulative cost
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
