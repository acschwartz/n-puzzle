#!/usr/bin/env python3

import unittest
#from math import floor, ceil
#from timeit import timeit

import inspect
myself = lambda: inspect.stack()[1][3]

from dbtools import db
from fringe15.fringe15encoding import *
from fringe15.fringe15generator import *
from fringe15.fringe15pattern import *

from pdbgen.moves import MOVE_FUNCTIONS as moves
from pdbgen.moves import OPP_MOVE_IDs as opp_moves
from pdbgen.moves import DIRECTIONS as dir

DEBUG = True
TIMEIT = False

dim = 4
puzzles = (
			{ 	# 0  -  -  3
				# -  -  -  7
				# -  -  -  11
				# 12 13 14 15
				'pattern': (0,3,7,11,12,13,14,15), 
				'encoding': b'\x03\x7b\xcd\xef' 
			},
			{ 	# -  0  -  3
				# -  7  -  -
				# -  13 11 15
				# 12 -  -  14
				'pattern': (1,3,5,10,12,9,15,11), 
				'encoding': b'\x13\x5a\xc9\xfb' 
			},
			{ 	# 15  -  - 14
				#  -  -  - 13
				#  -  -  - 12
				# 11  7  3  0
				'pattern': (15,14,13,12,11,7,3,0), 
				'encoding': b'\xfe\xdc\xb7\x30' 
			},
			{ 	# -  -  -  3
				# -  -  -  7
				# -  -  0  11
				# 12 13 14 15
				'pattern': (10,3,7,11,12,13,14,15), 
				'encoding': b'\xa3\x7b\xcd\xef' 
			},
		)


##====================================================================##

#  U N I T   T E S T S

##====================================================================##

class TestEncoding(unittest.TestCase):
	
	def test_encode_pattern(self):
		for puzzle in puzzles:
			self.assertEqual(encode_pattern(puzzle['pattern'], DEBUG), puzzle['encoding'])
	
	def test_decode_pattern(self):
		for puzzle in puzzles:
			self.assertEqual(decode_pattern(puzzle['encoding']), puzzle['pattern'])
		
	def test_encode_decode(self):
		for puzzle in puzzles:
			pattern = puzzle['pattern']
			encoded = encode_pattern(puzzle['pattern'], DEBUG)
			self.assertEqual(decode_pattern(encoded), pattern)
		for puzzle in puzzles:
			self.assertEqual(decode_pattern(encode_pattern(puzzle['pattern'])), puzzle['pattern'])
			self.assertEqual(encode_pattern(decode_pattern(puzzle['encoding'])), puzzle['encoding'])
	
	def test_decode_singlebyte(self):
		test_inputs = [
			{'e': bytes([10]),
			 'd': (0, 10) }, 
			{'e': bytes([254]),
			 'd': (15, 14) },
		]
		for i in test_inputs:
			self.assertEqual(decode_pattern(i['e']), i['d'])
	
	def test_decode_stub_get_0th_element(self):
		test_inputs = [
			{'e': bytes([10]),
			 'd': (0, 10) }, 
			{'e': bytes([254]),
			 'd': (15, 14) },
		]
		for i in test_inputs:
			self.assertEqual(decode_pattern(i['e'])[0], i['d'][0])
	
	
	 
class TestGenerateChildren(unittest.TestCase):
	
	def test_puzzle0(self):
		puzzle = puzzles[0]
		# 0  -  -  3
		# -  -  -  7
		# -  -  -  11
		# 12 13 14 15
		
		node = Node(encode_pattern(puzzle['pattern']))
		children = generate_children(node, dim, moves, opp_moves, encode_pattern, decode_pattern)
		expected_children = [
			Node(encode_pattern((1,3,7,11,12,13,14,15)), cost=0, undo=dir.index('left')),
			Node(encode_pattern((4,3,7,11,12,13,14,15)), cost=0, undo=dir.index('up')),
		]
		for i, child in enumerate(children):
			self.assertEqual(child.get_decoded_pattern(), expected_children[i].get_decoded_pattern())
		
		
	def test_puzzle3(self):
		puzzle = puzzles[3]
		# -  -  -  3
		# -  -  -  7
		# -  -  0  11
		# 12 13 14 15
		
		node = Node(encode_pattern(puzzle['pattern']))
		children = generate_children(node, dim, moves, opp_moves, encode_pattern, decode_pattern)
		expected_children = [
			Node(encode_pattern((9,3,7,11,12,13,14,15)), cost=0, undo=dir.index('right')),
			Node(encode_pattern((11,3,7,10,12,13,14,15)), cost=1, undo=dir.index('left')),
			Node(encode_pattern((6,3,7,11,12,13,14,15)), cost=0, undo=dir.index('down')),
			Node(encode_pattern((14,3,7,11,12,13,10,15)), cost=1, undo=dir.index('up')),
		]
		for i, child in enumerate(children):
			self.assertEqual(child.get_decoded_pattern(), expected_children[i].get_decoded_pattern())
		
		
		
		

##====================================================================##
if __name__ == '__main__':
	unittest.main()