# Pac-Man AI Project

## Overview

This project focuses on implementing various search algorithms to create an intelligent Pac-Man agent. The goal is to design an agent that can navigate through a maze, collect all the food dots, and avoid ghosts efficiently. The project explores both uninformed and informed search algorithms, as well as adversarial search techniques to handle the presence of ghosts.

## Table of Contents

1. [Introduction](#introduction)
2. [Uninformed Search Algorithms](#uninformed-search-algorithms)
   - [Depth-First Search (DFS)](#depth-first-search-dfs)
   - [Breadth-First Search (BFS)](#breadth-first-search-bfs)
   - [Uniform Cost Search (UCS)](#uniform-cost-search-ucs)
3. [Informed Search Algorithms](#informed-search-algorithms)
   - [A* Search](#a-search)
   - [Corners Problem](#corners-problem)
   - [Food Heuristic](#food-heuristic)
   - [Suboptimal Search](#suboptimal-search)
4. [Adversarial Search](#adversarial-search)
   - [Reflex Agent](#reflex-agent)
   - [Minimax Algorithm](#minimax-algorithm)
   - [Alpha-Beta Pruning](#alpha-beta-pruning)
5. [Conclusion](#conclusion)

## Introduction

Pac-Man is a classic arcade game where the player controls Pac-Man, who must eat all the dots in a maze while avoiding ghosts. The project aims to create an intelligent Pac-Man agent that can find optimal paths through the maze to achieve the goal state—eating all the dots while avoiding the ghosts in the minimum number of steps.

The project implements several search algorithms, including uninformed search algorithms (DFS, BFS, UCS) and informed search algorithms (A* search). Additionally, multi-agent algorithms such as ReflexAgent, Minimax, and Alpha-Beta are implemented to handle adversarial scenarios with ghosts.

## Uninformed Search Algorithms

### Depth-First Search (DFS)

DFS explores the deepest nodes in the search tree first. It uses a stack (LIFO) to manage states and explores the most recently generated node first. The algorithm is implemented in the `depthFirstSearch` function.

### Breadth-First Search (BFS)

BFS explores nodes level by level, starting from the root node. It uses a queue (FIFO) to manage states and guarantees the shortest path in terms of the number of steps. The algorithm is implemented in the `breadthFirstSearch` function.

### Uniform Cost Search (UCS)

UCS expands the node with the lowest path cost. It uses a priority queue to prioritize nodes based on their cumulative cost from the start state. The algorithm is implemented in the `uniformCostSearch` function.

## Informed Search Algorithms

### A* Search

A* search is an informed search algorithm that uses a heuristic to estimate the cost to reach the goal. It combines the cost to reach the current node and the estimated cost to reach the goal. The algorithm is implemented in the `aStarSearch` function.

### Corners Problem

The Corners Problem involves finding a path that visits all four corners of the maze. The `CornersProblem` class defines the state space and successor function for this problem. The `cornersHeuristic` function provides an admissible heuristic for this problem.

### Food Heuristic

The `foodHeuristic` function provides an admissible heuristic for the Food Search problem, estimating the distance to the nearest uneaten food dot.

### Suboptimal Search

The `findPathToClosestDot` function implements a suboptimal search strategy to find the nearest food dot using BFS.

## Adversarial Search

### Reflex Agent

The Reflex Agent chooses actions based on a simple evaluation function that considers food locations and ghost positions. The `evaluationFunction` method evaluates the desirability of a given game state and action.

### Minimax Algorithm

The Minimax algorithm is used to handle adversarial scenarios where Pac-Man and ghosts take turns. The `getAction` function in the `MinimaxAgent` class implements this algorithm, considering the depth and evaluation function.

### Alpha-Beta Pruning

Alpha-Beta Pruning is an optimization of the Minimax algorithm that reduces the number of nodes explored by pruning branches that cannot influence the final decision. The `getAction` function in the `AlphaBetaAgent` class implements this algorithm.

## Conclusion

This project demonstrates the application of various search algorithms to create an intelligent Pac-Man agent. The agent can navigate mazes, avoid ghosts, and collect food efficiently using both uninformed and informed search strategies. Adversarial search techniques like Minimax and Alpha-Beta Pruning further enhance the agent's ability to handle dynamic and competitive environments.

## How to Run the Project

1. Clone the repository.
2. Ensure you have Python installed.
3. Run the Pac-Man game with the desired agent by executing the appropriate Python script.
4. Observe the agent's behavior and performance in different scenarios.

## Dependencies

- Python 3.x
- Pygame (for visualization, if applicable)

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- The Pac-Man game framework provided by the University of California, Berkeley.
- The AI algorithms and concepts from the course "Artificial Intelligence" at the Faculty of Automation and Computer Science.

---

For any questions or further information, please contact the author: **Youssef Abanoub**.
