#!/usr/bin/env python3

from fringe15.fringe15encoding import *

##====================================================================##
PATTERN_INFO = {
    '15puzzle_fringe': {
        # 0  -  -  3
        # -  -  -  7
        # -  -  -  11
        # 12 13 14 15
        
                'dim': 4,    # 15-puzzle is 4x4
                'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
                'goal state': (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),
                'empty tile': 0,
                'encode': encode_pattern,
                'decode': decode_pattern,
                },
}
##====================================================================##

def pretty_pattern(pattern_decoded, pinfo=PATTERN_INFO['15puzzle_fringe'], target_pattern=(0,3,7,11,12,13,14,15)):
    # pattern including empty tile at index 0, i.e. (0,3,7,11,12,13,14,15)
    dim = pinfo['dim']
    # ptiles

    # TODO: 
    board = ['-']*(dim*dim)
    for ref, pip in enumerate(pattern_decoded):
        n = target_pattern[ref]
        board[pip] = n
    pretty_pattern_string = ''
    for i, tile in enumerate(board):
        tile_str = str(tile)
        if len(tile_str) < 2:
            pretty_pattern_string = ''.join([pretty_pattern_string, f"{tile}", ' '*3])
        else:
            pretty_pattern_string = ''.join([pretty_pattern_string, f"{tile}", ' '*2])
        # yes these edge cases are not handled
        if i%dim == dim-1:
            pretty_pattern_string = ''.join([pretty_pattern_string, '\n'])
    return pretty_pattern_string
