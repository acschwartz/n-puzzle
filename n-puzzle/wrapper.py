#!/usr/bin/env python3

import argparse
import sqlite3
import re
import os
import sys
import traceback
import inspect

from copy import copy
from math import ceil, floor
from time import strftime, perf_counter

from main import main as solver
from npuzzle.pdb import pdb
from npuzzle import colors
from npuzzle.colors import color
from npuzzle import logger


colors.enabled = True
RUN_ID = strftime(f'%b%d-%Y_%I-%M-%S%p')
OUTPUT_DIRECTORY = 'output/'




#====================# FORMATTING  #====================#
def centerOnLine(text, maxlinelength, constructString=True, paddingChar=' '):
# NOTE this is wonky if you already have the colors appended to the string,
# or if you use any whitespace chars other than spaces (\t, \n, etc)
# it messes up the count.
# therefore it also returns the numbers you need to construct the string yourself
	emptyspace = maxlinelength-len(text)
	leftpadding = int(floor(emptyspace/2))
	rightpadding = int(ceil(emptyspace/2))
	
	if constructString:
		return ''.join((paddingChar*leftpadding, text, paddingChar*rightpadding))
	else:
		return leftpadding, rightpadding


#	WRONG. lol
#def printProgressBar(completed, total, linelength, chComplete='+', colorComplete='green2', chIncomplete='-', colorIncomplete='white'):
#	percentComplete = completed / total
#	strComplete = chComplete * int(ceil(percentComplete*linelength))
#	strIncomplete = chIncomplete * int((1 - percentComplete)*linelength)
#	if len(strComplete)+len(strIncomplete) > linelength:
#		strIncomplete = strIncomplete[:-1]
#	bar_Complete = color(colorComplete, strComplete)
#	bar_Incomplete = color(colorIncomplete, strIncomplete)
#	print(''.join([bar_Complete, bar_Incomplete]))


MAX_LINE_LENGTH = 72
INDENT = ' ' * 6
SM_INDENT = ' ' * 2
SEPARATOR_DOTS = '.' * MAX_LINE_LENGTH
SEPARATOR_DASH = '-' * MAX_LINE_LENGTH
SEPARATOR_EQ = '=' * MAX_LINE_LENGTH
SEPARATOR_STAR = '*' * MAX_LINE_LENGTH
SEPARATOR_TILDE = '~' * MAX_LINE_LENGTH
MINI_SEP_DOTS = centerOnLine('. '*12, MAX_LINE_LENGTH)



	

def initDirectory(dir):
	if not os.path.exists(dir):
		os.mkdir(dir)
		print(f'\nDirectory created: {dir}')
	return

def stripFilename(fname):
	f = fname.split('/')
	f = f[-1]
	f = f.split('.')
	f = f[0]
	return f


def callSolver(args, silent=False):
	if not silent: 
		print()
		print(color('magenta2', centerOnLine(f' CALLING SOLVER ', MAX_LINE_LENGTH, paddingChar='.')))
		print()
	try:
		success, logheader = solver(args)
	except Exception as exc:
		printException(exc, lineno())
		return False, None
	except SystemExit as s:
		printException(s, lineno())
		return False, None
	return success, logheader

def lineno():
	"""Returns the current line number in the program."""
	return inspect.currentframe().f_back.f_lineno

def printException(exc, lineno):
	print()
	exc_name = type(exc).__name__
	title = f'exception caught by {os.path.basename(__file__)} line {lineno} '
	print(color('white', title))
	header = centerOnLine('  E X C E P T I O N  ', MAX_LINE_LENGTH, paddingChar='*')
	redSeparator = color('red2', centerOnLine(f'X', MAX_LINE_LENGTH, paddingChar='X'))

	print(f'{redSeparator}')
	print(color('red2', header))
	print(f'{redSeparator}')
	print(color('red', f' \n\N{NO ENTRY SIGN}  {exc_name} : '), color('red', str(exc)))
	print()
	print(color('white', traceback.format_exc()))
	print('\nStack:')
	traceback.print_stack()
	print(f'\n{redSeparator}')


def sec_to_hours(seconds):
# SOURCE: https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
	h=seconds//3600
	m=(seconds%3600)//60
	s=(seconds%3600)%60
	return f'{h} h {m} m {s:.2f} s'
secondsToHours = sec_to_hours

