#!/usr/bin/env python3

def load_pdb(pdb):
	global PDB_DICT
	if PDB_DICT:
		print("load_pdb: PDB already loaded. Will not re-load.")
		return
		
	filename = PDBINFO[pdb]['file']
	
	if '.json' in filename:
		import json
		with open(filename, 'r') as f:
			PDB_DICT = json.load(f)
	
	if '.pickle' in filename:
		import pickle
		with open(filename, "rb") as f:
			PDB_DICT = pickle.load(f)

def pdb_lookup(state, goal_state=None, size=None):
	try:
		return PDB_DICT[state]
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

PDB_DICT = None