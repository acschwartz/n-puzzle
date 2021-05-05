#!/usr/bin/env python3
import sys
import json
import resource
from time import perf_counter
from collections import deque
from aima.search import Problem
from aima.search import Node


BLANK_TILE = 0  #None

'''
Potential state representations:
(0, 3, 0, 0, 15, 0, 0, 7, 12, 11, 0, 0, 0, 13, 14, 0)
state[1] = 3
state.index(3) = 1

(None, None, None, (x,y), None, None, None, (x,y), None, None, None, (x,y), (x,y), (x,y), (x,y), (x,y))
state[3] = (x,y) coordinates of tile 3
state.index(2,1) = see if any pattern tile occupies that coordinate

{3: (x,y), 7: (x,y), ...}
downside: can't search for coordinates


'''


class FifteenPuzzlePattern(Problem):
	def __init__(self, pattern_tiles, blank_tile=BLANK_TILE):
		self.pattern_tiles = pattern_tiles
		self.blank_tile = blank_tile
		self.grid_dim = 4
		self.possible_moves = ('left', 'right', 'up', 'down')
		self.move_xy = {
			'left': lambda x,y: (x, y-1),
			'right': lambda x,y: (x, y+1),
			'up': lambda x,y: (x-1, y),
			'down': lambda x,y: (x+1, y),
		}
		
		target_pattern = list(range(16))
		for tile in range(len(target_pattern)):
			if target_pattern[tile] not in pattern_tiles:
				target_pattern[tile] = blank_tile
		super().__init__(tuple(target_pattern))
	
	def actions(self, state):
		def isInBounds():
			for c in new_coords:
				if c < 0 or c >= self.grid_dim:
					return False
			return True
		
		# schema: action = (3, 'up')
		actions = []
		dim = self.grid_dim
		index_pattern_tiles = self.get_pattern_tile_indices(state)
		occupied = set()
		for tile in index_pattern_tiles:
			i = index_pattern_tiles[tile]
			occupied.add(self.index_1d_to_xy(i))
			
		for tile in self.pattern_tiles:
			i = index_pattern_tiles[tile]
			x, y = self.index_1d_to_xy(i)
			for direction in self.possible_moves:
				new_coords = self.move_xy[direction](x,y)
				if isInBounds() and new_coords not in occupied:
					actions.append((tile, direction))
		return actions
	
	
	def result(self, state, action):
		""" Given state and action, return a new state that is the result of the action.
		Action is assumed to be a valid action in the state """
		
		# assuming state takes form: (0, 3, 11, 7, 0, 0, 0, 15, 0, 0, 0, 0, 12, 13, 14, 0)
		# action schema: (ptile, move) i.e. (3, 'left')
		patterntile, direction = action
		i = state.index(patterntile)
		x, y = self.index_1d_to_xy(i)
		
		new_state = list(state)
		new_coords = self.move_xy[direction](x,y)
		new_index = self.index_xy_to_1d(new_coords)
		new_state[i] = BLANK_TILE
		new_state[new_index] = patterntile
		return tuple(new_state)
		

		
	def goal_test(self, state):
		return False
	
	def get_pattern_tile_indices(self, state):
		# assuming state takes form: (0, 0, 0, 3, 0, 0, 0, 7, 0, 0, 0, 11, 12, 13, 14, 15)
		pt_indices = dict()
		for tile in self.pattern_tiles:
			pt_indices[tile] = state.index(tile)
		return pt_indices  # schema: {3: 3, 7: 7, ...} 

	def index_1d_to_xy(self, i):
		dim = self.grid_dim
		x = i // dim
		y = i % dim
		return (x,y)
	
	def index_xy_to_1d(self, x, y):
		dim = self.grid_dim
		i = x*dim + y
		return i
	
	def index_xy_to_1d(self, coords):
		x, y = coords
		dim = self.grid_dim
		i = x*dim + y
		return i
	
	def clone_and_swap(state,y0,y1):
		clone = list(state)
		tmp = clone[y0]
		clone[y0] = clone[y1]
		clone[y1] = tmp
		return tuple(clone)


class FringePattern(FifteenPuzzlePattern):
	def __init__(self):
		pattern_tiles = (3, 7, 11, 12, 13, 14, 15)
		super().__init__(pattern_tiles)


# modified a bit
def breadth_first_graph_search(problem):
	node = Node(problem.initial)
	frontier = deque([node])
	explored = dict()
	while frontier:
		node = frontier.popleft()
		explored[node.state] = node.depth
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				if problem.goal_test(child.state):
					return child
				frontier.append(child)
	return explored

def generateFringePDB():
	with open("database.json", "w") as f:
		explored = breadth_first_graph_search(FringePattern())
		json.dump(explored, f)
	return len(explored)


