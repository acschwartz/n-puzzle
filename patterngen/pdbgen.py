#!/usr/bin/env python3
##==============================================================================================##
import sys
from time import strftime

from helpers.memorytools import *
from helpers.timetools import *

from pdbgen import generator
from pdbgen import logger
from pdbgen import moves
from pdbgen.parser import parseArgs
from pdbgen import patterns

#mmaybe remove later
from pprint import pp as pp


RUN_ID = strftime(f'%y%m%d-%H%M%S')
OUTPUT_DIRECTORY = 'output/'

##==============================================================================================##
def handle_exception(exc_type, exc_value, exc_traceback):
# Source: https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
	if issubclass(exc_type, KeyboardInterrupt):
		sys.__excepthook__(exc_type, exc_value, exc_traceback)
		return
	
	log.critical("\nUncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
	log.info('\n')
	
sys.excepthook = handle_exception
##==============================================================================================##


##==============================================================================================##
#		M A I N
##==============================================================================================##
if __name__ == '__main__':
	pname = parseArgs()
	print(f'pname: {pname}')
	print(f'RUN_ID: {RUN_ID}')
	
	log, logfile = logger.initLogger()
	
	info = patterns.PATTERN_INFO[pname]
	
#	print(encode(ptiles))
#	print(decode(encode(ptiles)))
	
	generator.generatePatternDatabase(info, log)
	