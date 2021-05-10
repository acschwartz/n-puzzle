#!/usr/bin/env python3

import argparse
import main
from npuzzle.pdb import pdb
from npuzzle import colors
colors.enabled = True
from npuzzle.colors import color
from sys import exit

'''
SET UP EACH EXPERIMENT:
1. READING OF INPUT FILE (CONTAINING an initial state)
2. SPECIFY ARGS TO CALL
3. ITERATIVELY CALL main
4. RECORD RESULTS TO JSON FILE
5. name file meaninfully (w datetime?)
'''

if __name__ == '__main__':
#	args = ['--str', "(6, 3, 8, 7, 1, 2, 4, 0, 5)", '-f', 'manhattan']
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-pdb', help='pattern database as heuristic function', choices=list(pdb.PDBINFO.keys()))
	args = parser.parse_args()
	
	
	if args.pdb:
#		time_to_load_pdb = pdb.load_pdb(args.pdb)
#		print(color('yellow','time to load PDB:') + ' %.4f second(s)' % (time_to_load_pdb))
		
		# Connect to Database!
		PDB_CONNECTION = pdb.initDB(args.pdb)

	else:
		args.pdb = None
		print(color('red', '\nNo pdb selected.'))
		print(color('yellow', 'If you meant to select a PDB, your options are:'))
		print(color('yellow', str(tuple(pdb.PDBINFO.keys()))))
	
	while 1:
		if args.pdb:
			print ('\nRUN SOLVER WITH PDB: ', color('green', args.pdb))
		else:
			print ('\nRUN SOLVER WITH PDB: ', color('red', 'None'))
		print('Enter each arg on separate line (press Return in between)')
		print('   - to RUN: press Space, type run or ok, or Return twice.')
		print('   - to EXIT: type exit, or Return twice.')
		print('   - HELP: verbose: type -help or -h, concise: type help or h')
		print('')
		
		argsList = []
		if args.pdb:
			argsList.append(PDB_CONNECTION)
			print(color('yellow', str(argsList)))
		
		while 1:
			nextArg = input().strip()
			if nextArg in [' ', 'exit']:
				exit()
			if nextArg in ['', 'run', 'ok']:
				break
			if nextArg in ['--help', '-h', 'help', 'h']:
				try:
					main.main(nextArg)
				except:
					continue
			
			argsList.append(nextArg)
			
			if nextArg == '--str':
				print(color('red','NOTE:'), color('yellow', 'UNlike cli, do not contain string in quotes or escape any chars'))
				
			if nextArg == '--ints':
				nextArg = input()
				nextArg_list = nextArg.split()
				argsList.extend(nextArg_list)
		
		
		if len(argsList) > 0:
			if args.pdb:
				argsList.extend(['-f', ''.join(['pdb_', args.pdb])])
			print(argsList)
			try:
				print(f'\nwrapper.py: calling main with args: {argsList} \n')
				main.main(argsList)
			except:
				continue
		else:
			break
		
		