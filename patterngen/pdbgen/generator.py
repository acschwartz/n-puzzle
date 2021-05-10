#!/usr/bin/env python3

from collections import deque
from dbtools import db
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
	return node[:len_encoded_pattern], {'cost': node[len_encoded_pattern], 'emptyTileLocation': node[len_encoded_pattern+1], 'undo': node[len_encoded_pattern+2]}

def generatePatternDatabase(info, log, RUN_ID, moves=MOVE_FUNCTIONS, opp_moves=OPP_MOVE_IDs):
# (initNode, dim, num_ptiles, moveSet, oppMoves, BASE_OUTPUT_FILENAME, logger)
	dim = info['dim']
	ptiles = info['pattern tiles']
	empty_tile = info['empty tile']
	goalstate = info['goal state']
	encode = info['encode']
	decode = info['decode']
	init_node, len_pattern_encoding = makeInitialNode(ptiles, empty_tile, goalstate, encode)
	
	queue = deque([init_node])
	
	# Visited entries stored in database
	visitedCount = 0
#	con, cur = db.initDB(log, f'{RUN_ID}.db')
	con, cur = db.initDB(log)
	tablenames = db.createTables(cur, dim*dim, log)

	# Begin Generating Pattern Database
	# using breadth-first search "backwards" from target pattern
	# TODO: Idk if I still need a try/ except block here
	
	while queue:
		node = queue.popleft()
		# split node whatever
		pattern, nodeinfo = splitNode(node, len_pattern_encoding)
		
		print(pattern)
		print(list(pattern))
		print(nodeinfo)
		
		# generate children
		children = generateChildren(pattern, nodeinfo, dim, ptiles, moves, opp_moves, encode, decode, log)

def generateChildren(pattern, stateinfo, dim, ptiles, moves, opp_moves, encode, decode, log=None):
	from pdbgen.moves import DIRECTIONS as DIRS
	log.debug('\n\n ---- generateChildren -----')
	emptyTileLocation = stateinfo['emptyTileLocation']
	current_cost = stateinfo['cost']
	undo = stateinfo['undo']
	decoded_pattern = decode(pattern)
	# ^ this action applied to the current state would generate the parent from which it originated
	
	log.debug(f'DECODED PATTERN: {decoded_pattern}')
	log.debug(f'EMPTY TILE LOCATION: {emptyTileLocation}')
	log.debug(f'\tcurrent cost: {current_cost}')
	log.debug(f'\tundo move: {undo} in {list(enumerate(DIRS))}')
	
	children = []
	moveID = 0		# not using enumerate(moves) because this is faster
	for m in moves:
		log.debug(f'\n  (({moveID})) EVALUATING POTENTIAL MOVE: {DIRS[moveID]}....')
		if moveID == undo:
			print(f'This is the undo move {moves[moveID]}, skipping')
			moveID += 1
			continue
		new_emptyTileLocation = m(emptyTileLocation, dim)
		log.debug(f'New empty tile location: {new_emptyTileLocation}')
		if new_emptyTileLocation:
			child = list(decoded_pattern)
			childinfo = {}
			childinfo['emptyTileLocation'] = new_emptyTileLocation
			childinfo['undo'] = opp_moves[moveID]
			try:
				# swapping with another pattern tile 
				# this means we also update cost
				ptileID = decoded_pattern.index(new_emptyTileLocation)
				child[ptileID] = emptyTileLocation
				childinfo['cost'] = current_cost + 1
				
				log.debug(f'Pattern was: {decoded_pattern}')
				log.debug(f'Swapped with another pattern tile represented by index {ptileID} in the pattern')
				log.debug(f'That tile is now at location {emptyTileLocation}')
				log.debug(f"Pattern cost incremented to {childinfo['cost']}")
			except ValueError:
				# swapping with a non-pattern tile
				# and cost stays the same
				childinfo['cost'] = current_cost
				
				log.debug(f'Swapped with non-pattern tile.')
				log.debug(f'Pattern and cost do not need to be updated.')
			log.debug(f'RESULTING CHILD STATE: {child}')
			log.debug(f'\tchildinfo: {childinfo}')
			children.append((encode(child), childinfo))
		moveID += 1
	
	log.debug(f'\nFinished generating children: \n{children}')
	log.debug(f'~~~~~~~~\n')
	return children