# myAgents.py
# ---------------
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

from game import Agent
from game import Directions
from searchProblems import PositionSearchProblem
import math
import util
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent2'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

"""
Strategy:
1）Put constraints on bfs, different pacman assign different segments of dots to eat, except at the fringe of segments
2) After all dots are collected in a segment, allow the agent to collect other dots in other segment
3）Use a buffer to cache bfs actions, call bfs only when buffer is empty
"""
class MyAgent2(Agent):
    
    def inSegment(self,x,y,gameState):
        segmentSize = math.ceil(gameState.getFood().width/gameState.getNumAgents())
        return x>=0.9*self.index*segmentSize and x<=(self.index+1.1)*segmentSize #allow some overlaps between segments

    def customBfs(self, problem, gameState):
        from util import Queue
        visitedPositions = set()
        visitedPositions.add(gameState.getPacmanPosition(self.index))
        stateQueue = Queue()
        stateQueue.push((gameState.getPacmanPosition(self.index),[]))
        while not stateQueue.isEmpty():
            currPos,currRoute = stateQueue.pop()
            if problem.isGoalState(currPos) and (self.inSegment(currPos[0], currPos[1], gameState) or self.finishCollect):
                return currRoute
            successors = problem.getSuccessors(currPos)
            for i in range(len(successors)):
                nextState,action,cost = successors[i]
                if nextState not in visitedPositions:
                    visitedPositions.add(nextState)
                    newRoute = currRoute.copy()
                    newRoute.append(action)
                    stateQueue.push((nextState,newRoute))
        return None

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        "*** YOUR CODE HERE ***"
        if not self.actionBuff.isEmpty():
            return self.actionBuff.pop()
        problem = AnyFoodSearchProblem(state, self.index) 
        route = self.customBfs(problem,state)
        if route is None: # all dots in the segment are collected
            self.finishCollect = True
            return Directions.STOP
        #fill up buffer
        for step in route:
            self.actionBuff.push(step)
        return self.actionBuff.pop()
    
    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        "*** YOUR CODE HERE"  
        self.finishCollect=False
        self.actionBuff=util.Queue()

"""
Strategy: 
1） Put constraints on bfs, different pacman assign different segments of dots to eat, except at the fringe of segments
2） Use a buffer to cache bfs actions, call bfs only when buffer is empty
"""
class MyAgent(Agent):
    
    def inSegment(self,x,y,gameState):
        segmentSize = math.ceil(gameState.getFood().width/gameState.getNumAgents())
        return x>=0.9*self.index*segmentSize and x<=(self.index+1.1)*segmentSize #allow some overlaps between segments

    def customBfs(self, problem, gameState):
        from util import Queue
        visitedPositions = set()
        visitedPositions.add(gameState.getPacmanPosition(self.index))
        stateQueue = Queue()
        stateQueue.push((gameState.getPacmanPosition(self.index),[]))
        while not stateQueue.isEmpty():
            currPos,currRoute = stateQueue.pop()
            if problem.isGoalState(currPos) and self.inSegment(currPos[0], currPos[1], gameState):
                return currRoute
            successors = problem.getSuccessors(currPos)
            for i in range(len(successors)):
                nextState,action,cost = successors[i]
                if nextState not in visitedPositions:
                    visitedPositions.add(nextState)
                    newRoute = currRoute.copy()
                    newRoute.append(action)
                    stateQueue.push((nextState,newRoute))
        return None

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        "*** YOUR CODE HERE ***"
        if self.finishCollect:
            return Directions.STOP
        if not self.actionBuff.isEmpty():
            return self.actionBuff.pop()
        problem = AnyFoodSearchProblem(state, self.index) 
        route = self.customBfs(problem,state)
        if route is None: # all dots in the segment are collected
            self.finishCollect = True
            return Directions.STOP
        #fill up buffer
        for step in route:
            self.actionBuff.push(step)
        return self.actionBuff.pop()
    
    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        "*** YOUR CODE HERE"  
        self.finishCollect=False
        self.actionBuff=util.Queue()

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)
        "*** YOUR CODE HERE ***"
        return search.breadthFirstSearch(problem)

    def getAction(self, state):
        #print('index: ',self.index,' state: ',state.getPacmanState(self.index))
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        "*** YOUR CODE HERE ***"
        return self.food[x][y]