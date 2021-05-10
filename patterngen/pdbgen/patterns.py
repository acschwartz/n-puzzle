#!/usr/bin/env python3

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