#!/usr/bin/env python3
from argparse import ArgumentParser
from sys import platform
from math import floor
from collections import deque
import time
import resource
import pickle

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

def bytes_to_human_readable_string(size,precision=2):
# SOURCE: https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python/14822210
# http://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/
	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024 and suffixIndex < 4:
		suffixIndex += 1 #increment the index of the suffix
		size = size/1024.0 #apply the division
	return "%.*f%s"%(precision,size,suffixes[suffixIndex])

##==============================================================================================##

def parseArgs():
	parser = ArgumentParser(description='n-puzzle pattern database generator')
	parser.add_argument('pattern_name', help='choose a pattern', choices=list(PATTERNS.keys()))
	args = parser.parse_args()
	return args.pattern_name

def initOutputFileID(pname):
	global OUTPUTFILE_IDENTIFIER
	OUTPUTFILE_IDENTIFIER = "".join([str(floor(time.time()*1000)-(1619863801*1000)-372000000), '__', pname, '_'])
	print(OUTPUTFILE_IDENTIFIER)
	return OUTPUTFILE_IDENTIFIER

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

def generateInitialSearchNode(ptiles):
#	return (generateTargetPatternAsBytes(ptiles), bytes([0, 255, 255]))
	return generateTargetPatternAsBytes(ptiles)+bytes([0,255,255])


def generateChildren(state, state_info, dim, moveSetAsTuple, undoMoves):
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
				children.append((bytes(child), bytes(childInfo)))
	return children


def generatePDB(initNode, dim, num_ptiles, moveSet, oppMoves):
	queue = deque([initNode])
	frontier = set()
	frontier.add(initNode[:num_ptiles])
	visited = dict()
	visitedCount = 0
	
	while queue:
		node = queue.popleft()
		state_repr = node[:num_ptiles]
		state_info = node[num_ptiles:]
		
		for child_state, child_info in generateChildren(state_repr, state_info, dim, moveSet, oppMoves):
			if (child_state not in visited) and (child_state not in frontier):
				queue.append(child_state+child_info)
				frontier.add(child_state)
				
		visited[state_repr] = bytes([state_info[0]])
		visitedCount += 1
		frontier.remove(state_repr)
		
		if visitedCount == 10**6:
			print(visited)
			break
		
		if visitedCount % 10000 == 0:
			print("Entries collected:", visitedCount)
			
		if not frontier:
			break
	
	print("Writing entries to database...")
	filename = "".join([OUTPUTFILE_IDENTIFIER, "database.pickle"])
	with open("".join([OUTPUT_DIRECTORY, filename]), "wb") as f:
		pickle.dump(visited, f)
		
	return filename, visitedCount
		
##==============================================================================================##
##==============================================================================================##
		
if __name__ == '__main__':
	patternName = parseArgs()
	initOutputFileID(patternName)
	ptiles = PATTERNS[patternName]['pattern tiles']
	
	stats = dict()
	
	stats['time (seconds)'] = time.perf_counter()
	stats['memory'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

	#GENERATE DATABASE
	stats['_PDB file'], stats['db entries (nodes explored)'] = generatePDB(generateInitialSearchNode(ptiles), PATTERNS[patternName]['dim'], len(ptiles), MOVES, OPP_MOVES)
	
	
	stats['time (seconds)'] = float("{:.2f}".format( time.perf_counter() - stats['time (seconds)']))
	stats['memory'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - stats['memory']
	stats['time (mins)'] = float("{:.2f}".format(stats['time (seconds)'] /60))
	stats['memory (w/ units)'] = bytes_to_human_readable_string(stats['memory'] * MAXRSS_UNIT_COEFFICIENT, 2)
	
	file = "".join([OUTPUTFILE_IDENTIFIER, "stats.txt"])
	with open(OUTPUT_DIRECTORY+file, "w") as f:
		# create list of strings
		stringz = [ f'{key} : {stats[key]}' for key in stats ]
		stringz.sort()
		# write string one by one adding newline
		[f.write(f'{st}\n') for st in stringz ]
		
	stats['_stats file:'] = OUTPUT_DIRECTORY+file
	print(stats)

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