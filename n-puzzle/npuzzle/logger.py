#!/usr/bin/env python3

import logging
from platform_info import *
from sys import stdout, platform
from npuzzle.platform_info import getSystemInfo
import json

SECTION_SEPARATOR = '=========================================================================='

def initLogger(logfile):

    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  
    
    output_file_handler = logging.FileHandler(logfile)
    output_file_handler.setLevel(logging.INFO)    # don't ever want debug stuff in the logfile
    logger.addHandler(output_file_handler)
    return logger



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
    if timeout_sec is not None:
        logger.info(f'Timeout: \t\t{secondsToWhatever(timeout_sec)}')
    else:
        logger.info(f'Timeout: \t\t{str(timeout_sec)}')
    logger.info(f'\nGoal state: {gstate}')
    logger.info(f'{SECTION_SEPARATOR}\n')
    logger.info(f' \nSYSTEM:')
    logger.info(getSystemInfo())
    logger.info(f'{SECTION_SEPARATOR}\n')
    
    logger.info('''note:
    for A*:
      - space complexity = nodes generated
      - time complexity = nodes generated
        
    for IDA*:
      - space complexity = max path length
      - time complexity: nodes generated''')
    logger.info(f'\n{SECTION_SEPARATOR}\n')
