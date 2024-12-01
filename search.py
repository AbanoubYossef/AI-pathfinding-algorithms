# search.py
#-------------------------------------------------------------------------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#-------------------------------------------------------------------------------------
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
#-------------------------------------------------------------------------------------
from util import Stack,Queue,PriorityQueue


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

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


def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
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
    stack  = Stack()
    start_state = problem.getStartState()# first point in my graph 
    stack .push((start_state,[]))
    
    marked= set() #uniqe set for not adding the point more than one time 
    while not stack .isEmpty():
        current_state, path = stack .pop()
        if current_state not in marked:
            marked.add(current_state)
            
            if problem.isGoalState(current_state):
                return path
            # Explore neighbors
            for successor, action, step_cost in problem.getSuccessors(current_state):
                if successor not in marked:
                    stack .push((successor, path + [action]))
    
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    queue =Queue()
    start_state = problem.getStartState()# first point in my graph 
    queue.push((start_state,[]))
    
    marked= set() #uniqe set for not adding the point more than one time 
    while not queue.isEmpty():
        current_state, path = queue.pop()
        if current_state not in marked:
            marked.add(current_state)
            
            if problem.isGoalState(current_state):
                return path
            # Explore neighbors
            for successor, action, step_cost in problem.getSuccessors(current_state):
                if successor not in marked:
                    queue.push((successor, path + [action]))
    
    util.raiseNotDefined()
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    priority_queue = PriorityQueue()
    start_state = problem.getStartState()# first point in my graph 
    priority_queue.push((start_state,[],0),0)
    
    marked= dict() 
    while not priority_queue.isEmpty():
        current_state, path, current_cost = priority_queue.pop()
        
        if problem.isGoalState(current_state):
            return path
        
        if current_state not in marked or current_cost < marked[current_state]:
            marked[current_state] = current_cost
            # Explore neighbors
            for successor, action, step_cost in problem.getSuccessors(current_state):
                new_cost = current_cost + step_cost
                if successor not in marked or new_cost < marked[successor]:
                    priority_queue.push((successor, path + [action], new_cost), new_cost)
    
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    # Priority Queue to hold nodes and their cost
    priority_queue = PriorityQueue()
    start_state = problem.getStartState()
    # Initialize the priority queue with the start state, an empty path, and a cost of 0
    priority_queue.push((start_state, [], 0), heuristic(start_state, problem))
    
    # To keep track of visited nodes and the cost of reaching them
    marked = dict() 
    
    while not priority_queue.isEmpty():
        # Pop the node with the lowest f value (f = g + h)
        current_state, path, current_cost = priority_queue.pop()
        
        # If the current state is the goal, return the path
        if problem.isGoalState(current_state):
            return path
        
        # Mark the node as visited only if we have not visited it before or we have a cheaper path to it
        if current_state not in marked or current_cost < marked[current_state]:
            marked[current_state] = current_cost
            
            # Explore neighbors
            for successor, action, step_cost in problem.getSuccessors(current_state):
                # Calculate the new cost to reach the successor
                new_cost = current_cost + step_cost
                # Calculate the heuristic value for the successor
                heuristic_cost = heuristic(successor, problem)
                # Calculate the total cost (f = g + h)
                total_cost = new_cost + heuristic_cost
                
                # Push the successor to the priority queue with its cost and updated path
                if successor not in marked or new_cost < marked[successor]:
                    priority_queue.push((successor, path + [action], new_cost), total_cost)
    
    # If no solution is found, raise an error (or return an empty list depending on the requirement)
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
