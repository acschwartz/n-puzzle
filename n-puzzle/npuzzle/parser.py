import argparse
from npuzzle import heuristics
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
    return 'ok'

def get_input():
    parser = argparse.ArgumentParser(description='n-puzzle @ 42 fremont')
    parser.add_argument('-c', action='store_true', help='colors')
    parser.add_argument('-ida', action='store_true', help='ida* search')
    parser.add_argument('-r', action='store_true', help='random node ordering')
    parser.add_argument('-g', action='store_true', help='greedy search')
    parser.add_argument('-u', action='store_true', help='uniform-cost search')
    parser.add_argument('-f', help='heuristic function', choices=list(heuristics.KV.keys()), default='manhattan')
    parser.add_argument('-s', help='goal state', choices=list(goal_states.KV.keys()), default='snail')
    parser.add_argument('-p', action='store_true', help='pretty print solution steps')
#    parser.add_argument('-v', action='store_true', help='gui visualizer')
    parser.add_argument( '--str', dest='commas', action = 'store', type = str, help = 'input passed as string in form: \(1,2,3..\), \"(1,2,3,..)\", 1,2,3,.., \"1,2,3,..\" (commas required)' )
    parser.add_argument('--file', help='input file', type=argparse.FileType('r'))
    parser.add_argument( '--ints', metavar='N', action = 'store', nargs='*', type = int, help = 'input passed as cli args: 0 1 2 3 ...' )
    parser.add_argument('-tracemalloc', '--tracemalloc', action='store_true', help='use tracemalloc to profile memory (default: resource module maxrss)')
    args = parser.parse_args()
    

    if not (args.file or args.commas or args.ints):
        print('parser: no input')
        print('for help: main.py --help')
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
            print('parser: invalid input, puzzle is not square:', puzzle)
            return None
        # TODO : could use more input validation for 'commas' at some point (works fine)
        
    if args.file:
        validator = is_valid_input(puzzle)
        if validator != 'ok':
            print('parser: invalid input,',v)
            return None
        puzzle1d = []                   #convert 2d matrix into list
        for row in puzzle:
            for item in row:
                puzzle1d.append(item)
    return (tuple(puzzle1d), size, args)
