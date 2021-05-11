#!/usr/bin/env python3

import sys
import resource
import tracemalloc
from time import perf_counter
#from npuzzle.visualizer import visualizer
from npuzzle import search
from npuzzle.is_solvable import is_solvable
from npuzzle import colors
from npuzzle.colors import color
from npuzzle import parser
from npuzzle import heuristics
from npuzzle import goal_states
from npuzzle.pdb import pdb
from npuzzle import timeout
import sqlite3

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


def bytes_to_human_readable_string(size,precision=2):
# SOURCE: https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python/14822210
# http://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])


def color_yes_no(v):
    return color('green', 'YES') if v else color('red', 'NO')

def verbose_info(args, puzzle, goal_state, size, PDB_CONNECTION):
    opts1 = {
            'greedy search:': args.g,
            'uniform cost search:': args.u,
#            'visualizer:': args.v,
            'solvable:': is_solvable(puzzle, goal_state, size)
            }
    opt_color = 'cyan2'
    for k,v in opts1.items():
        print(color(opt_color, k), color_yes_no(v))

    opts2 = {'heuristic function:': color('green2', args.f),
#            'pdb:': color('green2', args.pdb if args.pdb else 'None'),
            'puzzle size:': str(size),
            'solution type:': color('green2', args.s),
            'initial state:': str(puzzle),
            'final state:': str(goal_state)}
    for k,v in opts2.items():
            print(color(opt_color, k), v)

   
    # NOTE: removed because it wasn't vibing with my handling of the pdb's.. worry bout it later (TODO)
    if is_solvable(puzzle, goal_state, size):
        print(color('blue2', 'heuristic scores for initial state'))
        for k,v in heuristics.KV.items():
            try:
                print(color('blue2', '  - ' + k + '\t:'), v(puzzle, goal_state, size, PDB_CONNECTION))
            except:
                continue

    print(color('red2', 'search algorithm:'), ('IDA* w/ random node ordering (IDA*-R)' if args.r else 'IDA*') if args.ida else 'A*')


#########################################################################################

def main(arglist=None):
    global PDB_CONNECTION

    # if None passed, uses sys.argv[1:], else use custom args
    if arglist:
        print(f'\n{__name__}: args received from function call: {arglist}\n')
        if isinstance(arglist[0], sqlite3.Connection):
            print('DB connected already!')
            PDB_CONNECTION = arglist.pop(0)
            print(PDB_CONNECTION)
        else:
            PDB_CONNECTION = None
        data = parser.get_input(arglist)
    else:
        data = parser.get_input()
        print(f'\n{__name__}: args received from command line: {data}\n')
        PDB_CONNECTION = None
        
    if not data:
        return None
    puzzle, size, args = data

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
        
    
    goal_state = goal_states.KV[args.s](size)
    verbose_info(args, puzzle, goal_state, size, PDB_CONNECTION)
    if not is_solvable(puzzle, goal_state, size):
        print(color('red','this puzzle is not solvable'))
        sys.exit(0)
    
    # code snippet for making IDA* memory profiling work on linux
    # problem: tracemalloc prohibitively slow, and maxrss doesn't capture it
    # NOTE: !!!!!! only implemented for 15-puzzle
    USING_LINUX_MEMORY_WORKAROUND_FOR_15PUZZLE = (size == 4) and (sys.platform == 'linux') and (args.ida)
