#!/usr/bin/env python3

#!/usr/bin/env python3
from math import floor, ceil
from npuzzle.pdb.eightpuzzle.full8puzzle import full8puzzle

BASE_TABLE_NAME = full8puzzle.BASE_TABLE_NAME 
N_TABLES = full8puzzle.N_TABLES
TABLES = full8puzzle.TABLES




def remapTilesTo8Puzzle(state_as_SubPrOf15):
# map tiles from the 8-pizzle-equivalent subproblem of the 15-puzzle
# input: STATE - NOT!!! PATTERN!! of the subproblem  e.g. (0, 1, 2, 4, 5, 6, 8, 9, 10)  (goal state)
# output: STATE of traditional 8-puzzle            e.g.   (0, 1, 2, 3, 4, 5, 6, 7, 8)  (goal state)
# then that output state can be sent to  makeInitialNode- which does all the encoding/decoding for you as an 8-puzzle
    print(f'called subprof15.remapTilesTo8Puz | input: {state_as_SubPrOf15}')
    mapping_tiles_from_SubProbOf15_to_8Puzzle = {0:0,  1:1,  2:2,  4:3,  5:4, 6:5,  8:6,  9:7,  10:8}
    print(f'mapping function: {mapping_tiles_from_SubProbOf15_to_8Puzzle}')
    remap = [mapping_tiles_from_SubProbOf15_to_8Puzzle[tile] for tile in state_as_SubPrOf15]
    print(f'remap / output: {remap}')
    return tuple(remap) # returns an eightPuzzleState


def remap8PuzzleTilesToSubPrOf15(state_as_8puzzle):
    print(f'called subprof15.remap8PuzzleTilesToSubPrOf15 | input: {state_as_8puzzle}')
    mapping_tiles_from_8Puzzle_to_SubPrOf15 = {0:0,  1:1,  2:2,  3:4,  4:5,  5:6,  6:8,  7:9,  8:10}
    print(f'mapping function: {mapping_tiles_from_8Puzzle_to_SubPrOf15}')
    remap = [mapping_tiles_from_8Puzzle_to_SubPrOf15[tile] for tile in state_as_8puzzle]
    print(f'remap / output: {remap}')
    return tuple(remap) # return SubProf15 state    



def convertToQueryable(state):
    # state will be of form  (0, 1, 2, 4, 5, 6, 8, 9, 10)  (e.g. goal state)
    # where the index is the actual location of in the puzzle
    # and the value is the nubmered square
    # the pattern is represented the opposite of this
    
    state_remapped_to_8puzzle = remapTilesTo8Puzzle(state)
    return full8puzzle.convertToQueryable(state_remapped_to_8puzzle)


# 0  1  2
# 4  5  6
# 8  9 10
PUZZLE_INFO = {
                'dim': 3,
                'pattern tiles': (1, 2, 4, 5, 6, 8, 9, 10),
                'goal state repr': (0, 1, 2, 4, 5, 6, 8, 9, 10),
                'goal_state': 'zero_first',
                'empty tile': 0,
                'dbfile': full8puzzle.PUZZLE_INFO['dbfile'],
                'encode': remapTilesTo8Puzzle,
                'decode': remap8PuzzleTilesToSubPrOf15, 
                }
                

def validatePuzzle(puzzle, size, args, pzinfo=PUZZLE_INFO):    # TODO: could probs be generalized later
    if size != pzinfo['dim']:
        return False, f"puzzle size ({size}) does not match pattern size ({pzinfo['dim']})"
    if set(puzzle) != set(pzinfo['goal state repr']):
        return False, f"puzzle tiles {puzzle} do not match pattern tiles {pzinfo['goal state repr']}"  #??? pattern tiles???
    if args.s != pzinfo['goal_state']:
        return False, f"goal states don't match: {args.s} and {pzinfo['goal_state']}"
    # does not check for solvability, that's elsewhere!
    # are those all the checks?
    return True, None