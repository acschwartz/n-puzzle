#!/usr/bin/env python3



#import argparse
import sys
import sqlite3
import resource
import tracemalloc
from time import perf_counter
from random import shuffle


#from npuzzle.visualizer import visualizer
from npuzzle.search import a_star_search, ida_star_search
from npuzzle.is_solvable import is_solvable
from formatting import colors
from formatting.colors import color
from npuzzle import parser
from npuzzle import heuristics
from npuzzle import goal_states
from npuzzle.pdb import pdb
from npuzzle.pdb.eightpuzzle.subprof15 import subprof15
from npuzzle import timeout
from npuzzle.timeout import prettyTime

# TODO: these submodules need to be organized better with the project
from npuzzle.platform_info import prettyMemory
from formatting.exceptions import *


colors.enabled = True


def pretty_print_steps(steps, size):
    width = len(str(size*size))
    decor = '-'
    for n in range(len(steps)):
        if n == 0:
            print('-[initial state]%s' % (4*decor,))
        else:
            print('-[step %2d]%s' % (n,10*decor,))    
        print()
        for i in range(size):
            for j in range(size):
                tile = str(steps[n][i*size+j])
                if tile == '0':
                    tile = color('red2', '-'*width)
                print(' %*s' % (width, tile), end='')
            print()
        print()
    print('%s' % (20*decor,))



def secToMin(seconds):
    return seconds/60

def minToSec(minutes):
    return minutes*60

def KBtoBytes(kb):
    return kb * 1024.0

def bytesToKB(bytes):
    return bytes / 1024.0

def standardizeMemoryToBytes(memValReturnedByOS):
    if sys.platform.beginswith('darwin'):
        print('-----hello from macOS;-----')
        return memValReturnedByOS # as bytes
    else:
        return KBtoBytes(memValReturnedByOS)

def color_yes_no(v):
    return color('green', 'YES') if v else color('red', 'NO')

def verbose_info(args, puzzle, goal_state, size, PDB_CONNECTION):
    opts1 = {
#            'greedy search:': args.g,
#            'uniform cost search:': args.u,
#            'visualizer:': args.v,
            'solvable:': is_solvable(puzzle, goal_state, size)              # TODO: SHOULD HAVE OOP.... isInstance...
            }
    opt_color = 'white'
    for k,v in opts1.items():
        print(color(opt_color, k), color_yes_no(v))
    
    for k,v in {'heuristic function:': color('cyan2', args.f)}.items():
            print(color('red', k), v)
    
    opts2 = {#'heuristic function:': color('green2', args.f),
#            'pdb:': color('green2', args.pdb if args.pdb else 'None'),
#            'puzzle size:': str(size),
            'solution type:': color('green2', args.s),
            'initial state:': str(puzzle),
#            'final state:': str(goal_state)}
             }
    for k,v in opts2.items():
            print(color(opt_color, k), v)

    if is_solvable(puzzle, goal_state, size):
        print(color('blue', 'heuristic scores for initial state'))
        for k,v in heuristics.KV.items():
            try:
                print(color('blue', '  - ' + k + '\t:'), v(puzzle, goal_state, size, PDB_CONNECTION))
            except:
                continue
    
    emoji_randomness = ['\N{SLOT MACHINE}', '\N{GAME DIE}', '\N{GAME DIE}', '\U0001F0CF',
        '\u2666\uFE0F', '\u2660\uFE0F', '\u2663\uFE0F']
    black_suits = ['\u2660\uFE0F ', '\u2663\uFE0F ']
    red_suits = ['\u2665\uFE0F ', '\u2666\uFE0F ']
    shuffle(emoji_randomness)
    print(color('red2', 'search algorithm:'), (f'{emoji_randomness[0]} IDA* random node ordering (IDA*-R)' if args.r else 'IDA*') if args.ida else 'A*')


#########################################################################################

