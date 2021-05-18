#!/usr/bin/env python3

from collections import deque
from dbtools import db
from math import floor, ceil
from pdbgen.moves import *
from sqlite3 import IntegrityError

from fringe15.fringe15pattern import PATTERN_INFO

class Node:
	"""Search node for BFS in generate_pattern_database"""
	__slots__: ('pattern_encoding', 'cost', 'undo')
	def __init__(self, pattern, cost=0, undo=-1):
		if isinstance(pattern, bytes):
			self.pattern_encoding = pattern
		elif isinstance(pattern, (list, tuple)):
			self.pattern_encoding = self.encode(pattern)
		else:
			raise TypeError('Node.pattern must be bytes, list, or tuple')
		self.cost = cost
		self.undo = undo
	
	def encode(self, pattern):
		"""copied from fringe15encoding.py
		Input: pattern repr. WITH empty tile | Return: bytes encoding
		e.g. in: (0,3,7,11,12,13,14,15) | out: b'x\03x\7bx\cdx\ef'
		"""
		encoding = [0, 0, 0, 0]
		i=0
		for n in pattern:
			encoding[floor(i/2)] += n*(1<<(4*(~i&1)))
			i+=1
		return bytes(encoding)
	
	def decode(self, bytestr):
		"""copied from fringe15pattern.py
		Input: byte encoding | Return: pattern repr. WITH empty tile
		e.g. out: b'x\03x\7bx\cdx\ef' | out: (0,3,7,11,12,13,14,15)
		"""
		decoded = []
		for n in bytestr:
			decoded.append((n//16) % 16)
			decoded.append(n%16)
		return tuple(decoded)
	
	def get_pip_emptytile(self):
		# assuming emptytile is at index (ref) 0 in pattern
		return self.decode(self.pattern_encoding)[0]
	
	def get_pattern_encoding(self):
		return self.pattern_encoding
	
	def get_decoded_pattern(self):
		return self.decode(self.pattern_encoding)



def generate_children(node, dim, moves, opp_moves, 
					  encode, decode):
	"""Generate children of a search Node. Returns children as Nodes"""
	
	node_pattern = node.get_decoded_pattern()
	node_pip_emptytile = node.get_pip_emptytile()
	
	children = []
	moveID = 0		# not using enumerate(moves) because this is faster
	for m in moves:
		if moveID == node.undo:
			# This move generates node's parent - skip 
			moveID += 1
			continue
		child_pip_emptytile = m(node_pip_emptytile, dim)
		if child_pip_emptytile is not None:
			child_pattern = list(node_pattern)
			child_cost = node.cost
			child_undo = opp_moves[moveID]
			
			# update pip emptytile in child pattern
			child_pattern[0] = child_pip_emptytile
			
			try:
				# swapping with another pattern tile 
				# this means we also update cost
				ref_ptile_to_swap = node_pattern.index(child_pip_emptytile)
				child_pattern[ref_ptile_to_swap] = node_pip_emptytile
				child_cost += 1
			except ValueError:
				# else, swapping with a non-pattern tile
				# nothing else to update, and cost stays the same
				pass
				
			children.append(Node(child_pattern, child_cost, child_undo))
		moveID += 1
	return tuple(children)
	


#def generate_pattern_database(pattern_info=PATTERN_INFO, log=None, dbfile=None, moves=MOVE_FUNCTIONS, opp_moves=OPP_MOVE_IDs):
#	"""Generates the pattern database"""
#	dim = info['dim']
##	ptiles = info['pattern tiles']		# DO I NEED THIS?
#	goal_state = info['goal state']
#	encode = info['encode']
#	decode = info['decode']
#	
#	# Initialize search queue w/ initial node
#	queue = deque([Node(encode(goal_state))])
#	
#	# Initialize database
#	# Stores (Pattern, Cost) of explored nodes
#	connection, dbfile = db.initDB(log, dbfile)
#	cursor = con.cursor()
#	tables = db.createTables(con, dim*dim, log)
#	exploredCount = 0
#	
#	# Initialilze explored set
#	# For checking membership w/o querying DB
#	explored = set()
#	
#	
#	# Breadth first search finds (Pattern, Cost) values for PDB
#	while queue:
#		node = queue.popleft()
#		
#		# Generate node's children
#		children = generate_children(node, dim, moves, opp_moves, encode, decode, log)
#		for child in children:
#			table = tables[child.get_pip_emptytile()]	# TODO: fix
#			if not child.pattern in explored:
#				queue.append(child)
#		
#		# Add node to explored
#		try:
#			insert_into_table = tables[node.get_pip_emptytile()]
#			db.insert(connection, insert_into_table, node.pattern, node.cost)
#			exploredCount += 1
#		except IntegrityError as exc:
#			# Pattern already in DB for some reason ...
#			pass
#		
#		if exploredCount % 10000 == 0:
#			log.debug(f"Entries collected: {exploredCount}")
#			connection.commit()
#		
#	
#	# Tie up loose ends
#	log.debug(f'\n\nFINISHED GENERATING PATTERN DATABASE')
#	log.debug(f'{exploredCount} entries collected')
#	log.debug(f'Committing entries ...')
#	connection.commit()
#	connection.close()
#	log.debug(f'Done.')
#	
#	return dbfile, tables, exploredCount