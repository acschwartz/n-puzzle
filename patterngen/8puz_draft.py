#!/usr/bin/env python3

import json
import math
from collections import deque
from copy import deepcopy
from timeit import default_timer

 Goal state of the puzzle



EMPTY_TILE = 0



# Calculates the possible moves of the blank tile.
def get_moves(puzzle):
	pos = puzzle.index(0)
	
	if pos == 0:
		possible_moves = [1, 3]
	elif pos == 1:
		possible_moves = [1, 3, -1]
	elif pos == 2:
		possible_moves = [3, -1]
	elif pos == 3:
		possible_moves = [-3, 1, 3]
	elif pos == 4:
		possible_moves = [-3, 1, 3, -1]
	elif pos == 5:
		possible_moves = [-3, 3, -1]
	elif pos == 6:
		possible_moves = [-3, 1]
	elif pos == 7:
		possible_moves = [-3, 1, -1]
	else:
		possible_moves = [-3, -1]
		
	return possible_moves


# Moves the blank tile in the puzzle.
def move(puzzle, direction):
	# Creates a copy of the new_puzzle to change it.
	new_puzzle = deepcopy(puzzle)
	pos = puzzle.index(0)
	# Position blank tile will move to.
	new_pos = pos + direction
	# Swap tiles.
	new_puzzle[pos], new_puzzle[new_pos] = new_puzzle[new_pos], new_puzzle[pos]
	
	return new_puzzle

def flattenToString(lst):
#	return "".join(str(i) for i in lst)
	return str(tuple(lst))


# Creates the database.
def create_database():
	# Initializes a timer, starting state, queue and visited set.
	begin = default_timer()
	start = goal
	queue = deque([[start, 0]])
	entries = dict()
	visited = set()
	
	print("Generating database...")
	print("Collecting entries...")
	# BFS taking into account a state and the cost (number of moves) to reach it from the starting state.
	while queue:
		state_cost = queue.popleft()
		state = state_cost[0]
		cost = state_cost[1]
		
		for m in get_moves(state):
			next_state = move(state, m)
			
			# Increases cost if blank tile swapped with number tile.
			pos = state.index(0)
			if next_state[pos] > 0:
				next_state_cost = [next_state, cost+1]
			else:
				next_state_cost = [next_state, cost]
				
			if not flattenToString(next_state) in visited:
				queue.append(next_state_cost)
			
			state_as_string = flattenToString(state)
			entries[state_as_string] = cost
			visited.add(state_as_string)
			
		# Print a progress for every x entries in visited.
		if len(entries) % 10000 == 0:
			print("Entries collected: " + str(len(entries)))
			
		# Exit loop when all permutations for the puzzle have been found.
		if len(entries) >= 181440:
			break
		
	print("Writing entries to database...")
	# Writes entries to the text file, sorted by cost in ascending order .
	with open("database.json", "w") as f:
		json.dump(entries, f)
			
	end = default_timer()
	minutes = math.floor((end-begin)/60)
	seconds = math.floor((end-begin) % 60)
	return "Generated database in " + str(minutes) + " minute(s) and " + str(seconds) + " second(s)."


print(create_database())