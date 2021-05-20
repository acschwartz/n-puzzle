#!/usr/bin/env python3

import logging
from helpers.memorytools import *
from helpers.timetools import *
from sys import stdout, platform
SECTION_SEPARATOR = '=========================================================================='

def initLogger(logfile=None):
    if not logfile:
        logfile = f'pdbgen.log'
    else:
        logfile = ''.join([logfile, '.log'])

    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  
    
    # create handlers for logging to both file and stdout
    stdout_handler = logging.StreamHandler(stream=stdout)
    logger.addHandler(stdout_handler)
    
    output_file_handler = logging.FileHandler(logfile)
    output_file_handler.setLevel(logging.INFO)    # don't ever want debug stuff in the logfile
    logger.addHandler(output_file_handler)
    return logger, logfile


def generateStats(t_start, maxrss_start, dbfile, tables, n_entries):
    stats = dict()
    stats['database file'] = dbfile
    stats['entries collected'] = n_entries
    stats['platform'] = platform
    t_delta = pCounter() - t_start
    m_delta = getMaxRSS() - maxrss_start
    stats['time_raw'] = f'{t_delta:.2f}'
    stats['memory_raw'] = m_delta
    stats['time'] = prettyTime(t_delta)
    stats['memory'] = prettyMemory(m_delta)
    return stats


def printHeader(logger, pname, run_id, base_filename):
    logger.info(SECTION_SEPARATOR)
    logger.info(f'Run ID: {run_id}')
    logger.info(f'Database ID: {base_filename}')
    logger.info(f'Pattern type: {pname}')
    logger.info(f'{SECTION_SEPARATOR}\n')
    return


def printStats(logger, t_start, maxrss_start, dbfile, tables, n_entries, title=None ):
    stats = generateStats(t_start, maxrss_start, dbfile, tables, n_entries)
    
    stats_as_strings = sorted([ f'{key} : {stats[key]}' for key in stats ])
    logger.info(f'\n{SECTION_SEPARATOR}')
    if title:
        logger.info(f'\t{title}')
        logger.info(SECTION_SEPARATOR)
    for stat in stats_as_strings:
        logger.info(stat) 
    logger.info(SECTION_SEPARATOR)
    logger.info(f'Number tables: {len(tables)}')
    logger.info(f'  Tables are separated by the location of the empty tile - it is imputed from the table number')
    logger.info(f'  i.e. table0 hold all entries where the empty tile is at location 0 in the puzzle, etc...')
    logger.info(f'\nTable names:')
    for i, t in enumerate(tables):
        logger.info(f'   {i}     {t}')
    logger.info(SECTION_SEPARATOR)
    return