def secondsToWhatever(seconds):
	h=seconds//3600
	m=(seconds%3600)//60
	s=(seconds%3600)%60
	t_string = ''
	if h > 0:
		t_string = ''.join([t_string, f'{h} h'])
	if m > 0:
		t_string = ''.join([t_string, f' {m} m'])
	if s > 0:
		t_string = ''.join([t_string, f' {s:.2f} s'])
	t_string = t_string.strip()
	return t_string

'''
SET UP EACH EXPERIMENT:
1. READING OF INPUT FILE (CONTAINING an initial state)
2. SPECIFY ARGS TO CALL
3. ITERATIVELY CALL main
4. RECORD RESULTS TO JSON FILE
5. name file meaninfully (w datetime?)
'''

if __name__ == '__main__':
	
	def printArgs(listofargs):
#		argsEmojiSet = ['\N{SPEECH BALLOON}', '\N{ABACUS}']
		print(color('blue2', f'\n\N{WRAPPED PRESENT} ARGS:'), color('green', f'{[a for a in listofargs if not isinstance(a, sqlite3.Connection)]}'))
	
	def exitIfExit(inpt):
		inpt = inpt.strip()
		exit_substrings = ['q', 'exi', 'wxi', 'xit', 'eit', 'ecit', 'xig', 'evit', 'eci', 'xif', 'xot', 'ex']
		if any(s in inpt for s in exit_substrings):
			if PDB_CONNECTION:
				PDB_CONNECTION.close()
#				print('SQLite connection closed. Bye!')
			sys.exit(0)
	
	#---------------------------------------------#
	##### THIS TRY BLOCK ENCASES WHOLE PROGRAM ####
	# TODO: I wonder if I need the blocks within it then? :/
	try:
			
		wrapperParser = argparse.ArgumentParser()
		wrapperParser.add_argument('-pdb', help='pattern database as heuristic function', choices=list(pdb.PDBINFO.keys()))
		wrapperParser.add_argument('-b', '-batch', dest='batch', help='batch input from file', type=argparse.FileType('r'))
		wrapperArgs = wrapperParser.parse_args()
		PDB_CONNECTION = None
		

		#~~~~~~~~~~~~~~~~~~~~~ Program Header & Instructions ~~~~~~~~~~~~~~~~~~~~~
		
		print(f'\n{SEPARATOR_EQ}')
		print(color('red2', ' \N{WRAPPED PRESENT} wrapper:'), color('yellow', 'use to call n-puzzle'), color('yellow2', 'solver'), color('yellow', 'on batches of inputs'))
		print(f'{SEPARATOR_EQ}')
		INDENT = ' ' * 6
		print(f' \u21a9 TO', color('red2', 'EXIT')+':', 'type', color('white2', 'exit'), 'or', color('white2', 'q'))
		print(SEPARATOR_DASH)
#		print(color('white2', '\N{DOOR} TO'), color('red2', 'EXIT:'),  'type', color('white2', 'exit'))
		print('- help with', color('white2', 'wrapper'), f'args:\n  (command line)')
		print(f'{INDENT}wrapper.py -h  [or --help]')
		print('- help with', color('white2', 'solver'), f'args:\n  (inside wrapper)')
		print(f'{INDENT}concise:  type h  [or help]')
		print(f'{INDENT}verbose:  type -h  [or --help]')
		print(f'{SEPARATOR_DASH}')
		
		
		
		##~~~~~~~~~~~~~~~~~~~ Display & Initialize WRAPPER Settings ~~~~~~~~~~~~~~~~~~~~~~
		redNone = color('red', 'none')
		
		print(color('white', f'Wrapper instance {RUN_ID}'))
#		'SETTINGS \N{HAMMER AND WRENCH}'
		print()
#		print(f'{MINI_SEP_DOTS}')
#		print(color('yellow2', centerOnLine('\N{WRAPPED PRESENT}  YOUR WRAP:  \N{WRAPPED PRESENT}   ', MAX_LINE_LENGTH)))
		# TODO: word- SETTINGS? PARAMETERS??? CONFIGURATIONS?
#		print(color('yellow', centerOnLine(f'{RUN_ID}', MAX_LINE_LENGTH)))
#		print(color('white', centerOnLine('(persist until exit) ', MAX_LINE_LENGTH)))
		
		##~~~~~~~~~~~~~~~~ Initialize PDB & Display Choice ~~~~~~~~~~~~~~~~~~~~~~

		if wrapperArgs.pdb:
			# Connect to Database!
			PDB_CONNECTION = pdb.initDB(wrapperArgs.pdb)
			displaypdb = color('green2', wrapperArgs.pdb)
			
			
		else:
			wrapperArgs.pdb = None
			displaypdb = redNone
