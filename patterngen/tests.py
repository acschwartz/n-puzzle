#!/usr/bin/env python3

import unittest

dim_15puzzle = 4


##==============================================================================================##

#  U N I T   T E S T S

##==============================================================================================##

class TestIndexConversions_1d_xy(unittest.TestCase):
	pass
	
#	def test_index_1d_to_xy(self):
#		dim = dim_15puzzle
#		self.assertEqual(index_1d_to_xy(14, dim), (3,2), "Should be (3,2)")
#		self.assertEqual(index_1d_to_xy(9, dim), (2,1), "Should be (2,1)")
#		
#	def test_index_xy_to_1d(self):
#		dim = dim_15puzzle
#		self.assertEqual(index_xy_to_1d(3, 2, dim), 14, "Should be 14")
#		self.assertEqual(index_xy_to_1d(2, 1, dim), 9, "Should be 9")
#	
#	def test_index_coords_to_1d(self):
#		dim = dim_15puzzle
#		self.assertEqual(index_coords_to_1d((0,1), dim), 1, "Should be 1")
#		self.assertEqual(index_coords_to_1d((2,3), dim), 11, "Should be 11")





##==============================================================================================##
if __name__ == '__main__':
	unittest.main()