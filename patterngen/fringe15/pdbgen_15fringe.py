#!/usr/bin/env python3



#  I WANT THIS PDB GENERATOR TO BE GENERALIZEABLE BUT RIGHT NOW I JUST NEED TO GET THE 15-PUZZLE PDB WORKING !!!!
# SO I WILL SLAP IT TOGETHER FOR NOW

# AND WILL COMBINE LATER.... OTHERWISE THIS WILL BE A MESSSSSY PROJECT

##==============================================================================================##
import sys
from time import strftime

from patterngen.helpers.memorytools import *
from patterngen.helpers.timetools import *

from patterngen.pdbgen import logger
from patterngen.pdbgen import moves
from patterngen.pdbgen.parser import parseArgs
from patterngen.pdbgen import patterns
import fringe15generator


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
	info = patterns.PATTERN_INFO[pname]
	base_filename = f'{pname}_pdb_{RUN_ID}'
	base_filename_with_path = f'{OUTPUT_DIRECTORY}{base_filename}'
	
	log, logfile = logger.initLogger(base_filename_with_path)
	logger.printHeader(log, pname, RUN_ID, base_filename)
	
	t_start = pCounter()
	m_start = getMaxRSS()
	
	dbfile, tables, n_entries = generator.generatePatternDatabase(info, log, base_filename_with_path)
	
	logger.printStats(log, t_start, m_start, dbfile, tables, n_entries, title='Stats')
	log.debug(f'logfile: {logfile}')