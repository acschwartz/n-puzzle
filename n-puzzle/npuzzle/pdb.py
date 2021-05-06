#!/usr/bin/env python3
from time import perf_counter

PATTERN_DATABASE = None
# PDB implemented as dictionary

def load_pdb(pdb):
	global PATTERN_DATABASE
	if PATTERN_DATABASE:
		print("load_pdb: PDB already loaded. Will not re-load.")
		return
		
	filename = PDBINFO[pdb]['file']
	
	t_start = perf_counter()
	if '.json' in filename:
		from json import load
		with open(filename, 'r') as f:
			PATTERN_DATABASE = load(f)
	
	if '.pickle' in filename:
		from pickle import load
		with open(filename, "rb") as f:
			PATTERN_DATABASE = load(f)
			
	t_delta = perf_counter() - t_start
	return t_delta

def pdb_lookup(state, goal_state=None, size=None):
	try:
		return PATTERN_DATABASE[state]
	except NameError:
		print('pdb.pdb_lookup: attempted lookup but pattern database not loaded')
		exit(1)
#	return PDB_DICT[str(state)] if PDB_DICT else None


PDBINFO = {
	'8puz': {
			'file': 	'npuzzle/pdb/8puzzle/zerofirst_full_board.pickle',
			'size':		3,
			'goal_state': 'zero_first',
		}
}