#!/usr/bin/env python3

#!/usr/bin/env python3
from math import floor, ceil

# 0  1  2
# 4  5  6
# 8  9 10
PUZZLE_INFO = {
				'dim': 3,
				'pattern tiles': (1, 2, 3, 4, 5, 6, 7, 8),
				'goal_state': 'zero_first',
				'goal state repr': (0, 1, 2, 3, 4, 5, 6, 7, 8),
				'empty tile': 0,
				'dbfile': 'npuzzle/pdb/eightpuzzle/full8puzzle/full8puzzle_pdb_210510-122014.db',
				}


BASE_TABLE_NAME = 'PatternCosts_EmptyTileLocation_'
N_TABLES = PUZZLE_INFO['dim']**2
TABLES = [f'{BASE_TABLE_NAME}{N}' for N in range(N_TABLES)]



def convertToQueryable(state):
	# state will be of form (0, 1, 2, 3, 4, .. 8)
	# where the index is the actual location of in the puzzle
	# and the value is the nubmered square
	# the pattern is represented the opposite of this
	ptiles = PUZZLE_INFO['pattern tiles']
	pattern = [state.index(tile) for tile in ptiles]
	emptyTileLocation = state.index(0)
	encoding = encode(pattern)
	table = TABLES[emptyTileLocation]
	return(table, encoding)
	

def encode(pattern):
# includes locations of the pattern tiles but not the empty tile
	encoding = [0, 0, 0, 0]
	i=0
	for n in pattern:
		encoding[floor(i/2)] += n*(1<<(4*(~i&1)))
		i+=1
	return bytes(encoding)


def decode(bytestr):
# includes locations of the pattern tiles but not the empty tile
	decoded = []
	for n in bytestr:
		decoded.append((n//16) % 16)
		decoded.append(n%16)
	return tuple(decoded)

def convertPatternReprToStateRepr(patternform):
	ptiles = PUZZLE_INFO['pattern tiles']
	dim = PUZZLE_INFO['dim']
	
	state = [0]*(dim*dim)
	for ptileID, location in enumerate(patternform):
		state[location] = ptiles[ptileID]
	return tuple(state)
	