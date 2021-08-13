from solver import solver


# zero_first goal is assumed

def get_h_value(heuristic_name, puzzle_as_string):
    return main([heuristic_name, puzzle_as_string])

def main(args):
    heuristic_name = args[0]     # as string, e.g. 'manhattan'
    puzzle_as_string = args[1]   # as string, e.g. '(1, 8, 7, 3, 2, 5, 0, 6, 4)'
    return solver(['-f', heuristic_name, '--str', puzzle_as_string], returnHValueOnly=True)

if __name__ == '__main__': 
    import sys
    args = sys.argv[1:]
    main(args)