#    USING_LINUX_MEMORY_WORKAROUND_FOR_15PUZZLE = False
    
    if not USING_LINUX_MEMORY_WORKAROUND_FOR_15PUZZLE:
        if args.tracemalloc:
            tracemalloc.start()
        else:
            maxrss_before_search = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#            print(color('red', 'max rss before search:'), maxrss_before_search)


    # -------- SEARCH --------- #
    t_before_search = perf_counter()
    if args.tmin:
        TIMEOUT_SEC = args.tmin * 60 
        timeout.setAlarm(TIMEOUT_SEC)
    res = None
    if args.ida:
        try:
            res = search.ida_star_search(puzzle, goal_state, size, HEURISTIC, TRANSITION_COST, RANDOM_NODE_ORDER, PDB_CONNECTION)
            timeout.turnOffAlarm()
        except timeout.TimeOutException:
            print(f'Search timed out after {args.tmin} minutes')
            print(f'Nodes generated: {search.ida_star_nodes_generated}')
            res = (False, None, {'space':None, 'time':search.ida_star_nodes_generated})
            timeout.turnOffAlarm()
    else:
        try:
            res = search.a_star_search(puzzle, goal_state, size, HEURISTIC, TRANSITION_COST, PDB_CONNECTION)
            timeout.turnOffAlarm()
        except timeout.TimeOutException:
            print(f'Search timed out after {args.tmin} minutes')
            print(f'Nodes generated: {search.a_star_nodes_generated}')
            res = (False, None, {'space':search.a_star_nodes_generated, 'time':search.a_star_nodes_generated})
            timeout.turnOffAlarm()
    t_search = perf_counter() - t_before_search
    
    success, steps, complexity = res
    
    if not USING_LINUX_MEMORY_WORKAROUND_FOR_15PUZZLE:
        if args.tracemalloc:
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            print(color('red', 'peak memory use (tracemalloc): '), bytes_to_human_readable_string(peak))
        else:
            maxrss_after_search = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#            print(color('red', 'max rss after search: '), maxrss_after_search)
            
            # on macOS ('darwin'), max_rss reported in bytes
            # on linux, in kB
            MAXRSS_UNIT_COEFFICIENT = 1024 if sys.platform != 'darwin' else 1
            maxrss_delta = bytes_to_human_readable_string((maxrss_after_search-maxrss_before_search) * MAXRSS_UNIT_COEFFICIENT, 2)
            print(color('red', 'peak memory use (Δ maxrss): '), maxrss_delta)
    else:
        # NOTE: !!! only implemented for manhattan and LC heuristics
        peak = complexity['space']  # nodes in memory
        if args.f == 'manhattan':
            nodesize = 1.4 * 1024  #kB to bytes
        elif args.f == 'conflicts' or args.f == 'lc':
            nodesize = 3.0 * 1024  #kB to bytes
        else:
            print('main: linux memory workaround not implemented')
            nodesize = 0
            # should prob throw exception but this is thrown together ¯\_(ツ)_/¯
        peak *= nodesize
        print(color('red', 'peak memory use (calculated): '), bytes_to_human_readable_string(peak))

    print(color('yellow','search duration:') + ' %.4f second(s)' % (t_search))
    fmt = '%d' + color('yellow',' nodes generated, ') + '%.8f' + color('yellow',' second(s) per node')
    print(fmt % (complexity['time'], t_search / max(complexity['time'],1) ))
    if success:
        print(color('green','length of solution:'), max(len(steps) - 1, 0))
        if args.showsteps or args.p:
            print(color('green', 'initial state and solution steps:'))
            if args.p:
                pretty_print_steps(steps, size)
            else:
                for s in steps:
                    print(s)
    else:
        print(color('red','solution not found'))
    print(color('magenta','space complexity:'), complexity['space'], 'nodes in memory')
    print(color('magenta','time complexity:'), complexity['time'], 'nodes generated')
#    if success and args.v:
#        visualizer(steps, size)
    
    try:
        PDB_CONNECTION.close()
    except:
        pass
    
if __name__ == '__main__':  
    # find '-f' in argsv without doing parseargs - just 'peeking' to pre-set up the DB
    args = sys.argv[1:]
    print(args)
    heuristic = args[(args.index('-f')+1)]
    if heuristic.startswith('pdb_'):
        pdbname = heuristic[4:]
        # actually I don't know if I need the above... lol
        
    global PDB_CONNECTION
    PDB_CONNECTION = None
    
    main(sys.argv[1:])
    