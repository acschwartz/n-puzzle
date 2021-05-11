#!/usr/bin/env python3

import argparse
from main import main
from npuzzle.pdb import pdb
from npuzzle import colors
colors.enabled = True
from npuzzle.colors import color
import sys
import traceback
from os import path, mkdir
from copy import copy

from time import strftime
RUN_ID = strftime(f'%b%d-%Y-%I:%M:%S%p')
OUTPUT_DIRECTORY = 'output/'

def initDirectory(dir):
	if not path.exists(dir):
		mkdir(dir)
		print(f'\nDirectory created: {dir}')
	return

def stripFilename(fname):
	f = fname.split('/')
	f = f[-1]
	f = f.split('.')
	f = f[0]
	return f

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
	parser.add_argument('-b', '-batch', dest='batch', help='batch input from file', type=argparse.FileType('r'))
	args = parser.parse_args()
	
	PDB_CONNECTION = None
	
	if args.pdb:
		# Connect to Database!
		PDB_CONNECTION = pdb.initDB(args.pdb)

	else:
		args.pdb = None
		print(color('red2', '\nNo pdb selected.'))
		print(color('yellow', 'If you meant to select a PDB, your options are:'))
		print(color('yellow', str(tuple(pdb.PDBINFO.keys()))))
	
	if args.batch:
		f = args.batch	# is already opened for you by parser!
#		print(f)
		input_filename = f.name
		batchlines = [line.strip() for line in f]
		print(color('blue2', '\nBatch input from file: '), f'{input_filename}  ({len(batchlines)} lines)')
		initDirectory(OUTPUT_DIRECTORY)
		output_filename = f'{OUTPUT_DIRECTORY}{RUN_ID}_{stripFilename(input_filename)}.json'  # TODO: extension? .json?
		print(color('blue2', '\nOutput file: '), f'{output_filename}')


	
	while 1:
		print('\n.......................................................................')
		if args.pdb:
			print (color('cyan2', 'RUN SOLVER WITH PDB: '), color('green', args.pdb))
		else:
			print (color('cyan2', 'RUN SOLVER WITH PDB: '), color('red2', 'None'))
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
				if args.pdb:
					PDB_CONNECTION.close()
					print('\nSQLite connection closed. Bye!')
				sys.exit(0)
			if nextArg in ['', 'run', 'ok']:
				break
			if nextArg in ['--help', '-h', 'help', 'h']:
				try:
					main(nextArg)
				except:
					continue
			
			argsList.append(nextArg)
			
			if nextArg in ['--str', '-str']:
				print(color('red','NOTE:'), color('yellow', 'UNlike cli, do not contain string in quotes or escape any chars'))
				
			if nextArg in ['--ints', '-ints']:
				print(color('red','NOTE:'), color('yellow', 'enter all on one line, separated by spaces'))
				nextArg = input()
				nextArg_list = nextArg.split()
				argsList.extend(nextArg_list)
		
		
		if len(argsList) > 0:
			if args.pdb:
				argsList.extend(['-f', ''.join(['pdb_', args.pdb])])
			if batchlines:
				try:
					num_lines = len(batchlines)
					i=1
					for line in batchlines:
						argsThisRun = argsList.copy()
						argsThisRun.append('-ints')
						puzzle = line.split()
						argsThisRun.extend(puzzle)
						print(color('yellow2', f'\nRunning...  {i} / {num_lines} .....'))

						main(argsThisRun)
						i+=1
						
				except Exception as e:
					print(color('red', 'error:'), e)
					print(traceback.format_exc())
					print(f'args: {argsThisRun}')
					continue
				else:
					try:
						print(f'\nwrapper.py: calling main with args: {argsList} \n')
						main(argsList)
					except Exception as e:
						print(color('red', 'error:'), e)
						print(traceback.format_exc())
						print(f'args: {argsList}')
						continue
				
		else:
			break
		
	if args.pdb:
		PDB_CONNECTION.close()
		print('SQLite connection closed. Bye!')
		