#!/usr/bin/env python3
from argparse import ArgumentParser
from math import floor
from collections import deque
import sys
import time
import resource
import pickle
import traceback
import logging
import pprint

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
	x = i-dim
	if x >= 0:
		return x
	else:
		return None

def move_index_down(i, dim):
	x = i+dim
	if x < dim*dim:	# assumes square puzzle
		return x
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

MAXRSS_UNIT_COEFFICIENT = 1024 if sys.platform.startswith('darwin') else 1
SECTION_SEPARATOR = '=========================================================================='
RUN_ID = time.strftime(f'%y%m%d-%H%M%S')
OUTPUT_DIRECTORY = 'output/'

def getBaseOutputfileName(pname):
	OUTPUT_FILENAME_PREFIX = "".join([pname, '_'])
	OUTPUT_FILENAME_SUFFIX = "".join(['_', RUN_ID])
	base_output_filename = "".join([OUTPUT_FILENAME_PREFIX, 'pdb', OUTPUT_FILENAME_SUFFIX])
	return base_output_filename

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
	action_generate_parent = (state_info[1], state_info[2])
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


def generateChildrenOptimized(state, state_info, dim, moveSetAsTuple, undoMoves):
# Apparently this is a legitimate optimization...
#>>> def stepThruEnum():
#...     for I, val in enumerate(p_bytes):
#...             print(i, val)
#timeit(stepThruEnum) = 33.80008150300273
#
#>>> def stepThruwithi():
#...     i = 0
#...     for tile in p_bytes:
#...             print(i, tile)
#...             i += 1
#timeit(stepThruwithi) = 31.335610534995794

	state_depth = state_info[0]
	children_depth = state_depth + 1
	action_generate_parent = (state_info[1], state_info[2])
	# the above action would generate the parent from which this state originated
	
	children = []
	ptileID = 0
	for tileLocationInPuzzle in state:
		moveID = 0
		for moveFunction in moveSetAsTuple:
			action = (ptileID, moveID)
			if action == action_generate_parent:
				moveID += 1
				continue
			new_tile_location = moveFunction(tileLocationInPuzzle, dim)
			if new_tile_location and new_tile_location not in state:
			# checks that new location is in bounds, and that the new square is not occupied by another pattern tile
				child = list(state)
				child[ptileID] = new_tile_location
				childInfo = [children_depth, ptileID, undoMoves[moveID]]
				children.append((bytes(child), bytes(childInfo)))
			moveID += 1
		ptileID += 1
	return children

##==============================================================================================##
def handle_exception(exc_type, exc_value, exc_traceback):
# Source: https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
	if issubclass(exc_type, KeyboardInterrupt):
		sys.__excepthook__(exc_type, exc_value, exc_traceback)
		return
	
	logger.critical("\nUncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
	logger.info('\n')
	
sys.excepthook = handle_exception

##==============================================================================================##
#	 G E N E R A T E   P A T T E R N   D A T A B A S E
##==============================================================================================##

def generatePDB(initNode, dim, num_ptiles, moveSet, oppMoves, BASE_OUTPUT_FILENAME, logger):
	queue = deque([initNode])
	frontier = set()
	frontier.add(initNode[:num_ptiles])
	visited = dict()
	visitedCount = 0
	
	while queue:
		#DEBUG
#		break
		
		node = queue.popleft()
		state_repr = node[:num_ptiles]
		state_info = node[num_ptiles:]
		
		for child_state, child_info in generateChildrenOptimized(state_repr, state_info, dim, moveSet, oppMoves):
			if (child_state not in visited) and (child_state not in frontier):
				queue.append(child_state+child_info)
				frontier.add(child_state)
				
		visited[state_repr] = bytes([state_info[0]])
		visitedCount += 1
		frontier.remove(state_repr)
		
#		DEBUG
		if visitedCount == 10000:
			logger.debug(visited)
			break
		
		if visitedCount % 10000 == 0:
			print("Entries collected:", visitedCount)
			
		if not frontier:
			break
	
	# WRITE TO DATABASE FILE
	outfile = OUTPUT_DIRECTORY+BASE_OUTPUT_FILENAME
	tryAgain = 'y'
	while tryAgain == 'y':
		try:
			actionMessage = "".join(["\nWriting entries to database file:", outfile, "....."])
			f = open(outfile, "wb")
			logger.info(actionMessage)
#			raise OSError
			pickle.dump(visited, f, pickle.HIGHEST_PROTOCOL)
			logger.info('Done!')
			f.close()
			tryAgain = False
		except OSError as err:
			f.close()
			logger.exception(err)
			tryAgain = input('\nPress y to retry ')
			if tryAgain == 'y':
				logger.info('\nUser directive: retry')
			
	return visitedCount

##==============================================================================================##
#		M	A 	I	N
##==============================================================================================##
if __name__ == '__main__':
	pname = parseArgs()
	ptiles = PATTERNS[pname]['pattern tiles']
	dim = PATTERNS[pname]['dim']
	BASE_OUTPUT_FILENAME = getBaseOutputfileName(pname)
	logfile = "".join([OUTPUT_DIRECTORY, BASE_OUTPUT_FILENAME, '.log'])
	
	# create logger
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)  	# CAN SET TO INFO / DEBUG
	
	# create handlers for logigng to both file and stdout
	stdout_handler = logging.StreamHandler(stream=sys.stdout)
	logger.addHandler(stdout_handler)
	output_file_handler = logging.FileHandler(logfile)
	output_file_handler.setLevel(logging.INFO)	# don't ever want debug stuff in the logfile
	logger.addHandler(output_file_handler)
	
	logger.info(SECTION_SEPARATOR)
	logger.info('Run ID: '+str(RUN_ID))
	logger.info('DB name: '+BASE_OUTPUT_FILENAME)
	logger.info('Pattern type: '+str(pname))
	logger.info("".join([SECTION_SEPARATOR, '\n']))

	stats = dict()
	t_start = time.perf_counter()
	maxrss_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

	#GENERATE DATABASE
	len_db = generatePDB(generateInitialSearchNode(ptiles), dim, len(ptiles), MOVES, OPP_MOVES, BASE_OUTPUT_FILENAME, logger)
	
	stats['entries collected'] = len_db
	stats['platform'] = sys.platform
	stats['time (s)'] = float("{:.2f}".format( time.perf_counter() - t_start))
	stats['memory (raw)'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - maxrss_start
	stats['time (min)'] = float("{:.2f}".format(stats['time (s)'] /60))
	stats['memory (units)'] = bytes_to_human_readable_string(stats['memory (raw)'] * MAXRSS_UNIT_COEFFICIENT, 2)
	
	stats_as_strings = sorted([ f'{key} : {stats[key]}' for key in stats ])
	logger.info("".join(['\n', SECTION_SEPARATOR]))
	
	for stat in stats_as_strings:
		logger.info(stat) 
	logger.info(SECTION_SEPARATOR)

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