#!/usr/bin/env python3

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

MOVES_INFO = {
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
# a tuple to be able to iterate through in consistent order

MOVE_FUNCTIONS = tuple(map(lambda d: MOVES_INFO[DIRECTIONS[d]]['func'], range(len(DIRECTIONS))))
# functions stored in tuple to iterate through in order

OPP_MOVE_IDs = tuple(map(lambda d: DIRECTIONS.index(MOVES_INFO[DIRECTIONS[d]]['opp']), range(len(DIRECTIONS))))
