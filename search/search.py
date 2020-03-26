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
    actions = []
    goal = (0,0)
    visited = []
    stack = util.Stack()
    
    if problem.isGoalState(problem.getStartState()):
        return actions
    visited.append(problem.getStartState())
    nextStates = problem.getSuccessors(problem.getStartState())
    for x in nextStates:
        node = (x,0)
        stack.push(node)
    while not stack.isEmpty():
        state = stack.pop()
        visited.append(state[0][0])
        if problem.isGoalState(state[0][0]):
            goal = state
            break
        for y in problem.getSuccessors(state[0][0]):
            if not y[0] in set(visited):
                stack.push((y,state))
    while(not goal == 0):
        state = goal[0]
        actions.append(state[1])
        goal=goal[1]
    actions.reverse()
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    actions = []
    goal = (0,0)
    visited = []
    queue = util.Queue()
    
    if problem.isGoalState(problem.getStartState()):
        return actions
    visited.append(problem.getStartState())
    nextStates = problem.getSuccessors(problem.getStartState())
    for x in nextStates:
        visited.append(x[0])
        node = (x,0)
        queue.push(node)
    while not queue.isEmpty():
        state = queue.pop()
        if problem.isGoalState(state[0][0]):
            goal = state
            break
        for y in problem.getSuccessors(state[0][0]):
            if not y[0] in visited:
                queue.push((y,state))
                visited.append(y[0])

    while(not goal == 0):
        state = goal[0]
        actions.append(state[1])
        goal=goal[1]
    actions.reverse()
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    actions = []
    goal = 0
    visited = []
    found = False
    queue = util.PriorityQueue()
    
    if problem.isGoalState(problem.getStartState()):
        return actions
    visited.append(problem.getStartState())
    nextStates = problem.getSuccessors(problem.getStartState())
    states = []
    keep = []
    for i in range(len(nextStates)):
        if(nextStates[i][0] in states):
            index = states.index(nextStates[i][0])
            if(nextStates[i][2]<nextStates[index][2]):
                states[index] = 0
                keep[index] = 0
        else:
            states.append(nextStates[i][0])
            keep.append((nextStates[i],0))
    filter(lambda a: a != 0, keep)
    filter(lambda a: a != 0, states)
    for x in keep:
        queue.push(x,x[0][2])    
    while not queue.isEmpty():
        state = queue.pop()
        visited.append(state[0][0])
        if problem.isGoalState(state[0][0]):
            goal = state
            found = True
            break
        if(found):
            break
        for y in problem.getSuccessors(state[0][0]):
            if not y[0] in set(visited):
                subact = [y[1]]
                a = state
                while(not a == 0):
                    b = a[0]
                    subact.append(b[1])
                    a=a[1]
                subact.reverse()
                cost = problem.getCostOfActions(subact)
                if(y[0] in states):
                    i = states.index(y[0])
                    ss = []
                    a = keep[i]
                    while(not a == 0):
                        b = a[0]
                        ss.append(b[1])
                        a=a[1]
                    ss.reverse()
                    prevcost = problem.getCostOfActions(ss)
                    if(cost<prevcost):
                        queue.push((y,state),cost)
                else:
                    queue.push((y,state),cost)
                    states.append(y[0])
                    keep.append((y,state))
    while(not goal == 0):
        state = goal[0]
        actions.append(state[1])
        goal=goal[1]
    actions.reverse()
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    actions = []
    goal = 0
    visited = []
    found = False
    queue = util.PriorityQueue()
    
    if problem.isGoalState(problem.getStartState()):
        return actions
    visited.append(problem.getStartState())
    nextStates = problem.getSuccessors(problem.getStartState())
    states = []
    keep = []
    for i in range(len(nextStates)):
        if(nextStates[i][0] in states):
            index = states.index(nextStates[i][0])
            if(nextStates[i][2]+heuristic(nextStates[i][0])<nextStates[index][2]
               +heuristic(nextStates[index][0],problem)):
                states[index] = 0
                keep[index] = 0
        else:
            states.append(nextStates[i][0])
            keep.append((nextStates[i],0))
    filter(lambda a: a != 0, keep)
    filter(lambda a: a != 0, states)
    for x in keep:
        queue.push(x,x[0][2]+heuristic(x[0][0],problem))    
    while not queue.isEmpty():
        state = queue.pop()
        visited.append(state[0][0])
        if problem.isGoalState(state[0][0]):
            goal = state
            found = True
            break
        if(found):
            break
        for y in problem.getSuccessors(state[0][0]):
            if not y[0] in visited:
                subact = [y[1]]
                a = state
                while(not a == 0):
                    b = a[0]
                    subact.append(b[1])
                    a=a[1]
                subact.reverse()
                cost = problem.getCostOfActions(subact)+heuristic(y[0],problem)
                if(y[0] in states):
                    i = states.index(y[0])
                    ss = []
                    a = keep[i]
                    while(not a == 0):
                        b = a[0]
                        ss.append(b[1])
                        a=a[1]
                    ss.reverse()
                    prevcost = problem.getCostOfActions(ss)+heuristic(keep[i][0][0],problem)
                    if(cost<prevcost):
                        queue.push((y,state),cost)
                else:
                    queue.push((y,state),cost)
                    states.append(y[0])
                    keep.append((y,state))
    while(not goal == 0):
        state = goal[0]
        actions.append(state[1])
        goal=goal[1]
    actions.reverse()
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
