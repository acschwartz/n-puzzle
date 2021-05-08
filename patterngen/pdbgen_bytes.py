#!/usr/bin/env python3
from argparse import ArgumentParser
from sys import platform

'''

TODO: HUGE !!!!!!! H U G E discovery...
deepcopy is slow asf, compared to converting between lists and tuples

pz = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
>>> timeit(lambda:list(tuple(pz)))
0.31665251099911984
>>> timeit(lambda:deepcopy(pz))
11.42695140199794

YIKES.
That's probably why this ran so incredibly slowly.

P.S. bytearrays take up much less room and can be copied much quicker:
>>> ba = bytearray(pz)
>>> ba
bytearray(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f')
>>> timeit(lambda:bytearray(ba))
0.2905499839980621

Comparing two bytearrays is also faster than comparing two arrays.

ba2 = bytearray(ba) creates a new bytearray in ba2 that is distinct from and not a ref to ba

'''
##==============================================================================================##
'''
ANOTHER NOTE:

A dict with ints for keys and a dict with bytes for keys are apparently the same size.
So that is not a legitimate way to save space.. oddly.

for i in range(10000):
	d_ints[i] = randint(0,255)
	d_bytes[i] = bytes([int(randint(0,255)])

>>> sizeof(d_ints)
295000
>>> sizeof(d_bytes)
295000

'''
'''
ANOTHER NOTE:

Math on ints is much faster than math on bytes

>>> a = bytes([3])
>>> b= bytes([15])
>>> from timeit import timeit
>>> timeit(lambda:a+b)
0.17650921399996378
>>> timeit(lambda:3+15)
0.0963714110000069

'''

##==============================================================================================##

##==============================================================================================##
PATTERNS = {
	'15fringe': {
				'dim': 4,	# 15-puzzle is 4x4
				'pattern tiles': (0, 3, 7, 11, 12, 13, 14, 15),
				},
}
##==============================================================================================##
def move_index_left(i, dim):
	if i % dim > 0:
		return i-1
	else:
		return None

def move_index_right(i, dim):
	if i % dim + 1 < dim:
		return i+1
	else:
		return None

def move_index_up(i, dim):
	if i-dim >= 0:
		return i-dim
	else:
		return None

def move_index_down(i, dim):
	if i+dim < dim**2:	# assumes square puzzle
		return i+dim
	else:
		return None

MOVE_INDEX = {
	'left': {
		'func': move_index_left,
		'opp': 'right'
	},
	'right': {
		'func': move_index_right,
		'opp': 'left'
	},
	'up': {
		'func': move_index_up,
		'opp': 'down'
	},
	'down': {
		'func': move_index_down,
		'opp': 'up'
	}
}

# having the functions in a list saves dictionary lookups in MOVE_INDEX
DIRECTIONS = ('left', 'right', 'up', 'down')
MOVES = tuple(map(lambda d: MOVE_INDEX[DIRECTIONS[d]]['func'], range(len(DIRECTIONS))))
OPP_MOVES = tuple(map(lambda d: DIRECTIONS.index(MOVE_INDEX[DIRECTIONS[d]]['opp']), range(len(DIRECTIONS))))
##==============================================================================================##

OUTPUTFILE_IDENTIFIER = ""
OUTPUT_DIRECTORY = 'output/'
MAXRSS_UNIT_COEFFICIENT = 1024 if platform != 'darwin' else 1

##==============================================================================================##
def parseArgs():
	parser = ArgumentParser(description='n-puzzle pattern database generator')
	parser.add_argument('pattern_name', help='choose a pattern', choices=list(PATTERNS.keys()))
	args = parser.parse_args()
	return args.pattern_name

def init(patternName='15fringe'):
	global OUTPUTFILE_IDENTIFIER
	OUTPUTFILE_IDENTIFIER = "".join([str(math.floor(time.time()*1000)-(1619863801*1000)-372000000), '__', pname, '_'])
	print(OUTPUTFILE_IDENTIFIER)
	
	# global vars copied to local for speed
	dirs = DIRECTIONS
	moves = MOVES
	undo_moves = OPP_MOVES
	dim = PATTERNS[patternName]['dim']
	ptiles = PATTERNS[patternName]['pattern tiles']
	initialPatternTileLocations = generateTargetPattern(ptiles, dim)

def generateTargetPatternAsBytes(ptiles):
	# generate pattern representation of puzzle goal state = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	# which will be the initial state for the backwards BFS used to generate the PDB
	
	# returns: pattern as bytestring where pattern[i] is the index of pattern tile i within the puzzle state
	# e.g. if ptiles = (0,3,7,11,12,13,14,15)
	# pattern = b'\x00\x03\x07\x0b\x0c\r\x0e\x0f'
	# so pattern[i] will change when square i moves on the board.
	# "empty" squares which are not part of the pattern are omitted to save space
	# (although this only saves ~8 bytes per state, this is amortized over the millions of states we must store).
	# notes: bytestrings are like a 'tuple' compared to a bytearray - immutable but elements can be accessed by index
	
	pattern = []
	for tile in ptiles:
		pattern.append(tile)
	return bytes(pattern)


