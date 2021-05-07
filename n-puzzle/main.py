#!/usr/bin/env python3

import sys
import resource
import tracemalloc
from time import perf_counter
#from npuzzle.visualizer import visualizer
from npuzzle.search import a_star_search, ida_star_search
from npuzzle.is_solvable import is_solvable
from npuzzle import colors
from npuzzle.colors import color
from npuzzle import parser
from npuzzle import heuristics
from npuzzle import goal_states
from npuzzle import pdb

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

def verbose_info(args, puzzle, goal_state, size):
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
            'pdb:': color('green2', args.pdb if args.pdb else 'None'),
            'puzzle size:': str(size),
            'solution type:': color('green2', args.s),
            'initial state:': str(puzzle),
            'final state:': str(goal_state)}
    for k,v in opts2.items():
        print(color(opt_color, k), v)
   
    # NOTE: removed because it wasn't vibing with my handling of the pdb's.. worry bout it later (TODO)
#    print(color('blue2', 'heuristic scores for initial state'))
#    for k,v in heuristics.KV.items():
#        print(color('blue2', '  - ' + k + '\t:'), v(puzzle, goal_state, size))

    print(color('red2', 'search algorithm:'), ('IDA* w/ random node ordering (IDA*_R)' if args.r else 'IDA*') if args.ida else 'A*')


#########################################################################################

def main(arglist=None):
    # if None passed, uses sys.argv[1:], else use custom args
    if arglist:
        data = parser.get_input(arglist)
    else:
        data = parser.get_input()
        
    if not data:
        return None
    puzzle, size, args = data
    if args.c:
        colors.enabled = True

    if args.ida:
        args.g = False
    
    RANDOM_NODE_ORDER = args.r

    TRANSITION_COST = 1
    if args.g:
        TRANSITION_COST = 0

    HEURISTIC = heuristics.KV[args.f]
    if args.u:
        HEURISTIC = heuristics.uniform_cost

    goal_state = goal_states.KV[args.s](size)
    verbose_info(args, puzzle, goal_state, size)
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
    
#    t_start = perf_counter()
    if args.pdb and not pdb.PATTERN_DATABASE:
        time_to_load_pdb = pdb.load_pdb(args.pdb)
        print(color('yellow','time to load PDB:') + ' %.4f second(s)' % (time_to_load_pdb))
    t_before_search = perf_counter()
    if args.ida:
        res = ida_star_search(puzzle, goal_state, size, HEURISTIC, TRANSITION_COST, RANDOM_NODE_ORDER)
    else:
        res = a_star_search(puzzle, goal_state, size, HEURISTIC, TRANSITION_COST)
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

    
if __name__ == '__main__':    
    main(sys.argv[1:])
    