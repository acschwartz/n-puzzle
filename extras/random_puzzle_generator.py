#!/usr/bin/env python3

import json
from pandas.io.json import json_normalize
import random
from search import *

GOAL_STATE = (0,1,2,3,4,5,6,7,8)



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


def h2(node):		# to be used by astar_search from search.py
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
		info = {'init': each['state'], 'goal': goal, 'h2_manhattan':each['h2'], 'solution_length': len(searchresult.solution())}
		results.append(info)
	return json.dumps(results)

#########################################################################################