def repr(pattern):
	# get representation of each pattern - used as keys for storage, etc.
	return bytes(pattern)


def getActions(state, stateInfo, dim, moveSetAsTuple):
# Returns list of possible actions in the form action=(tileindex, direction)
	allowedActions = []
	undoAction = (int(stateInfo[1]), int(stateInfo[2]))
	# disallowed bc it would just take you back to the state's parent from which it was generated
	# and it's a waste of time to generate that parent state again
	
	for ptileID, tileLocationInPuzzle in enumerate(state):
		for moveID, moveFunction in enumerate(moveSetAsTuple):
			action = (ptileID, moveID)
			if action == undoAction:
				continue
			tileLocationAfterMove = moveFunction(tileLocationInPuzzle, dim)
			if tileLocationAfterMove and tileLocationAfterMove not in state:
				allowedActions.append(action)
	return allowedActions


def doAction(startState, dim, action, startStateDepth, moveSetAsTuple, undoMoves=OPP_MOVES):
	i, dir = action
	newState = list(startState)
	newState[i] = moveSetAsTuple[dir](startState[i], dim)
	info = [startStateDepth+1, i, undoMoves[dir]]
	return repr(newState), bytes(info)


# combines getActions and doAction
# getAction and doAction still useful for unit testing!
def generateChildren(state, state_info, dim, moveSetAsTuple, undoMoves=OPP_MOVES):
	state_depth = state_info[0]
	children_depth = state_depth + 1
	action_generate_parent = (int(state_info[1]), int(state_info[2]))
	# the above action would generate the parent from which this state originated
	
	children = []
	for ptileID, tileLocationInPuzzle in enumerate(state):
		for moveID, moveFunction in enumerate(moveSetAsTuple):
			action = (ptileID, moveID)
			if action == action_generate_parent:
				continue
			new_tile_location = moveFunction(tileLocationInPuzzle, dim)
			if new_tile_location and new_tile_location not in state:
			# checks that new location is in bounds, and that the new square is not occupied by another pattern tile
				child = list(state)
				child[ptileID] = new_tile_location
				childInfo = [children_depth, ptileID, undoMoves[moveID]]
				children.append((repr(child), bytes(childInfo)))
	return children
	

##==============================================================================================##

# NOTES: 
'''
>>> sizeof((1,2))
56
>>> sizeof(Coords(1,2))
48

class Coords:
	__slots__: ['x', 'y']
	def __init__(self, x, y):
		self.x = x
		self.y = y
'''
'''
As far s PDB lookups go...
>>> timeit(lambda:bytes(bytearray([1,2,3,4,7,8,9])))
0.6865901119999762
>>> timeit(lambda:tuple([1,2,3,4,7,8,9]))
0.23621258300045156
>>> timeit(lambda:bytes([1,2,3,4,7,8,9]))
0.4075702660011302

Recall dictionary keys have to be IMMUTABLE TYPE - so lists, bytearrays not allowed
tuples, bytes, allowed

......
Regarding representations of states:

>>> pat_list = [0, 255, 255, 4, 255, 255, 255, 13, 255, 255, 255, 14, 2, 10, 3, 6]
>>> timeit(lambda:str(tuple(pat_list)))
2.4628033119988686
>>> timeit(lambda:str(bytes(pat_list))b')
0.7033650670000497
timeit(lambda:bytes(pat_list))
0.4218067380006687
>>> timeit(lambda:list(pat_list_as_bytes))
0.39167072900090716

Comparing values stored as bytes vs as ints
>>> timeit(lambda: b'\x01' == b'\x02')
0.11794590199860977
>>> timeit(lambda: 1 == 2)
0.11735898000006273
>>> timeit(lambda: 13  == b'\x02')
0.12782957599847578
>>> timeit(lambda: 15 == b'\x0f')
0.12981452200256172
>>> timeit(lambda: 15 == 15)
0.11791720199835254

retrieving a val from bytestring or list
>>> timeit(lambda: pat_list[3])
0.12938051099990844
>>> timeit(lambda: pat_list_as_bytes[3])
0.13401093900029082
>>> timeit(lambda: pat_list[15])
0.1675721989995509
>>> timeit(lambda: pat_list_as_bytes[15])
0.1338116719998652


>>> timeit(lambda: pat_list_as_bytes[15]+1)
0.15390037799988932
>>> pat_list_as_bytes[15]+1
7
>>> pat_list[15]+1
7
>>> timeit(lambda: pat_list[15]+1)
0.14973862400074722
'''