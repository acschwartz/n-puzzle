#!/usr/bin/env python3
from time import perf_counter

PATTERN_DATABASE = None
PDB_TYPE = None
# PDB implemented as dictionary

def load_pdb(pdb):
	def printLoading():
		print ('Loading pattern database into memory ... ')
	def printLoaded():
		print('PDB', pdb, 'loaded from', filename)
	
	global PATTERN_DATABASE, PDB_TYPE
	if PATTERN_DATABASE:
		print("load_pdb: PDB already loaded. Will not re-load.")
		return
		
	filename = PDBINFO[pdb]['file']
	PDB_TYPE = pdb
	
	t_start = perf_counter()
	if '.json' in filename:
		from json import load
		with open(filename, 'r') as f:
			printLoading()
			PATTERN_DATABASE = load(f)
	
	if '.pickle' in filename:
		from pickle import load
		with open(filename, "rb") as f:
			printLoading()
			PATTERN_DATABASE = load(f)
			
	t_delta = perf_counter() - t_start
	return t_delta

def pdb_lookup(state, goal_state, size):
	# this could be implemented cleaner... doing these checks every single call ain't cute
	# TODO: maybe each pdb should have its own lookup function...
	
	if PDB_TYPE == 'max15fringeLC':
		from npuzzle.heuristics import linear_conflicts
		lc = linear_conflicts(state, goal_state, size)
		fringe = pdb_lookup_15fringe(state)
		return max(fringe, lc)
		
	
	if PDB_TYPE == '15fringe':
		return pdb_lookup_15fringe(state)
	
	if PDB_TYPE == '8puz':
		try:
			return PATTERN_DATABASE[state]
		except NameError:
			print('pdb.pdb_lookup: attempted lookup but pattern database not loaded')
			exit(1)


def pdb_lookup_15fringe(state):
#		ptiles = PDBINFO['15fringe']['pattern tiles']
#		empty_tile = PDBINFO['15fringe']['empty tiles']
		# TODO: the above should also be passed in as local vars for optimal performance...
		# global lookups are expensive
	
		# just gonna hardcode this in to save lookup time
		ptiles = (3, 7, 11, 12, 13, 14, 15)
		empty_tile = 0
		# I had the line below as pattern = [empty_tile] * 16 and I don't even think that works
		# since empty_tile is a var... idk looks into it
	
		# convert state to pattern
		pattern = [0] * 16
		for ptile in ptiles:
			pattern[ptile] = state.index(ptile)
			
		pattern = tuple(pattern)
		print('pdb_lookup: looking up pattern ', pattern)
		h = PATTERN_DATABASE[pattern]
		print('pdb_lookup: h =', h)
		return h

		# TODO: !!!! so I realized that I should have had the entries be lists in my pdb,
		# since the lookup keys are patterns and not keys, and patterns have to be built, therefore
		# are mutable. list <--> tuple conversion takes computation time


PDBINFO = {
	'8puz': {
			'file': 	'npuzzle/pdb/8puzzle/zerofirst_full_board.pickle',
			'size':		3,
			'goal_state': 'zero_first',
		},
	'15fringe': {
			'file': 	'npuzzle/pdb/15puzzle/4732363__15fringe_database.pickle',
			'size':		4,
			'goal_state': 'zero_first',
			'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
			'empty tile': 0,
		},
	'max15fringeLC':{
			'file': 	'npuzzle/pdb/15puzzle/4732363__15fringe_database.pickle',
			'size':		4,
			'goal_state': 'zero_first',
			'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
			'empty tile': 0,
		},
}
