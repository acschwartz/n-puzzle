#!/usr/bin/env python3

from pdbgen_bytes import *
import unittest

dim_15puzzle = 4

class TestIndexConversions_1d_xy(unittest.TestCase):
	
	def test_index_1d_to_xy(self):
		dim = dim_15puzzle
		self.assertEqual(index_1d_to_xy(14, dim), (3,2), "Should be (3,2)")
		self.assertEqual(index_1d_to_xy(9, dim), (2,1), "Should be (2,1)")
		
	def test_index_xy_to_1d(self):
		dim = dim_15puzzle
		self.assertEqual(index_xy_to_1d(3, 2, dim), 14, "Should be 14")
		self.assertEqual(index_xy_to_1d(2, 1, dim), 9, "Should be 9")
	
	def test_index_coords_to_1d(self):
		dim = dim_15puzzle
		self.assertEqual(index_coords_to_1d((0,1), dim), 1, "Should be 1")
		self.assertEqual(index_coords_to_1d((2,3), dim), 11, "Should be 11")


class TestMOVE_XY(unittest.TestCase):
	
	def test_MOVE_XY_left(self):
		self.assertEqual(MOVE_XY['left'](0,1), (0,0), "Should be (0,0)")
		self.assertEqual(MOVE_XY['left'](0,0), (0,-1), "Should be (0,-1)")
	
	def test_MOVE_XY_right(self):
		self.assertEqual(MOVE_XY['right'](0,1), (0,2), "Should be (0,2)")
		self.assertEqual(MOVE_XY['right'](0,3), (0,4), "Should be (0,4)")
	
	def test_MOVE_XY_up(self):
		self.assertEqual(MOVE_XY['up'](1,1), (0,1), "Should be (0,1)")
		self.assertEqual(MOVE_XY['up'](0,3), (-1,3), "Should be (-1,3)")
	
	def test_MOVE_XY_down(self):
		self.assertEqual(MOVE_XY['down'](1,1), (2,1), "Should be (2,1)")
		self.assertEqual(MOVE_XY['down'](3,0), (4,0), "Should be (4,0)")


class TestMOVE_INDEX(unittest.TestCase):
	
	def compare_MOVE_XY_to_MOVE_INDEX(self, direction, i, dim):
		x, y = index_1d_to_xy(i, dim)
		self.assertEqual(index_1d_to_xy(MOVE_INDEX[direction](i,dim), dim), MOVE_XY[direction](x,y))
		
	def test_15puzzle_MOVE_INDEX_left(self):
		dir = 'left'
		dim = dim_15puzzle
		for i in range(1,4):
			self.compare_MOVE_XY_to_MOVE_INDEX(dir, i, dim)
		for i in range(5,8):
			self.compare_MOVE_XY_to_MOVE_INDEX(dir, i, dim)
		for i in range(13,16):
			self.compare_MOVE_XY_to_MOVE_INDEX(dir, i, dim)
		for i in (0,4,8,12):
			self.assertIsNone(MOVE_INDEX[dir](i,dim))
		self.assertEqual(move_index_left(2, 4), 1, "Should be 1")
	
	def test_15puzzle_MOVE_INDEX_right(self):
		dir = 'right'
		dim = dim_15puzzle
		for i in range(0,3):
			self.compare_MOVE_XY_to_MOVE_INDEX(dir, i, dim)
		for i in range(4,7):
			self.compare_MOVE_XY_to_MOVE_INDEX(dir, i, dim)
		for i in range(8,11):
			self.compare_MOVE_XY_to_MOVE_INDEX(dir, i, dim)
		for i in (3,7,11,15):
			self.assertIsNone(MOVE_INDEX[dir](i,dim))
	
	def test_15puzzle_MOVE_INDEX_up(self):
		dir = 'up'
		dim = dim_15puzzle
		for i in range(4,16):
			self.compare_MOVE_XY_to_MOVE_INDEX(dir, i, dim)
		for i in range(0,4):
			self.assertIsNone(MOVE_INDEX[dir](i,dim))
	
	def test_15puzzle_MOVE_INDEX_down(self):
		dir = 'down'
		dim = dim_15puzzle
		for i in range(0,12):
			self.compare_MOVE_XY_to_MOVE_INDEX(dir, i, dim)
		for i in range(12,16):
			self.assertIsNone(MOVE_INDEX[dir](i,dim))