#			print(color('red2', '\nNo pdb selected.')) #, ' (optional)')
#			print(color('yellow', 'If you meant to select a PDB, restart the program and use flag -pdb \nfrom the command line.'))
#			print(color('yellow', ''.join(('PDB options: ', str(tuple(pdb.PDBINFO.keys()))))))
		
#		print(color('yellow2', 'Configuration:'))
		
		
		print(color('white', f'\nBindings '))
	
		#~~~~~~~~~~~~~~~~~~~~~~~~~~ Show DB Connection ~~~~~~~~~~~~~~~~~~~~~~~~~~
#		if PDB_CONNECTION:
#			print('initialized', color('white', str(PDB_CONNECTION)), ' \u2714', '\u2714')
		
#		print(f'\n{MINI_SEP_DOTS}')
		
		
#		print()
#		print(centerOnLine('.  .  .  .', MAX_LINE_LENGTH-1))
#		print()
#		print(color('white2', 'SETUP:'))
		
#		print(color('blue2', f'\n\N{WRAPPED PRESENT} PDB: '), displaypdb)
		if wrapperArgs.pdb:
			print(color('blue2', f'\n\N{WRAPPED PRESENT} PDB: '), displaypdb)
		else:
			print(color('blue2', f'\n* PDB: '), displaypdb)
			
		
		
		##~~~~~~~~~~~~~~~~~~ Initialize INPUT File & Display Choice ~~~~~~~~~~~~~~~~~~~~~~
		if wrapperArgs.batch:
			f = wrapperArgs.batch	# is already opened for you by parser!
			input_filename = f.name
			batchlines = [line.strip() for line in f]
			f.close()
			
			print(color('blue2', f'\N{WRAPPED PRESENT} Input: '), color('green2', f'{input_filename} '), f'({len(batchlines)} lines)')
			outputToFile = True
			
			
		else:
			print(color('blue2', f'\n* Input: '), 'manual')
			outputToFile = False  # TODO: for now!
#			print(color('red2', '\nNo input file selected.')) #, ' (optional)')
#			print(color('yellow', 'To use a file for batch input of puzzles, restart the program \nand use flag -b from the command line.'))
	
		
		##~~~~~~~~~~~~~~~~~~ Initialize OUTPUT File & Display Choice ~~~~~~~~~~~~~~~~~~~~~~
		if outputToFile:
			initDirectory(OUTPUT_DIRECTORY)
			output_filename = f'{OUTPUT_DIRECTORY}{stripFilename(input_filename)}__{RUN_ID}.json'
			print(color('blue2', f'\N{WRAPPED PRESENT} Output: '), f'{output_filename}')
			
			logfile = f'{OUTPUT_DIRECTORY}{stripFilename(input_filename)}__{RUN_ID}.log'
			log = logger.initLogger(logfile)
			print(color('blue2', f'\N{MEMO} Log: '), f'{logfile}')	# or \N{SPIRAL NOTE PAD}
		else:
			print(color('blue2', f'\n* Output:'), 'stdout')
			print(color('blue2', f'\n* Log:'), color('red', 'none'))
			logfile = None
			log = None
		
		
		
		
		
		
		##=====================  FRESH INPUT FOR SOLVER  ===========================
		while 1:
			ARGSLIST = []
#			print(f'\n{SEPARATOR_DOTS}')
			
#			print(f'{SEPARATOR_EQ}')
#			print('\n')
			
#			solverEmojiSet = [ '\N{ROBOT FACE}', '\N{BRAIN}',  '\N{RAT}',  '\N{ABACUS}',  u"\U0001F50D", u"\U0001F50E" ,'\N{DIRECT HIT}', '\N{JIGSAW PUZZLE PIECE}']
#			for emoji in solverEmojiSet:
#				print(color('yellow2', centerOnLine(f'{emoji} ENTER ARGUMENTS FOR SOLVER {emoji} \n', MAX_LINE_LENGTH)))
			
