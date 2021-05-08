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

SECTION_SEPARATOR = '=========================================================================='
RUN_ID = time.strftime(f'%y%m%d-%H%M%S')
OUTPUT_DIRECTORY = 'output/'

def getBaseOutputfileName(pname):
	OUTPUT_FILENAME_PREFIX = "".join([pname, '_'])
	OUTPUT_FILENAME_SUFFIX = "".join(['_', RUN_ID])
	base_output_filename = "".join([OUTPUT_FILENAME_PREFIX, 'pdb', OUTPUT_FILENAME_SUFFIX])
	return base_output_filename

##==============================================================================================##

MAXRSS_UNIT_COEFFICIENT = 1024 if not sys.platform.startswith('darwin') else 1

def getMaxRSS():
	return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

def rawMaxRSStoPrettyString(raw_maxrss):
	# get_maxrss returns bytes on macOS and kB on linux. this handles that for you.
	return bytes_to_human_readable_string(raw_maxrss * MAXRSS_UNIT_COEFFICIENT)

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
def initLogger(loggerName, BASE_OUTPUT_FILENAME):
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
	return logger, logfile

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
	
	try:
		# Generate Pattern Database using breadth-first search "backwards" from goal state.
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
			
			#DEBUG
#			if visitedCount == 10000:
#				import pprint
#				pprint.pp(visited, indent=1)
#				break
			
			if visitedCount % 10000 == 0:
				print("Entries collected:", visitedCount)
				
	except KeyboardInterrupt as e:
			logger.info('\nKeyboardInterrupt: Aborted search. No database file created.')
			return visitedCount
	
	
	# Save database / write to file.
	outfile = OUTPUT_DIRECTORY+BASE_OUTPUT_FILENAME
	logger.info("".join(["\nWriting entries to database file:", outfile, " ....."]))
	tryAgain = 'y'
	while tryAgain == 'y':
		try:
			f = open(outfile, "wb")
			pickle.dump(visited, f, pickle.HIGHEST_PROTOCOL)
			logger.info('Done!')
			f.close()
			tryAgain = False
		except OSError as err:
			f.close()
			logger.exception(err)
			maxrss = getMaxRSS()
			logger.info("".join(['(', str(visitedCount), ' entries in memory, using ', rawMaxRSStoPrettyString(maxrss) ,')\n']))
			
			tryAgain = input('\nPress y to retry ')
			if tryAgain == 'y':
				logger.info('\nRetrying ....')
			else:
				logger.info('User aborted.')
	
	return visitedCount

##==============================================================================================##
#		M	A 	I	N
##==============================================================================================##
if __name__ == '__main__':
	pname = parseArgs()
	ptiles = PATTERNS[pname]['pattern tiles']
	dim = PATTERNS[pname]['dim']
	BASE_OUTPUT_FILENAME = getBaseOutputfileName(pname)
	logger, logfile = initLogger(__name__, BASE_OUTPUT_FILENAME)
	
	logger.info(SECTION_SEPARATOR)
	logger.info('Run ID: '+str(RUN_ID))
	logger.info('DB name: '+BASE_OUTPUT_FILENAME)
	logger.info('Pattern type: '+str(pname))
	logger.info("".join([SECTION_SEPARATOR, '\n']))

	stats = dict()
	t_start = time.perf_counter()
	maxrss_start = getMaxRSS()

	#GENERATE DATABASE
	len_db = generatePDB(generateInitialSearchNode(ptiles), dim, len(ptiles), MOVES, OPP_MOVES, BASE_OUTPUT_FILENAME, logger)
	
	stats['entries collected'] = len_db
	stats['platform'] = sys.platform
	stats['time (s)'] = float("{:.2f}".format( time.perf_counter() - t_start))
	stats['memory (raw)'] = getMaxRSS() - maxrss_start
	stats['time (min)'] = float("{:.2f}".format(stats['time (s)'] /60))
	stats['memory (units)'] = rawMaxRSStoPrettyString(stats['memory (raw)'])
	
	stats_as_strings = sorted([ f'{key} : {stats[key]}' for key in stats ])
	logger.info("".join(['\n', SECTION_SEPARATOR]))
	
	for stat in stats_as_strings:
		logger.info(stat) 
	logger.info(SECTION_SEPARATOR)
	logger.info('logfile: '+logfile)
	