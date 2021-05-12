import argparse
from npuzzle import heuristics
from npuzzle import pdb
from npuzzle import goal_states
from math import sqrt

def is_valid_input(data):
    if len(data[0]) != 1:
        return 'first line of input should be a single number (size)'  # first list[] in data must be size of matrix
    size = data.pop(0)[0]
    if size < 2:                        # puzzle too small?
        return 'puzzle too small'
    if len(data) != size:               # data[] should be an array of size N lists[]
        return 'number of rows doesnt match puzzle size'
    for line in data:                   # each list[] must be of size N (data must be square matrix)
        if len(line) != size:
            return 'number of columns doesnt match puzzle size'
    expanded = []
    for line in data:
        for x in line:
            expanded.append(x)
    generated = [x for x in range(size**2)]
    difference = [x for x in generated if x not in expanded]
    if len(difference) != 0:
        return 'puzzle tiles must be in range from 0 to SIZE**2-1'
    return True

def is_valid_pdb(pdb_name, goal_state, size):
    if size != pdb.PDBINFO[pdb_name]['size']:
        return 'mismatched sizes'
    if goal_state != pdb.PDBINFO[pdb_name]['goal_state']:
        return 'mismatched goal states'
    return True

def setup_parser():
    parser = argparse.ArgumentParser(description='n-puzzle solver ')
#    parser.add_argument('-c', action='store_false', help='no colors', default=True)
    parser.add_argument('-f', help='heuristic function', choices=list(heuristics.KV.keys()), default="manhattan")
    parser.add_argument('-ida', action='store_true', help='ida* search (default is A*)')
    parser.add_argument('-r', action='store_true', help='random node ordering (for IDA*)')
    parser.add_argument('-tmin', '-tm', dest='tmin', metavar='MINUTES', action='store', type=int, help='timeout (minutes)')
    parser.add_argument('-tsec', '-ts', dest='tsec', metavar='SECONDS', action='store', type=int, help='timeout (seconds)')
    parser.add_argument( '-str', '--str', dest='commas', action = 'store', type = str, help = 'input passed as string in form: \(1,2,3..\), \"(1,2,3,..)\", 1,2,3,.., \"1,2,3,..\" (commas required)' )
    parser.add_argument('-file', '--file', help='input file containing a single puzzle', type=argparse.FileType('r'))
    parser.add_argument( '-ints', '--ints', metavar='N', action = 'store', nargs='*', type = int, help = 'input passed as cli args: 0 1 2 3 ...' )
    parser.add_argument('-tracemalloc', '--tracemalloc', dest='tracemalloc', action='store_true', help='use tracemalloc to profile memory (default: resource module maxrss)')
    parser.add_argument('-g', action='store_true', help='greedy search')
    parser.add_argument('-u', action='store_true', help='uniform-cost search')
#    parser.add_argument('-pdb', help='pattern database as heuristic function', choices=list(pdb.PDBINFO.keys()))
    parser.add_argument('-s', help='goal state', choices=list(goal_states.KV.keys()), default='zero_first')
    parser.add_argument('-steps', dest='showsteps', action='store_true', help='show solution steps')
    parser.add_argument('-p', action='store_true', help='pretty print solution steps')
#    parser.add_argument('-v', action='store_true', help='gui visualizer')
    return parser
    

def get_input(altargs=None):
    parser = setup_parser()
    
    if altargs:
        args = parser.parse_args(altargs)
    else:
        args = parser.parse_args()
    
#    print(f'\nget_input: args received by parser: {args}\n')

    if not (args.file or args.commas or args.ints):
        args = ['-h']
        parser.parse_args(args)
        return None
    
    if not args.f:
        print('parser: please specify heuristic function or pattern database to use')
        return None
    
    if args.tmin and args.tsec:
        print('parser: please enter timeout in either minutes OR seconds')
        return None
    
    if args.file: 
        data = args.file.read().splitlines()
        args.file.close()
        data = [line.strip().split('#')[0] for line in data]      #remove comments
        data = [line for line in data if len(line) > 0]           #remove empty lines
        puzzle = []
        for line in data:
            row = []
            for x in line.split(' '):
                if len(x) > 0:
                    if not x.isdigit():
                        print('parser: invalid input, must be all numeric')
                        return None
                    row.append(int(x))
            puzzle.append(row)
        size = puzzle[0][0]
    
    if args.commas:
        puzzle_as_string = args.commas
        print(puzzle_as_string)
        puzzle = eval(puzzle_as_string)
        puzzle1d = puzzle
    if args.ints:
        puzzle = args.ints
        puzzle1d = args.ints
    
    if args.commas or args.ints:
        size = sqrt(len(puzzle))
        if size.is_integer():
            size = int(size)
        else:
            print('parser: invalid input, puzzle is not square:', puzzle, ";  size:", size)
            return None
        # TODO : could use more input validation for 'commas' at some point (works fine)
        
    if args.file:
        validator = is_valid_input(puzzle)
        if validator is not True:
            print('parser: invalid input,', validator)
            return None
        puzzle1d = []                   #convert 2d matrix into list
        for row in puzzle:
            for item in row:
                puzzle1d.append(item)
    
#    if args.pdb:
#        validator = is_valid_pdb(args.pdb, args.s, size)
#        if validator is not True:
#            print('parser: invalid pdb/puzzle combo,', validator)
#            return None
        
    return (tuple(puzzle1d), size, args)