def solver(arglist=None, returnHValueOnly=False):
    try:
        global PDB_CONNECTION
    
        # if None passed, uses sys.argv[1:], else use custom args
        receivedDBConnectionAsArgument = False
        try:
            if arglist:
    #            print(f'\n{__name__}: args received from function call: {arglist}\n')
                if isinstance(arglist[0], sqlite3.Connection):
                    print('DB connected already!')
                    PDB_CONNECTION = arglist.pop(0)
                    print(PDB_CONNECTION)
                    receivedDBConnectionAsArgument = True
                else:
                    PDB_CONNECTION = None
                data = parser.get_input(arglist)
            else:
                data = parser.get_input()
                print(f'\n{__name__}: args received from command line: {data}\n')
                PDB_CONNECTION = None
        
            
    
            if not data:
                print('solver.py return')
                return (None, None, 0) 
            # (None, None, None) throws an exception when you try to unpack it
    
        except Exception as exc:
            printException(exc, lineno())
    #        sys.exit(exc)
        
        
        puzzle, size, args = data    
        
        #------------- SET UP LOG HEADER SCHEMA -----------#
        logheader = {
            'psize': size,
            'algo': ('IDA*-R' if args.r else 'IDA*') if args.ida else 'A*',
            'heur': args.f,
            'timeout_s': None,
            'goal': args.s
            
        }
        #---------------------------------------------------#
        
        #----------------- INIT RESULTSET ------------------#
        
        resultSet = {}
        
        #---------------------------------------------------#
        
        
    
        if args.ida:
            args.g = False
        
        RANDOM_NODE_ORDER = args.r
    
        TRANSITION_COST = 1
        if args.g:
            TRANSITION_COST = 0
    
        HEURISTIC = heuristics.KV[args.f]
        if args.u:
            HEURISTIC = heuristics.uniform_cost
        
        if args.f.startswith('pdb_') and not PDB_CONNECTION:
            pdbtype = args.f[4:]
            PDB_CONNECTION = pdb.initDB(pdbtype)
        
        if args.f == 'pdb_8SubPrOf15':
            print(f'REAL init state: {puzzle}')
            print(f"REAL goal state: {subprof15.PUZZLE_INFO['goal_state']}: {subprof15.PUZZLE_INFO['goal state repr']}")
            print(f'Being remapped to 8-puzzle so can be solved... then will turn back..... ') # TODO: make this clean plug-in later
            puzzle = subprof15.PUZZLE_INFO['encode'](puzzle)
            
            
        goal_state = goal_states.KV[args.s](size)

        # -------- RETURN H VALUE ONLY OPTION (NO SEARH) --------- #
        if returnHValueOnly:
            return HEURISTIC(puzzle, goal_state, size, PDB_CONNECTION)

        verbose_info(args, puzzle, goal_state, size, PDB_CONNECTION)

        if not is_solvable(puzzle, goal_state, size):
            print(color('red','this puzzle is not solvable'))
            return (None, logheader, resultSet)
        
        # code snippet for making IDA* memory profiling work on linux
        # problem: tracemalloc prohibitively slow, and maxrss doesn't capture it
        # NOTE: !!!!!! only implemented for 15-puzzle
    #    USING_LINUX_MEMORY_WORKAROUND_FOR_15PUZZLE = (size == 4) and (sys.platform == 'linux') and (args.ida)
        USING_LINUX_MEMORY_WORKAROUND_FOR_15PUZZLE = False
        
        if not USING_LINUX_MEMORY_WORKAROUND_FOR_15PUZZLE:
            if args.tracemalloc:
                tracemalloc.start()
            else:
                maxrss_before_search = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                print(color('white', 'max rss before search:'), maxrss_before_search)
    

        # -------- SEARCH --------- #
        t_before_search = perf_counter()
        if args.tmin:
            TIMEOUT_SEC = minToSec(args.tmin)
            timeout.setAlarm(TIMEOUT_SEC)
            logheader['timeout_s'] = TIMEOUT_SEC
        if args.tsec:
            TIMEOUT_SEC = args.tsec
            timeout.setAlarm(TIMEOUT_SEC)
            logheader['timeout_s'] = TIMEOUT_SEC
        res = None
        searchTimedOut = False
        
        
        if args.ida:
            try:
                res = ida_star_search(puzzle, goal_state, size, HEURISTIC, TRANSITION_COST, RANDOM_NODE_ORDER, PDB_CONNECTION)
                timeout.turnOffAlarm()
            except timeout.TimeOutException:
                searchTimedOut = True
    #            emoji = ( '\N{NO ENTRY SIGN} \N{STOPWATCH} ')
    #            print('t\o at ')
    #            timeOutMessage = color('red2', f' \N{ALARM CLOCK} Search timed out after {TIMEOUT_SEC} seconds ({secToMin(TIMEOUT_SEC)} mins !)')
    #            print(timeOutMessage)
                from npuzzle.search import ida_star_nodes_generated, ida_star_max_path_length
                print(f'Nodes generated: {ida_star_nodes_generated}')
                res = (False, None, {'space':ida_star_max_path_length, 'time':ida_star_nodes_generated})
                timeout.turnOffAlarm()
        else:
            try:
                res = a_star_search(puzzle, goal_state, size, HEURISTIC, TRANSITION_COST, PDB_CONNECTION)
                timeout.turnOffAlarm()
            except timeout.TimeOutException:
                searchTimedOut = True
    #            print(color('red2', f' \N{NO ENTRY SIGN}\N{STOPWATCH} Search timed out after {TIMEOUT_SEC} seconds ({secToMin(TIMEOUT_SEC)} mins !)'))
                from npuzzle.search import a_star_nodes_generated
                print(f'Nodes generated: {a_star_nodes_generated}')
                res = (False, None, {'space':a_star_nodes_generated, 'time':a_star_nodes_generated})
                timeout.turnOffAlarm()
        t_search = perf_counter() - t_before_search
        
        success, steps, complexity = res
        from npuzzle.search import ida_star_nodes_generated, ida_star_max_path_length, a_star_nodes_generated
        
        if args.f == 'pdb_8SubPrOf15':
            decode = subprof15.PUZZLE_INFO['decode']
            puzzle = decode(puzzle)
            steps = [decode(state) for state in steps]
        
        if not USING_LINUX_MEMORY_WORKAROUND_FOR_15PUZZLE:
            if args.tracemalloc:
                peak = tracemalloc.get_traced_memory()[1]
                tracemalloc.stop()
                print(color('magenta', 'peak memory use (tracemalloc): '), prettyMemory(peak))
                print(color('magenta', 'memory per node: '), f"{prettyMemory(peak/complexity['time'])}")
    
            else:
                maxrss_after_search = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                print(color('white', 'max rss after search: '), maxrss_after_search)
                
                # on macOS ('darwin'), max_rss reported in bytes
                # on linux, in kB
                maxrss_delta = maxrss_after_search-maxrss_before_search
                maxrss_delta_pretty = prettyMemory(maxrss_delta)
                print(color('magenta', 'peak memory use (Δ maxrss): '), maxrss_delta_pretty)
                print(color('magenta', 'memory per node: '), f"{prettyMemory(maxrss_delta/complexity['time'])}")
    #    else:
    #        # NOTE: !!! only implemented for manhattan and LC heuristics
    #        peak = complexity['space']  # nodes in memory
    #        if args.f == 'manhattan':
    #            nodesize = 1.5 * 1024  #kB to bytes
    #        elif args.f == 'conflicts' or args.f == 'lc':
    #            nodesize = 3.0 * 1024  #kB to bytes
    #        else:
    #            print('main: linux memory workaround not implemented')
    #            nodesize = 0
    #            # should prob throw exception but this is thrown together ¯\_(ツ)_/¯
    #        peak *= nodesize
    #        print(color('red', 'peak memory use (calculated): '), bytes_to_human_readable_string(peak))
        print(color('yellow2', f' \u231B search duration: {prettyTime(t_search)}'))
        print(color('magenta2','space complexity:'), f"{complexity['space']:,}", 'nodes in memory')
        print(color('green2','time complexity:'), f"{complexity['time']:,}", 'nodes generated')
        print(f" {(t_search / max(complexity['time'],1)):.5f}")
    #    fmt = '%d' + color('green2',' nodes generated, ') + '%.8f' + color('green',' second(s) per node')
    #    print(fmt % (complexity['time'], t_search / max(complexity['time'],1) ))
        
        print('\n')
        if searchTimedOut:
            print(color('red2', f' \N{ALARM CLOCK} Search timed out after'),(color('white2', f'{prettyTime(TIMEOUT_SEC)} ')))
        if success:
            print(color('yellow', '\N{GLOWING STAR} solution found '))
            print(color('yellow2','length of solution:'), max(len(steps) - 1, 0))
            print(str(puzzle).replace(',','').replace('(','').replace(')',''))
            if args.showsteps or args.p:
                print(color('green', '\N{WORLD MAP} initial state and solution steps:'))  # or \N{FOOTPRINTS}
                if args.p:
                    pretty_print_steps(steps, size)
                else:
                    for s in steps:
                        if args.f == 'pdb_8SubPrOf15':
                            print(color('magenta', f'{s}'), '   <--->   ', color('yellow', f"{subprof15.PUZZLE_INFO['encode'](s)}"))
                        else:
                            print(s)
    
        else:
            print(color('red',' \N{THUMBS DOWN SIGN} solution not found'))
    #    if success and args.v:
    #        visualizer(steps, size)
        
        if not receivedDBConnectionAsArgument:
            try:
                PDB_CONNECTION.close()
            except:
                pass
        
        if steps:
            sol_len= max(len(steps) - 1, 0)
        else:
            steps = 0
            sol_len = -1
        # -------- POPULATE RESULTSET --------#
        resultSet = {
            'init': str(puzzle),
            'foundSol': success,  # none if failed, False if not found, True if found
            'timedOut': searchTimedOut,
            'runtime_sec': t_search,
            'nodes_gen': res[2]['time'],
            'algo': logheader['algo'], # for knowing which is time and space complexity
            'heuristic': logheader['heur'],
            'h_val': HEURISTIC(puzzle, goal_state, size, PDB_CONNECTION),
            'sol_len': sol_len,
            'max_path_len': (ida_star_max_path_length if args.ida else sol_len),
            'n_puzzle': size**2-1,
            'goal': args.s,
            # don't include memory measurement probbaly
        }
        # -------- POPULATE RESULTSET --------#
        
    #    print(color('white2', '\n\nReturning (success, logheader, resultSet)'))
    #    print(color('white2', '\nsuccess:'), f'{success}')
    #    print(color('white2', '\nlogheader:'), f'\n{logheader}')
    #    print(color('white2', '\nresultSet:'), f'\n{resultSet}')
        print('\n')
        
        return (success, logheader, resultSet)
    
    except KeyboardInterrupt as k:
        raise KeyboardInterrupt(''\
            'KeyboardInterrupt from solver.py: \n'\
            'Returning to wrapper.py to clean up before exiting...')
    
    
#--- TAKING AWAY ABILITY TO CALL IT AS A SCRIPT FOR NOW....
# --- I LKE MY WRAPPER BETTER FOR ME
    
#if __name__ == '__main__':  
#    # find '-f' in argsv without doing parseargs - just 'peeking' to pre-set up the DB
##    args = sys.argv[1:]
##    print(args)
##    heuristic = args[(args.index('-f')+1)]
##    if heuristic.startswith('pdb_'):
##        pdbname = heuristic[4:]
##        # actually I don't know if I need the above... lol
#        
#    global PDB_CONNECTION
#    PDB_CONNECTION = None
#    
#    main(sys.argv[1:])
    