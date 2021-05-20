#!/usr/bin/env python3

from collections import deque
from dbtools import db
from math import floor, ceil
from pdbgen.moves import *
from sqlite3 import IntegrityError

from pdbgen.moves import DIRECTIONS as dir

from fringe15.fringe15pattern import PATTERN_INFO
from fringe15.fringe15pattern import pretty_pattern


class Node:
    """Search node for BFS in generate_pattern_database
    For 15-puzzle fringe pattern only (currently) """
    __slots__: ('pattern_encoding', 'cost', 'undo')
    def __init__(self, pattern, cost=0, undo=255):
        if isinstance(pattern, bytes):
            self.pattern_encoding = pattern
        elif isinstance(pattern, (list, tuple)):
            self.pattern_encoding = self.encode(pattern)
        else:
            raise TypeError('Node.pattern must be bytes, list, or tuple')
        self.cost = cost
        self.undo = undo
    
    def __repr__(self):
        info = f"""
pattern: {self.get_decoded_pattern()}
pretty:
{pretty_pattern(self.get_decoded_pattern())}
encoding: {self.get_pattern_encoding()}
pip emptytile: {self.get_pip_emptytile()}
undo move: {self.undo_move_repr()}
cost: {self.cost}
        """
        return info

    def __str__(self):
        return f"pattern{self.get_decoded_pattern()}; cost: {self.cost}"

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
    
    def undo_move_repr(self):
        try:
            return dir[self.undo]
        except:
            return None





def generate_children(node, dim, moves, opp_moves):
    """Generate children of a search Node. Returns children as Nodes"""
    
    node_pattern = node.get_decoded_pattern()
    node_pip_emptytile = node.get_pip_emptytile()
    
    children = []
    moveID = 0        # not using enumerate(moves) because this is faster
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
    



def generate_pattern_database(pattern_info=PATTERN_INFO, log=None, dbfile=None, moves=MOVE_FUNCTIONS, opp_moves=OPP_MOVE_IDs):
	"""Generates the pattern database"""
	dim = pattern_info['dim']
	# ptiles = pattern_info['pattern tiles']		# DO I NEED THIS?
	# goal_state = pattern_info['goal state']
#	encode = info['encode']		# No longer need bc of change to Node class
#	decode = info['decode']
	target_pattern = (0,3,7,11,12,13,14,15) 	# TODO: should prob not hardcode this in if poss
	
	# Initialize search queue w/ initial node

	queue = deque([Node(target_pattern)])
	
	# Initialize database
	# Stores (Pattern, Cost) of explored nodes
	connection, dbfile = db.initDB(log, dbfile)
	cursor = connection.cursor()
	tables = db.createTables(connection, dim*dim, log)
	exploredCount = 0
	
	# Initialilze explored set
	# For checking membership w/o querying DB
	explored = set()
	
	
	# Breadth first search finds (Pattern, Cost) values for PDB
	while queue:
		node = queue.popleft()
		
		if node.get_pattern_encoding() not in explored:
			# Generate node's children
			children = generate_children(node, dim, moves, opp_moves)
			for child in children:
				if child.get_pattern_encoding() not in explored:
					queue.append(child)
			
			# Add node info to PDB and explored set
			try:
				insert_into_table = tables[node.get_pip_emptytile()]
				db.insert(connection, insert_into_table, node.get_pattern_encoding(), node.cost)
				
				explored.add(node.get_pattern_encoding())
				exploredCount += 1
			except IntegrityError as exc:
				# Pattern already in DB for some reason ...
				# TODO: does this need more investigating?
				pass
			
			
			if exploredCount % 10000 == 0:
				print(f"Entries collected: {exploredCount:,}")
				if exploredCount % 10000000 == 0:
					connection.commit()
					print(f"Database commit")
		
	
	# Tie up loose ends
	log.debug(f'\n\nFINISHED GENERATING PATTERN DATABASE')
	log.debug(f'{exploredCount} entries collected')
	log.debug(f'Committing entries ...')
	connection.commit()
	connection.close()
	log.debug(f'Done.')
	
	return dbfile, tables, exploredCount
