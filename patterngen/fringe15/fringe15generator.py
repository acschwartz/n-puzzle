#!/usr/bin/env python3

from collections import deque
from dbtools import db
from pdbgen.moves import *
from sqlite3 import IntegrityError
#from fringe15encoding import *		# seems to be handled by lines ~22-23
from fringe15.fringe15pattern import PATTERN_INFO

class Node:
	"""Search node for BFS in generate_pattern_database"""
	__slots__: ('pattern', 'cost', 'undo')
	def __init__(self, pattern, cost=0, undo=-1):
		self.pattern = pattern
		self.cost = cost
		self.undo = undo



def generate_children(node, dim, moves, opp_moves, 
					  encode, decode):
	"""Generate children of a search Node. Returns children as Nodes"""
	
	node_pattern = decode(node.pattern)
	print(node_pattern)
	node_pip_emptytile = node_pattern[0]
	
	children = []
	moveID = 0		# not using enumerate(moves) because this is faster
	for m in moves:
		print(m)
		if moveID == node.undo:
			# This move generates node's parent - skip 
			moveID += 1
			continue
		print('node_pip_emptytile', node_pip_emptytile, )
		child_pip_emptytile = m(node_pip_emptytile, dim)
		print('child_pip_emptytile:', child_pip_emptytile, '\n\n')
		if child_pip_emptytile is not None:
			child_pattern = list(node_pattern)
			# update pip emptytile in child pattern
			child_pattern[0] = child_pip_emptytile
			print(child_pattern)
			
			child_cost = node.cost
			child_undo = opp_moves[moveID]
			
			try:
				# swapping with another pattern tile 
				# this means we also update cost
				ref_ptile_to_swap = node_pattern.index(child_pip_emptytile)
				child_pattern[ref_ptile_to_swap] = node_pip_emptytile
				child_cost += 1
			except ValueError:
				# swapping with a non-pattern tile
				# nothing else to update, and cost stays the same
				pass
				
			children.append(Node(encode(child_pattern), child_cost, child_undo))
		moveID += 1
	return tuple(children)
	


def generate_pattern_database(pattern_info=PATTERN_INFO, log=None, dbfile=None, moves=MOVE_FUNCTIONS, opp_moves=OPP_MOVE_IDs):
	"""Generates the pattern database"""
	dim = info['dim']
#	ptiles = info['pattern tiles']		# DO I NEED THIS?
	goal_state = info['goal state']
	encode = info['encode']
	decode = info['decode']
	
	# Initialize search queue w/ initial node
	queue = deque([Node(encode(goal_state))])
	
	# Initialize database
	# Stores (Pattern, Cost) of explored nodes
	connection, dbfile = db.initDB(log, dbfile)
	cursor = con.cursor()
	tables = db.createTables(con, dim*dim, log)
	exploredCount = 0
	
	# Initialilze explored set
	# For checking membership w/o querying DB
	explored = set()
	
	
	# Breadth first search finds (Pattern, Cost) values for PDB
	while queue:
		node = queue.popleft()
		
		# Generate node's children
		children = generate_children(node, dim, moves, opp_moves, encode, decode, log)
		for child in children:
			table = tables[child.get_pip_emptytile()]	# TODO: fix
			if not child.pattern in explored:
				queue.append(child)
		
		# Add node to explored
		try:
			insert_into_table = tables[node.get_pip_emptytile()]
			db.insert(connection, insert_into_table, node.pattern, node.cost)
			exploredCount += 1
		except IntegrityError as exc:
			# Pattern already in DB for some reason ...
			pass
		
		if exploredCount % 10000 == 0:
			log.debug(f"Entries collected: {exploredCount}")
			connection.commit()
		
	
	# Tie up loose ends
	log.debug(f'\n\nFINISHED GENERATING PATTERN DATABASE')
	log.debug(f'{exploredCount} entries collected')
	log.debug(f'Committing entries ...')
	connection.commit()
	connection.close()
	log.debug(f'Done.')
	
	return dbfile, tables, exploredCount