class TestUnitFunctions(unittest.TestCase):
	
	def test_generateTargetPatternAsBytes(self):
		ptiles = (0, 3, 7, 11, 12, 13, 14, 15)
		self.assertEqual(generateTargetPatternAsBytes(ptiles), b'\x00\x03\x07\x0b\x0c\r\x0e\x0f', "Should be b\'\x00\x03\x07\x0b\x0c\r\x0e\x0f\'") 
	
	def test_doAction(self):
		dim = dim_15puzzle
		state = bytes([0, 3, 7, 11, 12, 13, 14, 15])
		action = (6, 'up')
		state_depth = 0
		moveSetDict = MOVE_INDEX
		moveSetTuple = MOVE_INDEX_DIRECTIONS
		
		resultState, info = doAction(state, dim, action, state_depth, moveSetDict)
		self.assertEqual(resultState[action[0]], 10, "Should be 10")
		self.assertEqual(info[0], state_depth+1, "Should be 1")
		self.assertEqual(info[1], action[0], "Should be 6")
		self.assertEqual(moveSetTuple[info[2]], move_index_down, "Should be move_index_down")

# I WANT TO TEST ACTIONS UNDOING THEMSELVES
	
	def test_getActions(self):
		dim = dim_15puzzle
		moveSetDict = MOVE_INDEX
		moveSetTuple = MOVE_INDEX_DIRECTIONS
		dirs = DIRECTIONS
		ptiles = PATTERNS['15fringe']['pattern tiles']
		state, info = doAction(bytes([0, 3, 7, 11, 12, 13, 14, 15]), dim, (ptiles.index(3),'left'), 0, moveSetDict)
		
		returnedActions = getActions(state, info, dim, moveSetTuple)
		
		excludedAction = (ptiles.index(3), dirs.index('right')),	# This is the undo action that takes you back to parent state
		allowedActions = [
			(ptiles.index(0), dirs.index('right')),
			(ptiles.index(0), dirs.index('down')),
			(ptiles.index(3), dirs.index('left')),
			(ptiles.index(3), dirs.index('down')),
			(ptiles.index(7), dirs.index('up')),
			(ptiles.index(7), dirs.index('left')),
			(ptiles.index(11), dirs.index('left')),
			(ptiles.index(12), dirs.index('up')),
			(ptiles.index(13), dirs.index('up')),
			(ptiles.index(14), dirs.index('up')),
		]
		
		self.assertEqual(returnedActions, allowedActions)
	def test_getActions(self):
		dim = dim_15puzzle
		moveSetDict = MOVE_INDEX
		moveSetTuple = MOVE_INDEX_DIRECTIONS
		dirs = DIRECTIONS
		ptiles = PATTERNS['15fringe']['pattern tiles']
		state, info = doAction(bytes([0, 3, 7, 11, 12, 13, 14, 15]), dim, (ptiles.index(3),'left'), 0, moveSetDict)
		
		returnedActions = set(getActions(state, info, dim, moveSetTuple))
		
		excludedAction = (ptiles.index(3), dirs.index('right')),	# This is the undo action that takes you back to parent state
		allowedActions = {
			(ptiles.index(0), dirs.index('right')),
			(ptiles.index(0), dirs.index('down')),
			(ptiles.index(3), dirs.index('left')),
			(ptiles.index(3), dirs.index('down')),
			(ptiles.index(7), dirs.index('up')),
			(ptiles.index(7), dirs.index('left')),
			(ptiles.index(11), dirs.index('left')),
			(ptiles.index(12), dirs.index('up')),
			(ptiles.index(13), dirs.index('up')),
			(ptiles.index(14), dirs.index('up')),
		}
		
		self.assertEqual(returnedActions, allowedActions)

		
if __name__ == '__main__':
	unittest.main()