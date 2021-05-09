#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import deque
from math import floor
from os import mkdir, path
from resource import getrusage, RUSAGE_SELF
from time import perf_counter, strftime

import logging
import pickle
import sys

##==============================================================================================##
PATTERNS = {
	'15fringe': {
		# 0  -  -  3
		# -  -  -  7
		# -  -  -  11
		# 12 13 14 15
				
				'dim': 4,	# 15-puzzle is 4x4
				'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
				'goal state': (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),
				'empty tile': 0,
				},
	'full8puzzle': {
		# 0  1  2
		# 4  5  6
		# 8  9 10
				'dim': 3,
				'pattern tiles': (1, 2, 3, 4, 5, 6, 7, 8),
				'goal state': (0, 1, 2, 3, 4, 5, 6, 7, 8),
				'empty tile': 0,
				},
	'8puzzlesubproblem': {
	# subproblem of 15-puzzle when fringe pattern in target position
	# maps to 8-puzzle solutions
		# 0  1  2
		# 4  5  6
		# 8  9 10
				'dim': 3,
				'pattern tiles': (1, 2, 4, 5, 6, 8, 9, 10),
				'goal state': (0, 1, 2, 4, 5, 6, 8, 9, 10),
				'empty tile': 0,
				},
}
##==============================================================================================##

RUN_ID = strftime(f'%y%m%d-%H%M%S')
OUTPUT_DIRECTORY = 'output/'

SECTION_SEPARATOR = '=========================================================================='
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

DIRECTIONS = ('left', 'right', 'up', 'down')
MOVES = tuple(map(lambda d: MOVE_INDEX[DIRECTIONS[d]]['func'], range(len(DIRECTIONS))))
OPP_MOVES = tuple(map(lambda d: DIRECTIONS.index(MOVE_INDEX[DIRECTIONS[d]]['opp']), range(len(DIRECTIONS))))

##==============================================================================================##

def parseArgs():
	parser = ArgumentParser(description='n-puzzle pattern database generator')
	parser.add_argument('pattern_name', help='choose a pattern', choices=list(PATTERNS.keys()))
	args = parser.parse_args()
	return args.pattern_name

def initVars():
	pname = parseArgs()
	ptiles = PATTERNS[pname]['pattern tiles']
	dim = PATTERNS[pname]['dim']
	goal_state = PATTERNS[pname]['goal state']
	BASE_OUTPUT_FILENAME = getBaseOutputfileName(pname)
	return pname, ptiles, dim, goal_state, BASE_OUTPUT_FILENAME

def getBaseOutputfileName(pname):
	return f'{pname}_pdb_{RUN_ID}'

def initDirectory(dir):
	if not path.exists(dir):
		mkdir(dir)
		print(f'Directory created: {dir}')
	return

def initLogger(loggerName, base_output_filename, output_path=OUTPUT_DIRECTORY):
	logfile = f'{output_path}{base_output_filename}.log'
	
	# create logger
	logger = logging.getLogger(loggerName)
	logger.setLevel(logging.DEBUG)
	
	# create handlers for logigng to both file and stdout
	stdout_handler = logging.StreamHandler(stream=sys.stdout)
	logger.addHandler(stdout_handler)
	output_file_handler = logging.FileHandler(logfile)
	output_file_handler.setLevel(logging.INFO)	# don't ever want debug stuff in the logfile
	logger.addHandler(output_file_handler)
	return logger, logfile

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

def generateStats(t_start, maxrss_start, len_db):
	stats = dict()
	stats['entries collected'] = len_db
	stats['platform'] = sys.platform
	t_delta = perf_counter() - t_start
	m_delta = getMaxRSS() - maxrss_start
	stats['time_raw'] = f'{t_delta:.2f}'
	stats['memory_raw'] = m_delta
	stats['time'] = sec_to_hours(t_delta)
	stats['memory'] = rawMaxRSStoPrettyString(m_delta)
	return stats

