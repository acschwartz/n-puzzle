#!/usr/bin/env python3
import json

PDB_DICT = None

def load_pdb(filename):
	with open(filename, 'r') as JSON:
		global PDB_DICT
		PDB_DICT = json.load(JSON)

def pdb_lookup(state):
#	try:
#		return PDB_DICT[str(state)]
#	except NameError:
#		return None
	return PDB_DICT[str(state)] if PDB_DICT else None