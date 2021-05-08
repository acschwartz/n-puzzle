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

EMPTY_TILE = 255	# represents tiles which are not included in the pattern

DIRECTIONS = ('left', 'right', 'up', 'down')

MOVE_XY = {
	'left': lambda x,y: (x, y-1),
	'right': lambda x,y: (x, y+1),
	'up': lambda x,y: (x-1, y),
	'down': lambda x,y: (x+1, y),
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
	'left': move_index_left,
	'right': move_index_right,
	'up': move_index_up,
	'down': move_index_down,
		}

MOVE_INDEX_DIRECTIONS = (move_index_left, move_index_right, move_index_up, move_index_down)
# having the functions in a list saves dictionary lookups in MOVE_INDEX

##==============================================================================================##

OUTPUTFILE_IDENTIFIER = ""
OUTPUT_DIRECTORY = 'output/'
MAXRSS_UNIT_COEFFICIENT = 1024 if platform != 'darwin' else 1

##==============================================================================================##
# Functions to convert between 1d-arary indec and coordinates on the puzzle grid

def index_1d_to_xy(i, dim):
	x = i // dim
	y = i % dim
	return (x,y)

def index_xy_to_1d(x, y, dim):
	return x*dim + y

def index_coords_to_1d(coords, dim):
	# coords = (x,y)
	x, y = coords
	return index_xy_to_1d(x, y, dim)


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
	directions = DIRECTIONS
	move_xy = MOVE_XY
	dim = PATTERNS[patternName]['dim']
	ptiles = PATTERNS[patternName]['pattern tiles']
	goalPattern = generateTargetPattern(ptiles, dim)

'''
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
'''

##==============================================================================================##
#print(parseArgs())

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

Comparing values stored as bytes vs as ints
>>> timeit(lambda: b'\x01' == b'\x02')
0.11794590199860977
>>> timeit(lambda: 1 == 2)
0.11735898000006273

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