#!/usr/bin/env python3

PDBINFO = {
	'fringe': {
			#'file': 	'npuzzle/pdb/8puzzle/zerofirst_full_board.json',
			'size':		4,
			'goal_state': 'zero_first',
			'pattern_tiles': (3, 7, 11, 12, 13, 14, 15),
		}
}

ptiles = PDBINFO['fringe']['pattern_tiles']

state = (3, 14, 9, 11, 5, 4, 8, 2, 13, 12, 6, 7, 10, 1, 15, 0)

pattern1 = [0]*16
for i, tile in enumerate(state):
	if tile in ptiles:
		pattern1[i] = tile
		
pattern1 = [0]*16
for i in range(len(state)):
	tile = state[i]
	if tile in ptiles:
		pattern1[i] = tile
p1 = str(tuple(pattern1))
		
pattern2 = dict()
for tile in ptiles:
	pattern2[tile] = state.index(tile)
p2 = str(pattern2)

pattern3 = [0]*16
for tile in ptiles:
	pattern3[tile] = state.index(tile)
p3 = str(tuple(pattern3))


class State():
	