#!/usr/bin/env python3

import unittest
#from math import floor, ceil
#from timeit import timeit

import inspect
myself = lambda: inspect.stack()[1][3]

from dbtools import db
#from pdbgen import generator
#from pdbgen import logger
#from pdbgen import encoding
#from pdbgen import patterns

DEBUG = False
TIMEIT = False



##====================================================================##

#  U N I T   T E S T S

##====================================================================##

class TestEncoding(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestEncoding, self).__init__(*args, **kwargs)
		self.fifteenpuzzles_fringe = (
			{ 'pattern': (3,7,11,12,13,14,15), 'encoding': b'\x13\x7b\xcd\xef' },
			{ 'pattern': (3,7,0,12,13,14,15), 'encoding': b'\x13\x70\xcd\xef' },
		)
	
	
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