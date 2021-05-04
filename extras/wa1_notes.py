#!/usr/bin/env python3

from search import *
from random import shuffle
# file for Writing Assignment 1 - run in aima-py folder

# python3 -c "from wa1 import *; depth_first_tree_search(NQueensProblem(20)); print('SEARCH FINISHED'); sleep(10)"


# Eight-puzzle portion
puzzle = EightPuzzle((6, 2, 3, 1, 5, 4, 0, 7, 8))

# DLS is a tree implementation, so we will use tree for all
puzzle_dls50 = depth_limited_search(puzzle)
puzzle_bfs = breadth_first_tree_search(puzzle)

'''
len(puzzle_dls50.solution())  == 50   # moves from start node (== depth limit 50)
len(puzzle_dls50.path()) == 51		# all nodes in path including start node and goal


puzzle_dls50.solution() ==
['UP', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'UP', 'DOWN', 'DOWN', 'RIGHT', 'UP', 'RIGHT', 'UP', 'LEFT', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT']

puzzle_dls50.path() == 
[<Node (6, 2, 3, 1, 5, 4, 0, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (0, 2, 3, 6, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 0, 5, 4, 1, 7, 8)>, 
<Node (6, 2, 3, 1, 5, 4, 0, 7, 8)>, 
<Node (6, 2, 3, 1, 5, 4, 7, 0, 8)>, 
<Node (6, 2, 3, 1, 0, 4, 7, 5, 8)>, 
<Node (6, 2, 3, 1, 4, 0, 7, 5, 8)>, 
<Node (6, 2, 0, 1, 4, 3, 7, 5, 8)>, 
<Node (6, 0, 2, 1, 4, 3, 7, 5, 8)>, 
<Node (0, 6, 2, 1, 4, 3, 7, 5, 8)>, 
<Node (1, 6, 2, 0, 4, 3, 7, 5, 8)>, 
<Node (1, 6, 2, 4, 0, 3, 7, 5, 8)>, 
<Node (1, 0, 2, 4, 6, 3, 7, 5, 8)>, 
<Node (1, 2, 0, 4, 6, 3, 7, 5, 8)>, 
<Node (1, 2, 3, 4, 6, 0, 7, 5, 8)>, 
<Node (1, 2, 3, 4, 0, 6, 7, 5, 8)>, 
<Node (1, 2, 3, 4, 5, 6, 7, 0, 8)>, 
<Node (1, 2, 3, 4, 5, 6, 7, 8, 0)>]
'''


'''
len(puzzle_bfs.solution()) == 14  # moves from start node
len(puzzle_bfs.solution()) == 15  # all nodes in path including start node and goal

puzzle_bfs.solution() == ['RIGHT', 'UP', 'RIGHT', 'UP', 'LEFT', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT']


puzzle_bfs.path() ==
[<Node (6, 2, 3, 1, 5, 4, 0, 7, 8)>, <Node (6, 2, 3, 1, 5, 4, 7, 0, 8)>, <Node (6, 2, 3, 1, 0, 4, 7, 5, 8)>, <Node (6, 2, 3, 1, 4, 0, 7, 5, 8)>, <Node (6, 2, 0, 1, 4, 3, 7, 5, 8)>, <Node (6, 0, 2, 1, 4, 3, 7, 5, 8)>, <Node (0, 6, 2, 1, 4, 3, 7, 5, 8)>, <Node (1, 6, 2, 0, 4, 3, 7, 5, 8)>, <Node (1, 6, 2, 4, 0, 3, 7, 5, 8)>, <Node (1, 0, 2, 4, 6, 3, 7, 5, 8)>, <Node (1, 2, 0, 4, 6, 3, 7, 5, 8)>, <Node (1, 2, 3, 4, 6, 0, 7, 5, 8)>, <Node (1, 2, 3, 4, 0, 6, 7, 5, 8)>, <Node (1, 2, 3, 4, 5, 6, 7, 0, 8)>, <Node (1, 2, 3, 4, 5, 6, 7, 8, 0)>]

'''


# N-Queens portion
# BFS for boards sized 8 to 13
# breadth_first_tree_search(NQueensProblem(8))

# DFS for boards sized 8 to 20
# depth_first_tree_search(NQueensProblem(8))

def print_steps(node):
	initstate = node.path()[0]
	print(f"0. {initstate}")
	steps = list(zip(node.solution(), node.path()[1:]))
	stepno = 1
	for step in steps:
		print(f"{stepno}. {step}")
		stepno +=1
		
		
