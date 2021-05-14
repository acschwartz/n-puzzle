#!/usr/bin/env python3

import argparse
import sqlite3
import re
import os
import sys
import json
#import textwrap
# TODO: https://programmer.help/blogs/python-3-standard-library-textwarp-text-wrapping-and-filling.html

from copy import copy
from math import ceil, floor
from time import strftime, perf_counter

from formatting import colors
from formatting.colors import color
from formatting.exceptions import *
from formatting import stringtools as st
from formatting.txt_elements import *

from npuzzle.pdb import pdb
from npuzzle import logger
from npuzzle import platform_info

from solver import solver


colors.enabled = True
global RUN_ID
RUN_ID = strftime(f'%b%d-%Y_%I-%M-%S%p')
OUTPUT_DIRECTORY = 'output/'



def initDirectory(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
        print(f'\nDirectory created: {dir}')
    return

def printAndOrLog(line, log=None, doNotPrint=False):
    if log:
        log.info(line)
    if not doNotPrint:
        print(line)

def callSolver(args, silent=False):
    announcement = ''.join(
        ['\n', 
          st.center_by_padding( 
                f' CALLING SOLVER ', 
                MAX_LINE_LENGTH, 
                padding_char='.'), 
         '\n']
    )   
    
    if not silent: 
        print(color('magenta2', announcement))
    
    try:
#        print( color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'\
#                    'calling solver ...')
#        )
        outcome = solver(args)
        
#        print(color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'\
#                    f'solver returned: {outcome}')
#        )
        
        if outcome:
            return outcome
        
        else:
            # ??????????????
            # it this gonna throw an exception
            pass
            
    except SystemExit as ext:
#        print(color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'\
#                    'caught SystemExit as ext...')
#        )
#        print(color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'\
#                    'calling printException ...')
#        )
        printException(ext, lineno())
        
#        print(color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'
#                    'calling close_DB_and_exit...')
#        )
        close_DB_and_exit()
        
    except Exception as exc:
#        print(color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'\
#                    'caught Exception as exc')
#        )
#        print(color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'\
#                    'calling printException...')
#        )
        printException(exc, lineno())
        
        
#        print(color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'\
#                    'No cleanup call.')
#        )
#        print(color('yellow',
#                    f'DEBUG: wrapper | callSolver| line {lineno()} |'\
#                    'Did not execute explicit return statement. '\
#                    'What happens next?'))
#        return #None, None, None 
#        # this will throw exeption that I can't unpack an iterable
#        # with value None........ hmmmmmm ......



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
    try:    
        def printArgs(listofargs, prefix='', areWrapped=False):
            def hideDB(lst):
                return [a for a in listofargs 
                        if not isinstance(a, sqlite3.Connection)]
    
            args_deco = '\N{WRAPPED PRESENT}' if areWrapped else '\N{PACKAGE}'
            args_filtered = [a for a in listofargs if not isinstance(a, sqlite3.Connection)]
            
            if not areWrapped:
                print( #color('blue2', f'\n {args_deco} ARGS:'), 
                        f' {args_deco} ',
                        color('green2', f'{args_filtered}'))
            else:
                print(
                    color('white2', f'\n  {args_deco}  args:\t'),
                    color('yellow2', ' '.join(args_filtered))
                )
                
        
        def exit_if_exit(user_input_string):
    #        print(color('yellow', 'DEBUG: hello from exit_if_exit'))
            
            inpt = user_input_string.strip()
            exit_substrings = ['exit', 'q', 'exi', 'wxi', 'xit', 'eit',
                        'ecit', 'xig', 'evit', 'eci', 'xif', 'xot', 'ex']
            if any(s in inpt for s in exit_substrings):
                close_DB_and_exit(1)
        
        def close_DB_and_exit(exitcode=0):
            if PDB_CONNECTION:
                PDB_CONNECTION.close()
                deco = '\N{Link Symbol}\u200d\N{Cross mark}'
                print(f'{deco} SQLite connection closed. Bye!')
            sys.exit(exitcode)
        
        #---------------------------------------------#
        ##### THIS TRY BLOCK ENCASES WHOLE PROGRAM ####
        # TODO: I wonder if I need the blocks within it then? :/
        
        try:
                
            wrapperParser = argparse.ArgumentParser()
            wrapperParser.add_argument(
                '-pdb', 
                help='pattern database as heuristic function', 
                choices=list(pdb.PDBINFO.keys()))
            wrapperParser.add_argument(
                '-b',
                '-batch',
                dest='batch', 
                help='batch input from file', 
                type=argparse.FileType('r'))
            wrapperParser.add_argument(
                '-o',
                help='specify output filename')
            wrapperArgs = wrapperParser.parse_args()
            PDB_CONNECTION = None
            
    
            #~~~~~~~~~~~~~~~~ Program Header & Instructions ~~~~~~~~~~~~~~~~
#            print('\n\n')
#            print(f'{SEPARATOR_EQ}\n')
#            print(
#                color('red2',     ' \N{WRAPPED PRESENT}  wrapper:'), 
#                color('yellow',   ' call n-puzzle'), 
#                color('yellow2',  'solver'), 
#                color('yellow',   'on batches of inputs'))
#            print(f'\n{SEPARATOR_EQ}')
            
            #~~~~~~~~~~~~~~~~ Program Header & Instructions ~~~~~~~~~~~~~~~~
            print('\n')
            print(f'{SEPARATOR_EQ}')
            print(
                color('white2',     ' wrapper.py:'), 
                'batch-processing for the n-puzzle solver',
            )
            print(f'{SEPARATOR_EQ}\n')
            
            
#            TODO: fix (muuuuuch) later
#            print(color('white',   '- to exit, type'), 
#                    color('white2',  'exit'), 
#                    color('white',   'or'), 
#                    color('white2',  'q'))
#                
#            print(color('white',   '- help with'), 
#                    color('white2',  'wrapper'), 
#                    color('white',   'args:\n  (command line)'),
#                    color('white',  f'{INDENT}wrapper.py -h  [or --help]'))
#            
#            print(color('white',  '- help with'), 
#                    color('white2', 'solver'),
#                    color('white',  'args:\n  (inside wrapper)'),
#                    color('white', f'{INDENT}concise:  type h  [or help]'),
#                    color('white',  '{INDENT}verbose:  type -h  [or --help]'))
#            
#            print(f'{SEPARATOR_DASH}\n\n')
            
            
            ##~~~~~~ Display & Initialize Wrapper Choices from CLI ~~~~~~~~
            redNone = color('red', 'none')
            if wrapperArgs.o:
                RUN_ID = ''.join([wrapperArgs.o, '___', RUN_ID])
            print(
                    color('red',
                            f' \N{WRAPPED PRESENT}  wrapper id: '),
                    color( 'yellow2', 
                            f'{RUN_ID}\n\n'),
                    color('white',
                            f'\N{RIBBON}  bundling params:  ')
#                    f'\N{SQUARED ID} wrapper instance: {RUN_ID}'
                ) # alt deco: \N{SQUARED ID} \N{LABEL}
    
            
            ##~~~~~~~ Initialize & Print PDB if Chosen from CLI  ~~~~~~~~~~~
    
            if wrapperArgs.pdb:
                # Connect to Database!
                PDB_CONNECTION = pdb.initDB(wrapperArgs.pdb)
                displaypdb = color('green2', wrapperArgs.pdb)
                
                
            else:
                wrapperArgs.pdb = None
                displaypdb = redNone
        
            #~~~~~~~~~~~~~~~~~ Print DB Connection Obj ~~~~~~~~~~~~~~~~~~~~~
            
            # CUTE BUT DISTRACTING.... fix up UI later
#            if PDB_CONNECTION:
#                decoL = '\N{HANDSHAKE}'
#                decoR = '' # \N{LINK SYMBOL} 
#                print(
#                    f"{decoL} "\
#                    f"{color('black', 'initialized')},"\
#                    f"{color('black', str(PDB_CONNECTION))}"\
#                    f" {decoR}")
            
            if wrapperArgs.pdb:
                print(
                    color('blue2', f'\n \N{HEAVY MINUS SIGN} PDB: \t'), 
                    displaypdb)
            else:
                print(
                    color('blue2', f'\n \N{HEAVY MINUS SIGN} PDB: \t'), 
                    displaypdb)
                
            
            
            ##~~~~~~~~ Initialize INput File & Display Choice ~~~~~~~~~~~~~~
            if wrapperArgs.batch:
                # input tile is already opened for you by argparser!
                fi = wrapperArgs.batch
                input_filename = fi.name
                batchlines = [line.strip() for line in fi]
                fi.close()
                
                print(
                    color('blue2', f' \N{HEAVY MINUS SIGN} Input: \t'), 
                    color('green2', f'{input_filename} '), 
                    color('cyan2', f'({len(batchlines)} lines)'))
                
                outputToFile = True
                
            else:
                print(
                    color('blue2', f' \N{HEAVY MINUS SIGN} Input: \t'),
                    color('white', 'manual'))
                
                outputToFile = False  # TODO: for now!
    
    
            fo = None
            ##~~~~~~~~~ Initialize OUTPUT File & Display Choice ~~~~~~~~~~~#
            if outputToFile:
                initDirectory(OUTPUT_DIRECTORY)
                
                if wrapperArgs.o:
                    output_filename = ''\
                    f'{OUTPUT_DIRECTORY}{RUN_ID}.json'
                else:
                    output_filename = ''\
                    f'{OUTPUT_DIRECTORY}'\
                    f'{st.get_base_file_name(input_filename)}__{RUN_ID}.json'
                
                fo = open(output_filename, 'w')
                print(
                    color('blue2', f' \N{HEAVY MINUS SIGN} Output: \t'), 
                    color('blue', f'{output_filename}')
                )
                
                if wrapperArgs.o:
                    logfile = f'{OUTPUT_DIRECTORY}{RUN_ID}.log'
                else:
                    logfile = ''\
                    f'{OUTPUT_DIRECTORY}'\
                    f'{st.get_base_file_name(input_filename)}__{RUN_ID}.log'
                    
                log = logger.initLogger(logfile)
                
                print(color('blue2', f' \N{HEAVY MINUS SIGN} Log: \t'),
                      color('blue', f'{logfile}')) # \N{MEMO} 
                
            else:
                print(
                    color('blue2', f' \N{HEAVY MINUS SIGN} Output:\t'),
                    'stdout'
                )
                print(
                    color('blue2', f' \N{HEAVY MINUS SIGN} Log:\t'), 
                    color('red', 'none')
                )
                
                logfile = None
                log = None
                
                if wrapperArgs.o:
                    print(
                        color("yellow",
                                "\n\nI didn't actually implement writing results"\
                                '/logging to file with one-by-one inputs'\
                                "because it's a hell of a fringe case... "\
                                "Sorry! ¯\/_(ツ)_//¯.\n ")
                    )
            
        
            
            resultsDictionary = {}
            maxrss_start = platform_info.getMaxRSS()
            
            # =====++======  GET FRESH ARGS FOR SOLVER  ==========+=========
            # This loop repeats until/unless:
            # - you are doing batch input from file
            # - 
            
            while 1:
                
                ARGSLIST = []
                print(color('white', f'\n \N{BUILDING CONSTRUCTION}   with args: '))
                
                if wrapperArgs.pdb:
                    ARGSLIST.append(PDB_CONNECTION)
                    ARGSLIST.extend(
                        ['-f', ''.join(['pdb_', wrapperArgs.pdb])]
                    )
                
                wroteLogHeaderInfo = False
                # Log Header info for an input batch is collected
                # when the first input is run, and is written once.
                # (Since the contents of the header are the same for all
                # runs in he batch)
                
                while 1:
                    printArgs(ARGSLIST)
                    nextArg = input()
                    exit_if_exit(nextArg)
                    
                    if not nextArg:
                        print(SEPARATOR_DASH)
                        print(' - RUN: press SPACE, '\
                                'double-tap Enter, or type run or ok')
                        
                        print(' - DELETE: type del x to remove'\
                            'the last x arguments entered (default 1)')
                        print(SEPARATOR_DASH)
                        
                        
                        nextArg = input()
                        exit_if_exit(nextArg)
                        if not nextArg:
                            break # stop taking input
                        
    #                nextArg = nextArg.strip()
    #                exit_if_exit(nextArg)
                    
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
                                    print(
                                        color('magenta', 'To change '\
                                        'PDB choice, exit program.'))
                                    break
                        else:
                            for i in range(n):
                                if ARGSLIST:
                                    ARGSLIST.pop()
                        continue
                    
                    
                    if nextArg in ['', 'run', 'ok']:
                        break # stop taking input 
                    
                    
                    if nextArg in ['help', 'h']:    # concise help
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
                        print(
                            color('white1', '\n \N{BUILDING CONSTRUCTION}  '),
                            color('white2', 'adding...')
                        )
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
                        print(
                            color('red','Err:'), 
                            f'{nextArg} not accepted.'
                        )
                        print(
                            color('white', 
                            'Specify seconds (-ts, -tsec) '\
                            'or minutes (-tm, -tmin)')
                        )
                        continue
                    
                    
                    elif nextArg in ['--str', '-str']:
                        ARGSLIST.append(nextArg)
                        print(
                            color('yellow', 
                                f'Enter the string for arg '\
                                f'{nextArg} on its own line:')
                        )
                        stringAccepted = False
                        while not stringAccepted:
                            nextArg = input()
                            
                            exit_if_exit(nextArg)
                            nextArg = nextArg.strip()
                            if not nextArg:
                                break
                            if ',' not in nextArg:
                                print(
                                    color('red','Err:'), 
                                    'numbers must be separated by commas'
                                )
                                
                            if any(ch in ['\\','\'','\"'] for ch in nextArg):
                                print(
                                    color('red','Err:'),
                                    'unlike cli, do NOT contain '\
                                    'string in quotes or escape any chars'
                                )
                            else:
                                stringAccepted = True
                                ARGSLIST.append(nextArg)
                        
                    elif nextArg in ['--ints', '-ints']:
                        ARGSLIST.append(nextArg)
                        print(
                            color('yellow', 
                                'Enter numbers separated by spaces '\
                                '(no other characters)'))
                        nextArg = input()
                        
                        exit_if_exit(nextArg)
                        nextArg_list = nextArg.split()
                        ARGSLIST.extend(nextArg_list)
                    
                    else:
                        ARGSLIST.append(nextArg)
                
                
                if (wrapperArgs.pdb and len(ARGSLIST) > 3) or \
                (not wrapperArgs.pdb and len(ARGSLIST) > 0) or \
                (wrapperArgs.batch):
                    if wrapperArgs.batch:
                        
                        # It's lowkey so ghetto do define decent sized funcs
                        # like this nested within several loops... 
                        # TODO: please fix! <3
                        def printRunHeader():

#                            txt = [
#                                ''.join((
#                                    ' '*2, 
#                                    "\N{RUNNER} \N{RUNNER} \N{RUNNER}"\
#                                    " RUNNING SOLVER:     ")
#                                ),
#                                f' {n_processed+1} / {num_lines} ', 
#                                '\u23f3 '\
#                                f'{secondsToWhatever(perf_counter()-t_start)}'
#                            ]
#                            
#                            label = ''.join(
#                                (color
#                                    ('magenta2', txt[0]), 
#                                    color('cyan2', txt[1])
#                                ))
#                            blankspace = ' '*(len(SEPARATOR_DOT)-5-len(''.join(txt)))
#                            timeElapsed = color('blue', txt[2])
#                            
#                            print(''.join((label, blankspace, timeElapsed)))
                            
                            # TODO: THIS FORMATTING IDEA IS CUTE BUT I DON'T HAVE TIME FOR IT 
#                            text = [
#                                f'{n_processed+1} / {num_lines}',
#                                color('blue', f'  \u23f3  {secondsToWhatever(perf_counter()-t_start)}'),
#                                f'\N{RIBBON} \u2715 \N{PACKAGE} \u27f6 \N{WRAPPED PRESENT}',
#                                color(
#                                    'white2', 
#                                    f'wrapper: \N{RIBBON} \u2715 \N{PACKAGE}  '\
#                                    f'\u27f6  solver(\N{WRAPPED PRESENT})'),
#                                color(
#                                    'white2', 
#                                    f'wrapper ( \N{RIBBON} \u2715 \N{PACKAGE} )  '\
#                                    f'\u27f6  \N{WRAPPED PRESENT};  solver(\N{WRAPPED PRESENT})'),
#                            ]
#                            for t in text:
#                                print(t)
                        
#                            print(color('white', f'{SEPARATOR_DOT}\n'))
                            print(f'{SEPARATOR_DOT}\n')
                            
                            txt = [
                                ['white', '   > > > > >    '],
                                ['white2', 'SEARCHING   '],
                                ['magenta2', f'{n_processed+1} / {num_lines}'],
                                ['blue2', f'\u23f3  {secondsToWhatever(perf_counter()-t_start)}']
                            ]
                            
                            placeholder = ''.join([ele[1] for ele in txt][:-1])
                            
                            blankspace = ' ' * ( len(SEPARATOR_DOT) 
                                                - len(placeholder) 
                                                - len(txt[3][1]) -6 )
                            
                            colorized = [color(ele[0], ele[1]) for ele in txt]
                            line_ = ''.join(colorized[:-1]+[blankspace]+colorized[-1:])
                            print(line_)
                            
#                            print(color('white', f'\n{SEPARATOR_DOT}'))
                            print(f'\n{SEPARATOR_DOT}')
                            
#                            print(
#                                color('blue2', f'\n \N{INPUT SYMBOL FOR NUMBERS}  INPUT:\t'),
#                                color('green2', f'{input_filename}'))
#                            print(color('blue2', f'\n \N{bar chart}  OUTPUT:\t'),
#                                f'{output_filename}')
#                            print(color('blue2', f'\n \N{MEMO}  LOG:\t'),
#                                f'{logfile}') 
#                            print(f'{SEPARATOR_DASH}\n')
                            

                            # TODO: THIS IS SO FKN CUTE BUT DEAL WITH IT LATER!!!! LOL
#                            print(color('white2', f'\n   wrapper'), 
#                                  color('white', '(\N{RIBBON} \u2715 \N{PACKAGE} )  \u27f6  \N{WRAPPED PRESENT}\n'))
                            
                            print(
                                color('white', f'\n  \N{RIBBON}  bundle\t'),
                                color('red2', (f'{RUN_ID}')))
                            
                            print(
                                color('white', f'\n  \N{PACKAGE}  input\t'),
                                color('green2', f'{input_filename}'),
                                color('white', f'\t('),
                                color('cyan2', f'{n_processed+1}'),
                                color('white', f'of'),
                                color('cyan2', f'{num_lines}'),
                                color('white', ')')
                            )
                            
                            
#                            print(color('white', f'\n{SEPARATOR_DOT}'))
                            print(f'\n{SEPARATOR_DOT}')
                            
                            print(color('white', '\n Calling solver with '))
                            printArgs(argsThisRun, areWrapped=True)
#                            print(color('white2', f'\n{SEPARATOR_DOT}\n'))
                            print(f'\n{SEPARATOR_DOT}\n')
                            
                            
                        
                        def printFooter(log):
                            t_elaps = secondsToWhatever(perf_counter()-t_start)
                            printAndOrLog(f' Processed {n_processed} inputs in  {t_elaps}', log)
                            printAndOrLog(f'{SEPARATOR_DOT}\n', log)
                            
                            if n_fail:
                                print(" \u274C", color('red2', f'{n_fail}'), color('white', 'of'), color('red2', f'{num_lines}'), color('white', 'inputs'), color('red2','failed'), color('white', '(had errors)'))
                                printAndOrLog(f'  {n_fail} or {num_lines} inputs failed (had errors)', log, doNotPrint=True)
                                if n_success:
                                    print("  \u2714", color('green2', f'{n_success}'), color('white', 'of'), color('green2', f'{num_lines}'), color('white','inputs processed successfully'))
                                    printAndOrLog(f'  {n_success} of {num_lines} inputs processed successfully', log, doNotPrint=True)
                                
                            else: # success only
                                print(" \u2705", color('green2', f'{n_success}'), color('white', 'of'), color('green2', f'{num_lines}'), color('white','inputs processed successfully'))
                                printAndOrLog(f'  {n_success} of {num_lines} inputs processed successfully', log, doNotPrint=True)
                                
                                
                            print(f'\n \u231B time elapsed: {secondsToWhatever(perf_counter()-t_start)}')
                            print(color('blue2', "\n \N{HEAVY MINUS SIGN} results: \t"), color('green2', f'{output_filename} '))
                            print(color('blue2', f'\n \N{HEAVY MINUS SIGN} log: \t'), f'{logfile}') 
                            # alt \N{MEMO} or \N{SPIRAL NOTE PAD}
                            
                            printAndOrLog(f'{SEPARATOR_DOT}', log)
                            
                            printAndOrLog(f'Max RSS (of wrapper and all runs): {platform_info.prettyMemory(platform_info.getMaxRSS()-maxrss_start)}', log)
                            printAndOrLog(f'Keep in mind all results are held in memory and are dumped to json at the end.  ', log)
                        
                        def writeOutput(do_call_printFooter=True):
                            if outputToFile:
                                try:
                                    json.dump(resultsDictionary, fo, allow_nan=True, indent=4, sort_keys=True)
                                    print(' Successfully wrote results to json file.')
                                except:
                                    print(' Writing results failed.')
                            if do_call_printFooter:
                                printFooter(log)
                            
                        
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
                                
#                                print(color('yellow',
#                                            f'DEBUG: wrapper | wrapper|'\
#                                            f'line {lineno()} |'\
#                                            'calling callSolver,'\
#                                            'expecting 3 return vals')
#                                )
                                outcome = callSolver(argsThisRun, silent=True)
                                
                                if outcome: 
                                    success, logheader, resultSet = outcome
                                
                                    if log and \
                                    resultSet and \
                                    not wroteLogHeaderInfo:
                                        logger.printLogHeader(log, RUN_ID, input_filename, output_filename, logheader['psize'], logheader['algo'], logheader['heur'], logheader['timeout_s'], logheader['goal'])
#                                        print(color('yellow',
#                                                    f'DEBUG: wrapper | wrapper| line {lineno()} |'\
#                                                    'Wrote logheader to log file')
#                                        )
                                        wroteLogHeaderInfo = True
                                else:
                                    success = None
                                    logheader = None
                                    resultSet = None
                                    
                                n_processed += 1
                                if success is not None:
                                    n_success += 1
                                else:
                                    n_fail += 1
                                
                                if resultSet:
                                    resultsDictionary[n_processed] = resultSet.copy()
                                    # NOTE:  FAILED RUNS ARE NOT RECORDED TO LOG OR REUSLTS RN!
                                print('\n')
                            
                            writeOutput()
                            break
                        except Exception as exc:
                            printException(exc, lineno())
                            continue
                        except SystemExit as sysex:
                            printException(sysex, lineno())
                            print(f'^^ That was printException called from wrapper line {lineno()}. \n'\
                                    ' now calling clean-up-and-exit ')  
                            close_DB_and_exit()
                        
                    else:
                        try:
#                            print(f'DEBUG: calling callSolver from {lineno()}')
                            
                            success, logheader, resultSet = callSolver(ARGSLIST)
                            
                            if log and not wroteLogHeaderInfo:
                                log.printLogHeader(log, RUN_ID, input_filename, output_filename, logheader['psize'], logheader['algo'], logheader['heur'], logheader['timeout_s'], logheader['goal'])
                                wroteLogHeaderInfo = True
                                
#                                print(color('yellow',
#                                            f'DEBUG: wrapper | wrapper| line {lineno()} |'\
#                                            'Wrote logheader to log file')
#                                )
                                
                            continue
                        except Exception as exc:
                            printException(exc, lineno())
                            continue
    #                    except SystemExit as sysex:
    #                        printException(sysex, lineno())
                            
                        
                else:
#                    print(color('yellow',
#                                f'DEBUG: wrapper | wrapper | '\
#                                'line {lineno()} |'\
#                                '"break"ing out of outer loop')
#                    )
                    break
                
            
            if wrapperArgs.pdb:
                PDB_CONNECTION.close()
                print(color('white', 'SQLite connection closed. Bye!'))
                
    #        if fo: fo.close()
        
        
        ##### THIS TRY BLOCK ENCASES WHOLE PROGRAM #####
        except Exception as exc:
            print('I wonder if this block ever catches anything? lol')
            print(color('yellow',
                        f'DEBUG: wrapper | wrapper| line {lineno()} |'\
                        'calling printException...')
            )
            printException(exc, lineno())
            close_DB_and_exit()
            
    #        if fo:fo.close()
        
    
    except KeyboardInterrupt as k:
        broom = '\N{BROOM}'
        checkmark= '\u2705'
        print_task = lambda task: print(color('white2', f'\n{task} ... {broom}'))
        print_done = lambda: print(color('white', f'{HALF_INDENT}{checkmark} Done'))
        print_failed = lambda errormsg: print(color('white', f'{HALF_INDENT}\N{CROSS MARK} Failed\n{errormsg}'))
        
        printException(k, lineno(), verbose=False)
        
        try:
            t_elaps = secondsToWhatever(perf_counter()-t_start)
            printAndOrLog(f'Interrupted after {t_elaps}', log)
        except: pass
        
#        print(f'\nlogfile: {logfile}\n'\
#              'open file object: {fo}\n'\
#              'PDB_CONNECTION: {PDB_CONNECTION}\n')
        
        print(color('white2', f'\nCleaning up ... {broom}'))
        print('Will save whatever information is available.')
        results_collected = len(resultsDictionary)
        print(f'Results in memory: {results_collected}')
        
        if PDB_CONNECTION:
            print_task('Closing database connection')
            PDB_CONNECTION.close()
            print_done()
        
        if logfile and results_collected:
            print_task('Writing to log')
            try:
                printFooter(log)
                print_done()
            except:
                print_failed('Failed to update log')
        
        if fo and results_collected:
            print_task('Writing results to disk')
            try:
                writeOutput(do_call_printFooter=False)
                print_done()
            except:
                print_failed('Failed writing results to disk')
                print('Dumping results...\n\n\n\n')
                
                print(resultsDictionary)
                print('\n\n\n\nSEPARATOR_EQ')
                print(f'Results unable to be saved to file and have '\
                        'been dumped to output above. \nPlease copy '\
                        'them or they will be lost.')
                print('\nSEPARATOR_EQ')
            
        print(color('white2', '\nCleanup tasks finished.'))
        print(color('white', 'Exiting.\n'))
        exit()