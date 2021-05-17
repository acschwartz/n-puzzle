#!/usr/bin/env python3

from fringe15.fringe15encoding import *

##==============================================================================================##
PATTERN_INFO = {
	'15puzzle_fringe': {
		# 0  -  -  3
		# -  -  -  7
		# -  -  -  11
		# 12 13 14 15
		
				'dim': 4,	# 15-puzzle is 4x4
				'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
				'goal state': (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),
				'empty tile': 0,
				'encode': encode_pattern,
#				'decode': decode15puzzle_fringe_DummyTile,
				},
}
##==============================================================================================##
