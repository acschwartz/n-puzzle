#!/usr/bin/env python3

import logging
from sys import stdout

def initLogger(logfile=None, output_path=None):
	
	# TODO: deal with all this logfile path stuff later...
	
	if not logfile:
		logfile = f'pdbgen.log'

	# create logger
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)  
	
	# create handlers for logging to both file and stdout
	stdout_handler = logging.StreamHandler(stream=stdout)
	logger.addHandler(stdout_handler)
	
	output_file_handler = logging.FileHandler(logfile)
	output_file_handler.setLevel(logging.INFO)	# don't ever want debug stuff in the logfile
	logger.addHandler(output_file_handler)
	
	return logger, logfile

