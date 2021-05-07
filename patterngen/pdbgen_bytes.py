#!/usr/bin/env python3
from argparse import ArgumentParser

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
MAXRSS_UNIT_COEFFICIENT = 1024 if sys.platform != 'darwin' else 1
##==============================================================================================##
PATTERNS = {
	'15fringe': {
				'dim': 4,	# 15-puzzle is 4x4
				'pattern tiles': (0, 3, 7, 11, 12, 13, 14, 15),
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

EMPTY_TILE = 255	# represents tiles which are not included in the pattern
DIM = None				# TODO: remoev
PATTERN_TILES = None	# want all this as local vars

OUTPUTFILE_IDENTIFIER = ""
OUTPUT_DIRECTORY = 'output/'

##==============================================================================================##

def index_1d_to_xy(i, dim):
	x = i // dim
	y = i % dim
	return (x,y)

def index_xy_to_1d(x, y, dim):
	return x*dim + y

def index_coords_to_1d(coords, dim):
	x, y = coords
	return x*dim + y


##==============================================================================================##
def init(patternName='15fringe'):
	# global vars copied to local for speed
	directions = DIRECTIONS
	move_xy = MOVE_XY
	dim = PATTERNS[patternName]['dim']
	ptiles = PATTERNS[patternName]['pattern tiles']
	goalPattern = generateTargetPattern(ptiles, dim)



def generateTargetPattern(ptiles, dim):
	# generate pattern representation of puzzle goal state = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	# which will be the initial state for the backwards BFS used to generate the PDB
	
	# returns: pattern as bytearray where pattern[i] is the index of pattern tile i within the puzzle state
	# e.g. if ptiles = (0,3,7,11,12,13,14,15)
	# pattern = bytearray(b'\x00\xff\xff\x03\xff\xff\xff\x07\xff\xff\xff\x0b\x0c\r\x0e\x0f')
	
	pattern = bytearray([EMPTY_TILE]*(dim**2))
	for tile in ptiles:
		pattern[tile] = tile
	return pattern