#			solverEmoji = u"\U0001F50D"
#			print(color('yellow2', centerOnLine(f'{solverEmoji} N-PUZZLE SOLVER {solverEmoji} \n', MAX_LINE_LENGTH)))
			
			
#			if wrapperArgs.pdb:
#				print (color('cyan2', 'SOLVER USING PDB: '), color('green', wrapperArgs.pdb))
#			else:
#				print (color('cyan2', 'SOLVER USING PDB: '), color('red2', 'None'))
#			print(SEPARATOR_DASH)
			print(color('white', f'\nBuild argument list:'))

	
			if wrapperArgs.pdb:
				ARGSLIST.append(PDB_CONNECTION)
				ARGSLIST.extend(['-f', ''.join(['pdb_', wrapperArgs.pdb])])
			
			
			wroteLogHeaderInfo = False
			
			while 1:
				printArgs(ARGSLIST)
				nextArg = input()
				exitIfExit(nextArg)
				
				if not nextArg:
					print(SEPARATOR_DASH)
					print(' - RUN: press SPACE, double-tap Enter, or type run or ok')
					print(' - DELETE: type del x to remove the last x arguments entered (default 1)')
					print(SEPARATOR_DASH)
					nextArg = input()
					if not nextArg:
						break # stop taking input
					
				nextArg = nextArg.strip()
					
				if 'del' in nextArg:
					res = re.search(r'\d+', nextArg)
					if res is None:
						n = 1
					else:
						n = int(res.group())
					if wrapperArgs.pdb:
						for i in range(n):
							if len(ARGSLIST) > 3:
								ARGSLIST.pop()
							else: 
								print(color('magenta', 'To change PDB choice, exit program.'))
								break
					else:
						for i in range(n):
							if ARGSLIST:
								ARGSLIST.pop()
					continue
				
				if nextArg in ['', 'run', 'ok']:
					break # stop taking input 
				
				if nextArg in ['help', 'h']:	# concise help
					try:
						solver(' ')
						continue
					except:
						continue
				if nextArg in ['--help', '-h']:  # verbose help
					solver([nextArg])
					continue
				
				if len(nextArg.split(' ')) > 1:
					listofnextArgs = nextArg.split(' ')
					listofnextArgs.reverse()
					print(color('white2', '\nadding...'))
					while listofnextArgs:
						a = listofnextArgs.pop()
						if a in ['-t', 't']:
							nextArg = '-t'
							break
						if a in ['--str', '-str']:
							nextArg = '--str'
							print(f' {a}')
							break
						else:
							print(f' {a}')
							ARGSLIST.append(a)
					if not listofnextArgs:
						continue
				
				if nextArg in ['-t', 't']:
					print(color('red','Err:'), f'{nextArg} not accepted.')
					print(color('white', 'Specify seconds (-ts, -tsec) or minutes (-tm, -tmin)'))
					continue
				
				elif nextArg in ['--str', '-str']:
					ARGSLIST.append(nextArg)
					print(color('yellow', f'Enter the string for arg {nextArg} on its own line:'))
					stringAccepted = False
					while not stringAccepted:
						nextArg = input()
						
						exitIfExit(nextArg)
						nextArg = nextArg.strip()
						if not nextArg:
							break
						if ',' not in nextArg:
							print(color('red','Err:'), 'numbers must be separated by commas')
						if any(ch in ['\\', '\'', '\"'] for ch in nextArg):
							print(color('red','Err:'), 'unlike cli, do NOT contain string in quotes or escape any chars')
						else:
							stringAccepted = True
							ARGSLIST.append(nextArg)
					
				elif nextArg in ['--ints', '-ints']:
					ARGSLIST.append(nextArg)
					print(color('yellow', 'Enter numbers separated by spaces (no other characters)'))
					nextArg = input()
					if 'exi' in nextArg:
						sys.exit(0)
					nextArg_list = nextArg.split()
					ARGSLIST.extend(nextArg_list)
				
				else:
					ARGSLIST.append(nextArg)
			
			
			if (wrapperArgs.pdb and len(ARGSLIST) > 3) or (not wrapperArgs.pdb and len(ARGSLIST) > 0) or (wrapperArgs.batch):
				if wrapperArgs.batch:
					def printRunHeader():