def printHeader(logger, BASE_OUTPUT_FILENAME, pname):
	logger.info(SECTION_SEPARATOR)
	logger.info('Run ID: '+str(RUN_ID))
	logger.info('DB name: '+BASE_OUTPUT_FILENAME)
	logger.info('Pattern type: '+str(pname))
	logger.info(f'{SECTION_SEPARATOR}\n')
	return

def printStats(logger, stats, title=None):
	stats_as_strings = sorted([ f'{key} : {stats[key]}' for key in stats ])
	logger.info(f'\n{SECTION_SEPARATOR}')
	if title:
		logger.info(f'\t{title}')
		logger.info(SECTION_SEPARATOR)
	for stat in stats_as_strings:
		logger.info(stat) 
	logger.info(SECTION_SEPARATOR)
	return

##==============================================================================================##

MAXRSS_UNIT_COEFFICIENT = 1024 if not sys.platform.startswith('darwin') else 1

def getMaxRSS():
	return getrusage(RUSAGE_SELF).ru_maxrss

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

def sec_to_hours(seconds):
# SOURCE: https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
	h=seconds//3600
	m=(seconds%3600)//60
	s=(seconds%3600)%60
	return f'{h} hours {m} mins {s:.2f} sec'

##==============================================================================================##

def makeTargetPattern(ptiles, goal_state):
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
		pattern.append(goal_state.index(tile))
	return bytes(pattern)
	

def generateInitialNode(ptiles, goal_state):
#	return (makeTargetPattern(ptiles), bytes([0, 255, 255]))
	return makeTargetPattern(ptiles, goal_state)+bytes([0,255,255])


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

# NOTE: CONFIRMED THIS IS NOT THE PROPER WAY TO IMPLEMENT A PDB
# YOU ARE NOT SUPPOSED TO MOVE ALL THE TILES, ONLY THE EMPTY ONE (as usual...)

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


def generateChildren(state, state_info, dim, moveSetAsTuple, undoMoves):
# '''
# NEW generateChildren function - Hopefully fixed because now allows swapping between any adjacent tiles
# does not behave same as generateChildrenOptimized, currently.
# TO CLARIFY, THIS ALLOWS SWAPPING BETWEEN ALL PATTERN TILES AND 'BLANK' TILES ON THE BOARD
# therefore for a full-pattern 8-puzzle, it generates double the states it should (362,880 vs 181,440
	
# NOTE: CONFIRMED THIS IS NOT THE PROPER WAY TO IMPLEMENT A PDB
# '''
	state_depth = state_info[0]
	children_depth = state_depth + 1
	action_generate_parent = (state_info[1], state_info[2])
	# ^ this action applied to the current state would generate the parent from which it originated

	
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
			if new_tile_location:
				child = list(state)
				try:
					# i.e. if new_tile_location in state:
					# then we are swapping with another pattern tile and must update both in pattern
					
					other_ptileID = state.index(new_tile_location)
					other_ptile_current_location = new_tile_location
					
					this_ptile_current_location = tileLocationInPuzzle
					
					child[ptileID] = other_ptile_current_location
					child[other_ptileID] = this_ptile_current_location
					# (not super optimized code but extra vars important for clarity)
					# (TODO: may need to optimize to use fewer vars if this becomes a performance problem)
					
				except ValueError:
					# else: new_tile_location not in state
					# then we are swapping with a non-pattern tile
					
					child[ptileID] = new_tile_location
				childInfo = [children_depth, ptileID, undoMoves[moveID]]
				children.append((bytes(child), bytes(childInfo)))
			moveID += 1
		ptileID += 1
	return children