def print_modulo_table(boardsize=4):
	n = boardsize
	for i in range(n*n):
		print('i:', i)
		print(i, '%', n, '=', i % n)
		print(i, '//', n, '=', i // n)
		print()

def bytes_to_human_readable_string(size,precision=2):
# SOURCE: https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python/14822210
# http://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/
	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024 and suffixIndex < 4:
		suffixIndex += 1 #increment the index of the suffix
		size = size/1024.0 #apply the division
	return "%.*f%s"%(precision,size,suffixes[suffixIndex])

maxrss_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
t_start = perf_counter()
len_explored = generateFringePDB()
t_delta = perf_counter() - t_start
maxrss_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
MAXRSS_UNIT_COEFFICIENT = 1024 if sys.platform != 'darwin' else 1
maxrss_delta = maxrss_after - maxrss_before
maxrss_delta_human = bytes_to_human_readable_string(maxrss_delta * MAXRSS_UNIT_COEFFICIENT, 2)

print('nodes explored:', len_explored)
print('time (seconds): %.4f' % (t_delta))
print('delta maxrss:', maxrss_delta)
print('delta maxrss (with units):', maxrss_delta_human)





#def index_1d_to_xy(i, dim=4):
#	x = i // dim
#	y = i % dim
#	return (x,y)
#
#def index_xy_to_1d(x, y, dim=4):
#	i = x*dim + y
#	return i
	
'''
class Problem:
	"""The abstract class for a formal problem. You should subclass
	this and implement the methods actions and result, and possibly
	__init__, goal_test, and path_cost. Then you will create instances
	of your subclass and solve them with the various search functions."""

	def __init__(self, initial, goal=None):
		"""The constructor specifies the initial state, and possibly a goal
		state, if there is a unique goal. Your subclass's constructor can add
		other arguments."""
		self.initial = initial
		self.goal = goal

	def actions(self, state):
		"""Return the actions that can be executed in the given
		state. The result would typically be a list, but if there are
		many actions, consider yielding them one at a time in an
		iterator, rather than building them all at once."""
		raise NotImplementedError

	def result(self, state, action):
		"""Return the state that results from executing the given
		action in the given state. The action must be one of
		self.actions(state)."""
		raise NotImplementedError

	def goal_test(self, state):
		"""Return True if the state is a goal. The default method compares the
		state to self.goal or checks for state in self.goal if it is a
		list, as specified in the constructor. Override this method if
		checking against a single self.goal is not enough."""
		if isinstance(self.goal, list):
			return is_in(state, self.goal)
		else:
			return state == self.goal

	def path_cost(self, c, state1, action, state2):
		"""Return the cost of a solution path that arrives at state2 from
		state1 via action, assuming cost c to get up to state1. If the problem
		is such that the path doesn't matter, this function will only look at
		state2. If the path does matter, it will consider c and maybe state1
		and action. The default method costs 1 for every step in the path."""
		return c + 1

	def value(self, state):
		"""For optimization problems, each state has a value. Hill Climbing
		and related algorithms try to maximize this value."""
		raise NotImplementedError


class EightPuzzle(Problem):
	""" The problem of sliding tiles numbered from 1 to 8 on a 3x3 board, where one of the
	squares is a blank. A state is represented as a tuple of length 9, where  element at
	index i represents the tile number  at index i (0 if it's an empty square) """

	def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
		""" Define goal state and initialize a problem """
		super().__init__(initial, goal)

	def find_blank_square(self, state):
		"""Return the index of the blank square in a given state"""

		return state.index(0)

	def actions(self, state):
		""" Return the actions that can be executed in the given state.
		The result would be a list, since there are only four possible actions
		in any given state of the environment """

		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)

		if index_blank_square % 3 == 0:
			possible_actions.remove('LEFT')
		if index_blank_square < 3:
			possible_actions.remove('UP')
		if index_blank_square % 3 == 2:
			possible_actions.remove('RIGHT')
		if index_blank_square > 5:
			possible_actions.remove('DOWN')

		return possible_actions

	def result(self, state, action):
		""" Given state and action, return a new state that is the result of the action.
		Action is assumed to be a valid action in the state """

		# blank is the index of the blank square
		blank = self.find_blank_square(state)
		new_state = list(state)

		delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
		neighbor = blank + delta[action]
		new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

		return tuple(new_state)

	def goal_test(self, state):
		""" Given a state, return True if state is a goal state or False, otherwise """

		return state == self.goal

	def check_solvability(self, state):
		""" Checks if the given state is solvable """

		inversion = 0
		for i in range(len(state)):
			for j in range(i + 1, len(state)):
				if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
					inversion += 1

		return inversion % 2 == 0

	def h(self, node):
		""" Return the heuristic value for a given state. Default heuristic function used is 
		h(n) = number of misplaced tiles """

		return sum(s != g for (s, g) in zip(node.state, self.goal))


'''