#						print(f'\n\n{SEPARATOR_TILDE}')
#						print(color('magenta', f'\n\n{SEPARATOR_STAR}'))
						print(color('magenta', f'{SEPARATOR_DOTS}'))
						print()
						txt = [''.join((' '*2, "\N{RUNNER} \N{RUNNER} \N{RUNNER}  RUNNING SOLVER:     ")), f' {n_processed+1} / {num_lines} ', f'\u23f3 {secondsToWhatever(perf_counter()-t_start)} ']
						label = ''.join((color('magenta2', txt[0]), color('cyan2', txt[1])))
						blankspace = ' ' * (len(SEPARATOR_DOTS)-5-len(''.join(txt)))
						timeElapsed = color('blue', txt[2])
						
						print(''.join((label, blankspace, timeElapsed)))
						print(color('magenta', f'\n{SEPARATOR_DOTS}'))
#						print(color('magenta', f'{SEPARATOR_STAR}'))
#						print(SEPARATOR_TILDE)
						
						
						print(color('blue2', f'\nINPUT:'), f'{input_filename}')
						print(color('blue2', f'\nOUTPUT:'), f'{output_filename}')
						print(color('blue2', f'\n\N{MEMO} LOG: '), f'{logfile}')	# or \N{SPIRAL NOTE PAD}
						
#						print(f'\n{SEPARATOR_DASH}')
						printArgs(argsThisRun)
						print(f'\n{SEPARATOR_DOTS}\n')
						
					
					def printFooter():
#						print('\N{CHEQUERED FLAG}')
						print(f'\n\n finished  in  {secondsToWhatever(perf_counter()-t_start)}')
						print(f'{SEPARATOR_DOTS}\n')
						
						if n_fail:
							print(" \u274C", color('red2', f'{n_fail}'), color('white', 'of'), color('red2', f'{num_lines}'), color('white', 'inputs'), color('red2','failed'), color('white', '(had errors)'))
							if n_success:
								print("  \u2714", color('green2', f'{n_success}'), color('white', 'of'), color('green2', f'{num_lines}'), color('white','inputs processed successfully'))
							
						else: # success only
							print(" \u2705", color('green2', f'{n_success}'), color('white', 'of'), color('green2', f'{num_lines}'), color('white','inputs processed successfully'))
											
	#					print(f'\n time elapsed: {secondsToWhatever(perf_counter()-t_start)}')
						print(color('blue2', '\n\n OUTPUT (RESULT) FILE: '), color('white2', f'{output_filename} '))
						print(color('blue2', f'\N{MEMO} LOGFILE: '), f'{logfile}')	# or \N{SPIRAL NOTE PAD}
						
						print(f'{SEPARATOR_DOTS}')
					
					try:
						num_lines = len(batchlines)
						n_processed = 0
						n_success = 0
						n_fail = 0
						t_start = perf_counter()
						for line in batchlines:
							argsThisRun = ARGSLIST.copy()
							argsThisRun.append('-ints')
							puzzle = line.split()
							argsThisRun.extend(puzzle)
							printRunHeader()
							print(f'DEBUG: calling solver from {lineno()}')
							success, logheader = callSolver(argsThisRun, silent=True)
							if log and not wroteLogHeaderInfo:
								logger.printLogHeader(log, RUN_ID, input_filename, output_filename, logheader['psize'], logheader['algo'], logheader['heur'], logheader['timeout_s'], logheader['goal'])
								wroteLogHeaderInfo = True
								
							n_processed += 1
							if success is True: # doesn't handle unsolvable puzzles lol
								n_success += 1
							else:
								n_fail += 1
							print('\n')
						
						printFooter()
						break
					except Exception as exc:
						printException(exc, lineno())
#						printFooter()
						continue
					except SystemExit as sysex:
						printException(sysex, lineno())
					
				else:
					try:
						print(f'DEBUG: calling solver from {lineno()}')
						success, logheader = callSolver(ARGSLIST)
						if log and not wroteLogHeaderInfo:
							log.printLogHeader(log, RUN_ID, input_filename, output_filename, logheader['psize'], logheader['algo'], logheader['heur'], logheader['timeout_s'], logheader['goal'])
							wroteLogHeaderInfo = True
						continue
					except Exception as exc:
						printException(exc, lineno())
						continue
					except SystemExit as sysex:
						printException(sysex, lineno())
					
			else:
				print(f'DEBUG: breaking from line {lineno()}')
				break
			
		
		if wrapperArgs.pdb:
			PDB_CONNECTION.close()
	#		print(color('white', 'SQLite connection closed. Bye!'))
		else:
			print()
	
	
	##### THIS TRY BLOCK ENCASES WHOLE PROGRAM #####
	except Exception as exc:
		printException(exc, lineno())