# TODO: Working on this because a full puzzle where you can only move the blank behaves differently
def generateChildren_FullPuzzlePattern(state, state_info, dim, moveSetAsTuple, undoMoves, indexOfEmptyTileInPattern=0):	
# '''
# ONLY THE EMPTY TILE MOVES - AND DOESN'T WORK FOR SOME REASON
# '''
	
	logger.debug(f'Calling generateChildren_FullPuzzlePattern on State: {list(state)}')
	
	state_depth = state_info[0]
	children_depth = state_depth + 1
	action_generate_parent = (state_info[1], state_info[2])
	# ^ this action applied to the current state would generate the parent from which it originated
	emptyTileLocationInPuzzle = state[indexOfEmptyTileInPattern]
	logger.debug(f'emptyTileLocationInPuzzle: {emptyTileLocationInPuzzle}')
	
	children = []
#	moveID = 0
	for moveID, moveFunction in enumerate(moveSetAsTuple):
		logger.debug(f'\nEvaluating moveID {moveID} = {DIRECTIONS[moveID]}')
		action = (indexOfEmptyTileInPattern, moveID)
#		if action == action_generate_parent:
#			logger.debug('action == action_generate_parent')
#			moveID += 1
#			continue
		new_emptyTileLocation = moveFunction(indexOfEmptyTileInPattern, dim)
		logger.debug(f'new empty tile location after proposed move: {new_emptyTileLocation}')
		if new_emptyTileLocation:
			child = list(state)
			try:
				# then we are swapping with another pattern tile and must update both in pattern
				# (if the pattern is the full puzzle, then all tiles are pattern tiles)
				
				other_ptileID = state.index(new_emptyTileLocation)
				other_ptile_current_location = new_emptyTileLocation

				child[indexOfEmptyTileInPattern] = other_ptile_current_location
				child[other_ptileID] = emptyTileLocationInPuzzle
				# (not super optimized code but extra vars important for clarity)
				# (TODO: may need to optimize to use fewer vars if this becomes a performance problem)
				
			except ValueError:
				# else: new_tile_location not in state
				# then we are swapping with a non-pattern tile
				raise RuntimeError
				# This should NOT happen in this case so something would be terribly wrong
				
			childInfo = [children_depth, indexOfEmptyTileInPattern, undoMoves[moveID]]
			children.append((bytes(child), bytes(childInfo)))
#		moveID += 1

	return children


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
			node = queue.popleft()
			state_repr = node[:num_ptiles]
			state_info = node[num_ptiles:]
			
			for child_state, child_info in generateChildren_FullPuzzlePattern(state_repr, state_info, dim, moveSet, oppMoves):
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
	logger.info(f'\nWriting entries to database file: {outfile} .....')
	tryAgain = 'y'
	while tryAgain == 'y':
		try:
			f = open(outfile, "wb")
			pickle.dump(visited, f, pickle.HIGHEST_PROTOCOL)
			logger.info('Done!')
			f.close()
			tryAgain = False
		except FileNotFoundError:
			initDirectory(OUTPUT_DIRECTORY)
			tryAgain = 'y'
		except OSError as err:
			f.close()
			logger.exception(err)
			maxrss = rawMaxRSStoPrettyString(getMaxRSS())
			logger.info(f'({visitedCount}  entries in memory, using {maxrss})\n')
			
			tryAgain = input('\nPress y to retry ')
			if tryAgain == 'y':
				logger.info('\nRetrying ....')
			else:
				logger.info('User aborted.')
	
	return visitedCount


##==============================================================================================##
#		M A I N
##==============================================================================================##
if __name__ == '__main__':
	initDirectory(OUTPUT_DIRECTORY)
	pname, ptiles, dim, goal_state, BASE_OUTPUT_FILENAME = initVars()
	logger, logfile = initLogger(__name__, BASE_OUTPUT_FILENAME, OUTPUT_DIRECTORY)
	printHeader(logger, BASE_OUTPUT_FILENAME, pname)
	
	t_start = perf_counter()
	maxrss_start = getMaxRSS()
	
	len_db = generatePDB(generateInitialNode(ptiles, goal_state), dim, len(ptiles), MOVES, OPP_MOVES, BASE_OUTPUT_FILENAME, logger)
	
	stats = generateStats(t_start, maxrss_start, len_db)
	printStats(logger, stats, title="Stats")
	logger.debug(f'logfile: {logfile}')