#!/usr/bin/env python3
import argparse
import main
from npuzzle import pdb
from npuzzle import colors
colors.enabled = True
from npuzzle.colors import color

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
		time_to_load_pdb = pdb.load_pdb(args.pdb)
		print(color('yellow','time to load PDB:') + ' %.4f second(s)' % (time_to_load_pdb))
	
	while 1:
		print ('\nRUN SOLVER WITH PDB: ', color('red', args.pdb))
		print('Enter each arg on separate line (press Return in between)')
		print('Press Return twice to exit.')
		print('For verbose help, type -help or -h. For short help, type help or h')
		print('')
		
		argsList = []
		while 1:
			nextArg = input()
			if nextArg == '':
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
				argsList.append(nextArg)
		
		
		if len(argsList) > 0:
			if args.pdb:
				argsList.extend(['-pdb', args.pdb])
			print(argsList)
			
			try:
				main.main(argsList)
			except: pass
		else:
			break
		