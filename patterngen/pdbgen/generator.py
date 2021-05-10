#!/usr/bin/env python3

from collections import deque
from pdbgen.moves import *


def makeInitialNode(ptiles, emptytile, goalstate, encode):
	pattern = [goalstate.index(tile) for tile in ptiles]
	emptyTileLocation = goalstate.index(emptytile)
	encoding = encode(pattern)
	# then add additional info that makes it a node
	# node info [cost, emptyTileLocation, undoMove]
	return encoding+bytes([0, emptyTileLocation, 255]), len(encoding)

def splitNode(node, len_encoded_pattern):
# returns encoded pattern, cost, location of empty tile, undo move
#	return node[:len_encoded_pattern], node[len_encoded_pattern], node[len_encoded_pattern+1], node[len_encoded_pattern+2]
	return node[:len_encoded_pattern], {'cost': node[len_encoded_pattern], 'emptyTileLocation': node[len_encoded_pattern+1], 'undoMove': node[len_encoded_pattern+2]}

def generatePatternDatabase(info, log, moves=MOVE_FUNCTIONS, opp_moves=OPP_MOVE_IDs):
# (initNode, dim, num_ptiles, moveSet, oppMoves, BASE_OUTPUT_FILENAME, logger)
	dim = info['dim']
	ptiles = info['pattern tiles']
	empty_tile = info['empty tile']
	goalstate = info['goal state']
	encode = info['encode']
	decode = info['decode']
	
	queue = deque([initNode])
	
#	try:
#		# Generate Pattern Database using breadth-first search "backwards" from goal state.
#		
#		
#				
#	except KeyboardInterrupt as e:
#			logger.info('\nKeyboardInterrupt: Aborted search. No database file created.')
#			return visitedCount