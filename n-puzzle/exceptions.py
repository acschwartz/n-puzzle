#!/usr/bin/env python3

import inspect
import traceback

from wrapper import MAX_LINE_LENGTH
# P.S. / TODO: all these lovely formatting and tool functions like (prettyTime, prettyMemory), shoud be stored
# nicely on their own and then imported into every file in the project.
# e.g. have a file for formatting variables like the separators i've made for wrapper (where I split this code from
# because surprise... I needed my exception "handler" across the project lol


def lineno():
	"""Returns the current line number in the program."""
	return inspect.currentframe().f_back.f_lineno


def printException(exc, lineno):
	print()
	exc_name = type(exc).__name__
	title = f'exception caught by {os.path.basename(__file__)} line {lineno} '
	print(color('white', title))
	header = centerOnLine(f' \N{WARNING SIGN}  E X C E P T I O N  \N{WARNING SIGN}  ', MAX_LINE_LENGTH, paddingChar='*')
	redSeparator = color('red2', centerOnLine(f'X', MAX_LINE_LENGTH, paddingChar='X'))
	
	ExceptionEmojis = [ '\N{NO ENTRY SIGN}', '\U0001f92c', '\N{EXCLAMATION QUESTION MARK}',
		'\N{SOS}',  '\N{FIRE}' ,  '\N{FIRE EXTINGUISHER}' , '\N{COLLISION SYMBOL}', u"\U0001F921" # CLOWN FACE LOL
	]
	
	print(f'{redSeparator}')
	print(color('red2', header))
	print(f'{redSeparator}')
	print(color('red', f' \n\N{EXCLAMATION QUESTION MARK}  {exc_name} : '), color('red', str(exc)), '\U0001f92c')
	print()
	print(color('white', traceback.format_exc()))
	print('\nStack:')
	traceback.print_stack()
	print(f'\n{redSeparator}')