def rand8puzzle(goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
	solvable = False
	while not solvable:
		init_state = [*range(9)]
		random.shuffle(init_state)
		puzzle = EightPuzzle(tuple(init_state), goal)
		solvable = puzzle.check_solvability(init_state)
	return puzzle

""" In EightPuzzle class, default heuristic function used is 
	h(n) = number of misplaced tiles """
	
def makepuzzle(init, goal=(0,1,2,3,4,5,6,7,8)):
	puzzle = EightPuzzle(init, goal)
	if not puzzle.check_solvability(init): return None
	print('init state', init)
	print('h value', calculateManhattan(init))
	return puzzle


#  this doesn't work exactly as hoped but it's a tool of sorts...
def generatepuzzle(difficulty_lower_bound=0, difficulty_upper_bound=100):
	# 0-100%
	
	# This is based on Reinefeld paper, so only works with goal = (0,1,2,3,4,5,6,7,8)
	goal = (0,1,2,3,4,5,6,7,8)
	
	# calculate heuristic value for most difficult state
	hard_instance1 = (8,7,6,0,4,1,2,5,3)  # one of two with longest opt sol path = 31 (sol length = 30)
	hard_instance2 = (8,0,6,5,4,7,2,3,1)
	max_h = max(calculateManhattan(hard_instance1), calculateManhattan(hard_instance2)) + 1
	# max_h = 30  # tried this, it was bad
	h_lower_bound = max_h * difficulty_lower_bound / 100.0
	h_upper_bound = max_h * difficulty_upper_bound / 100.0
	
	puzzle = None
	init_state = [*range(9)]
	solvable = False
	h = -1
	
	while not solvable or not (h >= h_lower_bound and h<= h_upper_bound):
		random.shuffle(init_state)
		h = calculateManhattan(init_state)
		puzzle = EightPuzzle(tuple(init_state), goal)
		solvable = puzzle.check_solvability(init_state)
		
		
	print('init state:', tuple(init_state))
	print('h estimate:', h)
	return puzzle


''' MANHATTAN DISTANCE HEURISTIC: 

code given below:
'''
def calculateManhattan(initial_state):
	goal_state = (0,1,2,3,4,5,6,7,8)
	# https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
	# Manhattan Distance of a tile is the distance or the number of slides/tiles away it is from it’s goal state.Thus, for a certain state the Manhattan distance will be the sum of the Manhattan distances of all the tiles EXCEPT the blank tile.
	# tested and confirmed to work, with my modification to not count the blank square
	initial_config = initial_state
	manDist = 0
	for i,item in enumerate(initial_config):
		if item == 0:
			pass
		else:
			prev_row,prev_col = int(i/ 3) , i % 3
			goal_row,goal_col = int(item /3),item % 3
			manDist += abs(prev_row-goal_row) + abs(prev_col - goal_col)
	return manDist

goal_state = (0,1,2,3,4,5,6,7,8)
def h2(node):
	# for goal_state = (0,1,2,3,4,5,6,7,8)
	return calculateManhattan(node.state)


def generate_8puzzle_states(number):	# for goal_state = (0,1,2,3,4,5,6,7,8)
	
	def rand_solvable_state(goal=(0,1,2,3,4,5,6,7,8)):
		solvable = False
		while not solvable:
			init_state = [*range(9)]
			random.shuffle(init_state)
			puzzle = EightPuzzle(tuple(init_state), goal)
			solvable = puzzle.check_solvability(init_state)
		return tuple(init_state)
	
	states = []
	for i in range(0, number):
		isUnique = False
		while not isUnique:
			newstate = rand_solvable_state()
			if newstate not in states:
				isUnique = True
				states.append(newstate)
				
	states_with_hvalues = []
	for state in states:
		states_with_hvalues.append({'state': state, 'h2': calculateManhattan(state)})
		
	return states_with_hvalues

def do_astar_search_on_random_8puzzle_set(number, heuristic=h2, goal=(0,1,2,3,4,5,6,7,8)):
	states_with_hvalues = generate_8puzzle_states(number)
	results = []
	for each in states_with_hvalues:
		puzzle = EightPuzzle(each['state'], goal)
		searchresult = astar_search(puzzle, heuristic)
		info = {'init': each['state'], 'h2_manhattan':each['h2'], 'solution_length': len(searchresult.solution()), 'goal': goal, 'path': searchresult.path()}
		results.append(info)
	return results

		
	

'''
def helpmhtn(init):
...     for i, item in enumerate(init):
...             prev_row, prev_col = int(i/3), i%3
...             print('... i =', i, 'item =', item)
...             print('prev_row = int(i/3) =', prev_row, ', prev_col = i mod 3 =', prev_col)
...             goal_row, goal_col = int(item/3), item%3
...             print('goal_row = int(item/3) =', goal_row, ', goal_col = item mod 3 =', goal_col)
'''

''' ~ '''

# for goal= (0,1,2,3,4,5,6,7,8)
puz_easy = EightPuzzle((1,2,5,3,4,0,6,7,8), (0,1,2,3,4,5,6,7,8))  # opt solution length = 3
puz_med = EightPuzzle((1,4,2,6,5,8,7,3,0), (0,1,2,3,4,5,6,7,8))	  # opt solution length = 8 
puz_hard = EightPuzzle((1,0,2,7,5,4,8,6,3), (0,1,2,3,4,5,6,7,8))  # opt solution length = 23

# for timeit
def ucs_easy(): return uniform_cost_search(puz_easy)  #uses best_first_graph_search.. makes sense bc explored set..
def ucs_med(): return uniform_cost_search(puz_med)
def ucs_hard(): return uniform_cost_search(puz_hard)
	
def astar_easy(): return astar_search(puz_easy)
def astar_med(): return astar_search(puz_med)
def astar_hard(): return astar_search(puz_hard)
	
def iddfs_easy(): return iterative_deepening_search(puz_easy)
def iddfs_med(): return iterative_deepening_search(puz_med)
def iddfs_hard(): return iterative_deepening_search(puz_hard)
	
	
# examples for BUILT-IN! goal state: (123...)
'''
easy:
(1, 0, 3, 4, 2, 5, 7, 8, 6) # opt solution length = 3

(8, 4, 5, 0, 2, 7, 6, 3, 1) # opt solution length = 23 
(3, 2, 0, 8, 6, 1, 5, 4, 7) # opt solution length = 24
(8, 5, 0, 6, 2, 3, 4, 1, 7) # opt solution length = 26

'''
	
	
	
'''
# REINEFELD (from Reinfeld 8 Puzzle solutions) 
goal= (0,1,2,3,4,5,6,7,8)


The two cases with the shortest (non-trivial) solution path f* = 1 have either of tile 1 or 3 in the
upper left corner:
102345678
312045678

The two configurations with the most (64) solutions are:
856723410
EightPuzzle((8,5,6,7,2,3,4,1,0), (0,1,2,3,4,5,6,7,8))
854763210
EightPuzzle((8,5,4,7,6,3,2,1,0), (0,1,2,3,4,5,6,7,8))


EXTREMELY HARD:
The two configurations with the longest optimal solution path f* = 31 are:
# (8,7,6,0,4,1,2,5,3)
EightPuzzle((8,7,6,0,4,1,2,5,3), (0,1,2,3,4,5,6,7,8))
(8,0,6,5,4,7,2,3,1)
EightPuzzle((8,0,6,5,4,7,2,3,1), (0,1,2,3,4,5,6,7,8))

'''
	
''''
MORE INSTANCES FOR REINEFELD GOAL = 012...


420
175
368


# these hvalues are wrong and count the blank square's manhattan distance when they shouldn't... just fyi 
(1,4,2,3,7,5,6,0,8)           # h2 = 6, .path() = 4
(4,2,0,1,7,5,3,6,8)			  # h2 = 10, path = 9    # UCS solves quickly
(0, 1, 2, 3, 7, 5, 6, 8, 4)   # h2 = 4, path = 11
(0, 1, 2, 4, 5, 3, 6, 7, 8)   # h2 = 4, path = 15
(1, 2, 0, 8, 7, 5, 3, 6, 4)   # h2 = 12 path = 15
(0, 1, 2, 3, 5, 7, 6, 4, 8)   # h2 = 4, path = 17
(4, 2, 0, 8, 3, 1, 6, 7, 5)   # h2 = 12, path = 17
(7, 0, 1, 3, 2, 5, 6, 8, 4)   # h2 = 10, path = 18  # (fast)
(6, 4, 0, 3, 1, 2, 5, 7, 8)   # h2 = 10, path = 19
(0, 1, 5, 3, 4, 2, 7, 6, 8)   # h2 = 4, path = 21  # median / mean?
(0, 2, 4, 7, 1, 3, 8, 6, 5)	  # h2 = 12, path = 21
(4, 1, 8, 0, 3, 5, 6, 7, 2)   # h2 = 8, path = 22  # p quick
# 20-something path lengths seems to start to take time... remember each one is a depth level
(5, 0, 8, 6, 2, 3, 1, 4, 7)   # h2 = 16, path = 22
(0, 2, 1, 8, 3, 4, 6, 7, 5)   # h2 = 8, path = 23 
(1, 2, 3, 4, 5, 6, 7, 8, 0)   # h2 = 16, path = 23
(6, 3, 8, 7, 1, 2, 4, 0, 5)   # h2= 16, path = 24

init state (8, 0, 6, 2, 7, 4, 1, 5, 3)
h value 22
len(solution): 27

'''
	
'''
Want to generate every possible 8-puzzle?
Heap's algorithm:
https://stackoverflow.com/questions/59128777/how-to-find-all-possible-states-of-8-puzzle
'''