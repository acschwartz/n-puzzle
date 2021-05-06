#!/usr/bin/env python3

#!/usr/bin/env python3
import sys
import json
import math
import resource
import time
from collections import deque
from copy import deepcopy

MAXRSS_UNIT_COEFFICIENT = 1024 if sys.platform != 'darwin' else 1
##==============================================================================================##

PATTERNS = {
	'15fringe': {
				'dim': 4,
				'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
				},
}

DIRECTIONS = ('left', 'right', 'up', 'down')

MOVE_XY = {
	'left': lambda x,y: (x, y-1),
	'right': lambda x,y: (x, y+1),
	'up': lambda x,y: (x-1, y),
	'down': lambda x,y: (x+1, y),
		}
##==============================================================================================##

EMPTY_TILE = 0
DIM = None
PATTERN_TILES = None

OUTPUTFILE_IDENTIFIER = ""
OUTPUT_DIRECTORY = 'output/'

##==============================================================================================##

def index_1d_to_xy(i):
	x = i // DIM
	y = i % DIM
	return (x,y)

def index_xy_to_1d(x, y):
	i = x*DIM + y
	return i

def index_coords_to_1d(coords):
	x, y = coords
	i = x*DIM + y
	return i

def string_repr(state):
# input:  [0, 0, 0, (0, 3), 0, 0, 0, (1, 3), 0, 0, 0, (2, 3), (3, 0), (3, 1), (2, 2), (3, 3)]
# output: '(0, 0, 0, 3, 0, 0, 0, 7, 0, 0, 0, 11, 12, 13, 10, 15)'
	state_copy = deepcopy(state)
	for ptile in PATTERN_TILES:
		state_copy[ptile] = index_coords_to_1d(state_copy[ptile])
	return str(tuple(state_copy))

##==============================================================================================##

def get_moves(state):
# Returns list of possible moves
	def isInBounds():
		for c in newCoords:
			if c < 0 or c >= DIM:
				return False
		return True
	def isNotOccupied():
		return newCoords not in state
	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	
	moves = []	
	for tile in PATTERN_TILES:
		x, y = state[tile]
		for direction in DIRECTIONS:
			newCoords = MOVE_XY[direction](x,y)
			if isInBounds() and isNotOccupied():
				moves.append((tile, direction))
	return moves   # e.g. a move is: (3, 'up')


def move(state, move):
# Moves the tile and returns resulting state
	tile, direction = move
	x, y = state[tile]
	
	# Creates a copy of the new_puzzle to change it. (necessary!)
	new_state = deepcopy(state)
	new_state[tile] = MOVE_XY[direction](x,y)
	return new_state

##==============================================================================================##

def init():
	def parseArgs():
		from argparse import ArgumentParser 
		parser = argparse.ArgumentParser(description='n-puzzle pattern database generator')
		parser.add_argument('pattern_name', help='choose a pattern', choices=list(PATTERNS.keys()))
		args = parser.parse_args()
		return args.pattern_name
	
	pname = parseArgs()
	
	global DIM, PATTERN_TILES, OUTPUTFILE_IDENTIFIER
	DIM = PATTERNS[pname]['dim']
	PATTERN_TILES = PATTERNS[pname]['pattern tiles']
	OUTPUTFILE_IDENTIFIER = "".join([str(math.floor(time.time()*1000)-(1619863801*1000)-372000000), '__', pname, '_'])
	print(OUTPUTFILE_IDENTIFIER)
	
	
	
	pattern_target_state = '137bcdef'
	
	
	
	tile_coords = [EMPTY_TILE] * (DIM**2)
	for tile in PATTERN_TILES:
		tile_coords[tile] = index_1d_to_xy(tile)
		
	return tile_coords
	
	
		
##==============================================================================================##

def createDatabase():
	
	start_state = init()
	queue = deque([[start_state, 0]])
	frontier = set()
	frontier.add(string_repr(start_state))
	visited = dict()
	
	while queue:
		state, cost = queue.popleft()
		
		for m in get_moves(state):
			next_state = move(state, m)
			next_state_str = string_repr(next_state)
			if (next_state_str not in visited) and (next_state_str not in frontier):
				queue.append([next_state, cost+1])
				frontier.add(next_state_str)
				
		state_str = string_repr(state)
		visited[state_str] = cost
		frontier.remove(state_str)
#		print(cost, '\t', state_str,'\n')
		
		# Print a progress for every x entries in visited.
		len_visited = len(visited)
		if len(visited) % 10000 == 0:
			print("Entries collected: " + str(len(visited)))
			
		if not frontier:
			break
		
	print("Writing entries to database...")
	filename = "".join([OUTPUTFILE_IDENTIFIER, "database.json"])
	with open(OUTPUT_DIRECTORY + filename, "w") as f:
		json.dump(visited, f)
		
	return filename, len(visited)

		
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
##==============================================================================================##

if __name__ == '__main__':
	
	stats = dict()
	
	stats['time (seconds)'] = time.perf_counter()
	stats['memory'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
	
	
	#GENERATE DATABASE
	stats['_PDB file'], stats['db entries (nodes explored)'] = createDatabase()
	
	
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
	


###~~~~~~~~~~~~~~~~~`
'''
	#TODO: write to db as generating entries; save your spot in case search quits

	#TODO: Hex representation ideas
		let ptiles = (3, 7, 11, 12, 13, 14, 15)
	We only need to store the index that each ptile occupies in the 15-puzzle
	Hexadecimal digits represent 0-15. Perfect for our indices
	(1)  0123456789ABCDEF  would be goal state of 15-puzzle
		 00030007000bcdef  would be this state with only the ptiles
		NOTE: /PROBLEM: Python hex representation doesn't keep leading zeroes
	
	(2) could also represent the above (goal) state as:
		37bcdef
		We already know what the ptiles are and they are numerically ordered
		we could literally parse this like
		for s in string
			s = index/location of ptiles[s]

	(3) dealing with leading zero problem - just add a throwaway 1 at the beginning ot ignore
		137bcdef
		str[0] = throwaway
		str[1] = index of ptiles[1]
		str[2] = location of ptiles[2]
			etc...

	(4) also can append the heuristic val. I believe max depth is 62, which takes two hex digits to represent.
		the last two can 
		137bcdef00 --> 0x137bcdef00
		BUT if we append the heuristic, it makes it tough to seach for the string in the explored set/db.. 

	(5) or can split it up into a byte-string
		then no need for leading 1
		37 bc de f --> so maybe we do want a leading or trailing zero
		\x03 \x7b \xcd \xef  or \x37 \xbc \xde \xf0
		A byte represents values from 0 to 256
		
		
'''