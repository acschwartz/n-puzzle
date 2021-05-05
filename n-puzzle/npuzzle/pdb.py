#!/usr/bin/env python3
import json
#import npuzzle.goal_states

def load_pdb(pdb):
	filename = PDBINFO[pdb]['file']
	with open(filename, 'r') as JSON:
		global PDB_DICT
		PDB_DICT = json.load(JSON)

def pdb_lookup(state, goal_state=None, size=None):
	try:
		return PDB_DICT[str(state)]
	except NameError:
		print('pdb.pdb_lookup: attempted lookup but pattern database not loaded')
		exit(1)
#	return PDB_DICT[str(state)] if PDB_DICT else None


PDBINFO = {
	'8puz': {
			'file': 	'npuzzle/pdb/8puzzle/zerofirst_full_board.json',
			'size':		3,
			'goal_state': 'zero_first',
		}
}