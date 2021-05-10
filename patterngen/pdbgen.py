#!/usr/bin/env python3
##==============================================================================================##
import logging	#probably put into separate module
from time import strftime

from helpers.memorytools import *
from helpers.timetools import *

from pdbgen import moves
from pdbgen.parser import parseArgs
from pdbgen import patterns

#mmaybe remove later
from pprint import pp as pp


RUN_ID = strftime(f'%y%m%d-%H%M%S')
OUTPUT_DIRECTORY = 'output/'


##==============================================================================================##
#		M A I N
##==============================================================================================##
if __name__ == '__main__':
	pname = parseArgs()
	print(f'pname: {pname}')
	print(f'RUN_ID: {RUN_ID}')
	