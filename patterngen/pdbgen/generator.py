#!/usr/bin/env python3

from collections import deque
from dbtools import db
from pdbgen.moves import *
from sqlite3 import IntegrityError
from pdbgen.encoding import decode8puzzle


def makeInitialNode(ptiles, emptytile, goalstate, encode):
	pattern = [goalstate.index(tile) for tile in ptiles]
	emptyTileLocation = goalstate.index(emptytile)
	encoding = encode(pattern)
	# then add additional info that makes it a node
	# node info [cost, emptyTileLocation, undoMove]
	return encoding+bytes([0, emptyTileLocation, 255]), len(encoding)

def makeNode(encodedPattern, stateinfo):
#	print(f'makeNode: {decode8puzzle(encodedPattern)}, {stateinfo}')
#	info = [stateinfo['cost'], stateinfo['emptyTileLocation'], stateinfo['undo']]
	info = [stateinfo['c'], stateinfo['e'], stateinfo['u']]  # hoping this optimizes memory
	return encodedPattern+bytes(info)
# TODO: maybe could optimize

def splitNode(node, len_encoded_pattern):
# returns encoded pattern, cost, location of empty tile, undo move
#	return node[:len_encoded_pattern], node[len_encoded_pattern], node[len_encoded_pattern+1], node[len_encoded_pattern+2]
	return node[:len_encoded_pattern], {'c': node[len_encoded_pattern], 'e': node[len_encoded_pattern+1], 'u': node[len_encoded_pattern+2]}


def generatePatternDatabase(info, log, dbfile=None, moves=MOVE_FUNCTIONS, opp_moves=OPP_MOVE_IDs):
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
	con, dbfile = db.initDB(log, dbfile)
	cur = con.cursor()
	
	tables = db.createTables(con, dim*dim, log)
#	log.debug(f'\nTables created: {tuple(enumerate(tables))}\n')

	# Begin Generating Pattern Database
	# using breadth-first search "backwards" from target pattern
	# TODO: Idk if I still need a try/ except block here
	
	while queue:
		node = queue.popleft()
#		log.debug(f'Queue size: {len(queue)}')
		pattern, nodeinfo = splitNode(node, len_pattern_encoding)
		
#		log.debug(f'\n\n=========== POPPED! Node off Queue ==============')
#		log.debug(f'\tPattern: {decode(pattern)}')
#		log.debug(f'\tInfo: {nodeinfo}')
		
		# generate children
		children = generateChildren(pattern, nodeinfo, dim, ptiles, moves, opp_moves, encode, decode, log)
		for child_pattern, childinfo in children:
			table = tables[childinfo['e']]
#			log.debug(f"Checking table {table} for pattern {decode(child_pattern)} (empty tile loc: {childinfo['e']})")
			if not db.checkRowExists(con, table, child_pattern):
				queue.append(makeNode(child_pattern, childinfo))
#				log.debug(f'\tChild pattern {child_pattern} not in db; added to queue.')
#			else: log.debug(f'\tChild pattern {child_pattern} already in db.')
		
		# add node to visited
		try:
			tbl = tables[nodeinfo['e']]
			c = nodeinfo['c']
			db.insert(con, tbl, pattern, c)
			visitedCount += 1
#			log.debug(f"\nNode fully explored; added ({pattern}, {c}) to table {tbl}")
		except IntegrityError as exc:
#			log.debug(f'\n\n~~~~~~~\nTried to insert ({pattern}, {c}) into table: {tbl}')
#			log.debug(f'Entry already exists? {db.checkRowExists(con, tbl, pattern)}')
#			log.debug(f'Executing query: SELECT * from {tbl} where pattern = {pattern}')
#			res = cur.execute("SELECT * from %s where %s = ?"%(tbl, 'pattern'), (pattern,))
#			log.debug(f'Results: ')
#			for row in res:
#				log.debug(row)
			pass
		
#		log.debug(f"Explored: {visitedCount}\n")
##		log.debug(f'~~~~~~~~ Queue: ~~~~~~')
##		import pprint
##		pprint.pp(queue, indent=2)
#		log.debug(f'~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
		
		if visitedCount % 10000 == 0:
			log.debug(f"Entries collected: {visitedCount}")
	
	
	log.debug(f'\n\nFINISHED GENERATING PATTERN DATABASE')
	log.debug(f'{visitedCount} entries collected')
	log.debug(f'Committing database ...')
	con.commit()
	con.close()
	log.debug(f'Done.')
		
	return dbfile, tables, visitedCount


def generateChildren(pattern, stateinfo, dim, ptiles, moves, opp_moves, encode, decode, log):
#	from pdbgen.moves import DIRECTIONS as DIRS	# for DEBUGGING only
#	log.debug('\n\n ---- generateChildren -----')
	
	emptyTileLocation = stateinfo['e']
	current_cost = stateinfo['c']
	undo = stateinfo['u']
	decoded_pattern = decode(pattern)
	# ^ this action applied to the current state would generate the parent from which it originated
	
#	log.debug(f'DECODED PATTERN: {decoded_pattern}')
#	log.debug(f'EMPTY TILE LOCATION: {emptyTileLocation}')
#	log.debug(f'\tcurrent cost: {current_cost}')
#	log.debug(f'\tundo move: {undo} in {list(enumerate(DIRS))}')
	
	children = []
	moveID = 0		# not using enumerate(moves) because this is faster
	for m in moves:
#		log.debug(f'\n  (({moveID})) EVALUATING POTENTIAL MOVE: {DIRS[moveID]}....')
		if moveID == undo:
#			log.debug(f'This is the undo move {moves[moveID]}, skipping')
			moveID += 1
			continue
		new_emptyTileLocation = m(emptyTileLocation, dim)
#		log.debug(f'New empty tile location: {new_emptyTileLocation}')
		if new_emptyTileLocation is not None:
			child = list(decoded_pattern)
			childinfo = {}
			childinfo['e'] = new_emptyTileLocation
			childinfo['u'] = opp_moves[moveID]
			try:
				# swapping with another pattern tile 
				# this means we also update cost
				ptileID = decoded_pattern.index(new_emptyTileLocation)
				child[ptileID] = emptyTileLocation
				childinfo['c'] = current_cost + 1
				
#				log.debug(f'Pattern was: {decoded_pattern}')
#				log.debug(f'Swapped with another pattern tile represented by index {ptileID} in the pattern')
#				log.debug(f'That tile is now at location {emptyTileLocation}')
#				log.debug(f"Pattern cost incremented to {childinfo['c']}")
			except ValueError:
				# swapping with a non-pattern tile
				# and cost stays the same
				childinfo['c'] = current_cost
				
#				log.debug(f'Swapped with non-pattern tile.')
#				log.debug(f'Pattern and cost do not need to be updated.')
#			log.debug(f'RESULTING CHILD PATTERN: {child}')
#			log.debug(f'\tchildinfo: {childinfo}')
			children.append((encode(child), childinfo))
		moveID += 1
	
#	log.debug(f'\nFinished generating children: \n{children}')
	return tuple(children)