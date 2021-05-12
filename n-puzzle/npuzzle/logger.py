#!/usr/bin/env python3

import logging
from helpers.memorytools import *
from helpers.timetools import *
from sys import stdout, platform
SECTION_SEPARATOR = '=========================================================================='

def initLogger(logfile):

	# create logger
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)  
	
	output_file_handler = logging.FileHandler(logfile)
	output_file_handler.setLevel(logging.INFO)	# don't ever want debug stuff in the logfile
	logger.addHandler(output_file_handler)
	return logger



#def generateStats(t_start, maxrss_start, dbfile, tables, n_entries):
#	stats = dict()
#	stats['database file'] = dbfile
#	stats['entries collected'] = n_entries
#	stats['platform'] = platform
#	t_delta = pCounter() - t_start
#	m_delta = getMaxRSS() - maxrss_start
#	stats['time_raw'] = f'{t_delta:.2f}'
#	stats['memory_raw'] = m_delta
#	stats['time'] = prettyTime(t_delta)
#	stats['memory'] = prettyMemory(m_delta)
#	return stats






def printLogHeader(logger, run_id, input_file, result_file, pdim, algo, heur, timeout_sec, gstate):
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

	logger.info(SECTION_SEPARATOR)
	logger.info(f'Run ID: {run_id}')
	logger.info(f'Input file: {input_file}')
	logger.info(f'Result file: {result_file}')
	logger.info(f'{SECTION_SEPARATOR}\n')
	puzzlesize = f'{pdim**2-1}-puzzle'
	logger.info(f'Puzzle: {puzzlesize}')
	logger.info(f'\nSEARCH ALGORITHM: \t{algo}')
	logger.info(f'HEURISTIC: \t\t{heur}')
	logger.info(f'Timeout: \t\t{secondsToWhatever(timeout_sec)}')
	logger.info(f'\nGoal state: {gstate}')
	logger.info(f'{SECTION_SEPARATOR}\n')
	
	logger.info('''NOTE:
	For A*:
	  - space complexity = nodes generated
	  - time complexity = nodes generated
		
	For IDA*:
	  - space complexity = max path length
	  - time complexity: nodes generated''')
	logger.info(f'\n{SECTION_SEPARATOR}\n')




#def printStats(logger, t_start, maxrss_start, dbfile, tables, n_entries, title=None ):
#	stats = generateStats(t_start, maxrss_start, dbfile, tables, n_entries)
#	
#	stats_as_strings = sorted([ f'{key} : {stats[key]}' for key in stats ])
#	logger.info(f'\n{SECTION_SEPARATOR}')
#	if title:
#		logger.info(f'\t{title}')
#		logger.info(SECTION_SEPARATOR)
#	for stat in stats_as_strings:
#		logger.info(stat) 
#	logger.info(SECTION_SEPARATOR)
#	logger.info(f'Number tables: {len(tables)}')
#	logger.info(f'  Tables are separated by the location of the empty tile - it is imputed from the table number')
#	logger.info(f'  i.e. table0 hold all entries where the empty tile is at location 0 in the puzzle, etc...')
#	logger.info(f'\nTable names:')
#	for i, t in enumerate(tables):
#		logger.info(f'   {i}     {t}')
#	logger.info(SECTION_SEPARATOR)
#	return