#!/usr/bin/env python3

import unittest
#from math import floor, ceil
#from timeit import timeit

import inspect
myself = lambda: inspect.stack()[1][3]

from dbtools import db
from fringe15.fringe15encoding import *
from fringe15.fringe15pattern import *

DEBUG = True
TIMEIT = False



##====================================================================##

#  U N I T   T E S T S

##====================================================================##

class TestEncoding(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestEncoding, self).__init__(*args, **kwargs)
		self.puzzles = (
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
		)
	
	def test_encode_pattern(self):
		for puzzle in self.puzzles:
			self.assertEqual(encode_pattern(puzzle['pattern'], DEBUG), puzzle['encoding'])
	
	def test_decode_pattern(self):
		for puzzle in self.puzzles:
			self.assertEqual(decode_pattern(puzzle['encoding']), puzzle['pattern'])
		
	def test_encode_decode(self):
		for puzzle in self.puzzles:
			pattern = puzzle['pattern']
			encoded = encode_pattern(puzzle['pattern'], DEBUG)
			self.assertEqual(decode_pattern(encoded), pattern)
		for puzzle in self.puzzles:
			self.assertEqual(decode_pattern(encode_pattern(puzzle['pattern'])), puzzle['pattern'])
			self.assertEqual(encode_pattern(decode_pattern(puzzle['encoding'])), puzzle['encoding'])
	
#	def test_encode15puzzle_fringe_DummyTile(self):
#		pname = '15puzzle_fringe'
#		ptiles = patterns.PATTERN_INFO[pname]['pattern tiles']
#		goalstate = patterns.PATTERN_INFO[pname]['goal state']
#		emptytile = patterns.PATTERN_INFO[pname]['empty tile']
#		encode = patterns.PATTERN_INFO[pname]['encode']
#		decode = patterns.PATTERN_INFO[pname]['decode']
	
#	def test_encode15puzzle_fringe_DummyTile(self):
#		puzzles = self.fifteenpuzzles_fringe
#		res = []
#		for p in puzzles:
#			res.append(encoding.encode15puzzle_fringe_DummyTile(p['pattern']))
#			
#		for i, e in enumerate(res):
#			self.assertEqual(e, puzzles[i]['encoding'])
			
			
#	def test_decode15puzzle_fringe_DummyTile(self):
#		puzzles = self.fifteenpuzzles_fringe
#		res = []
#		for p in puzzles:
#			res.append(encoding.decode15puzzle_fringe_DummyTile(p['encoding']))
#			
#		for i, e in enumerate(res):
#			self.assertEqual(e, puzzles[i]['pattern'])
	

		
		

##==============================================================================================##
if __name__ == '__main__':
	unittest.main()