#!/usr/bin/env python3
from math import floor, ceil

def encode8puzzle(pattern):
# includes locations of the pattern tiles but not the empty tile
    encoding = [0, 0, 0, 0]
    i=0
    for n in pattern:
        encoding[floor(i/2)] += n*(1<<(4*(~i&1)))
        i+=1
    return bytes(encoding)

def decode8puzzle(bytestr):
# includes locations of the pattern tiles but not the empty tile
    decoded = []
    for n in bytestr:
        decoded.append((n//16) % 16)
        decoded.append(n%16)
    return tuple(decoded)


def convertState_8pzSubProb_MapTilesTo8Puzzle(subproblemState):
# map tiles from the 8-pizzle-equivalent subproblem of the 15-puzzle
# input: STATE - NOT!!! PATTERN!! of the subproblem  e.g. (0, 1, 2, 4, 5, 6, 8, 9, 10)  (goal state)
# output: STATE of traditional 8-puzzle            e.g.   (0, 1, 2, 3, 4, 5, 6, 7, 8)  (goal state)
# then that output state can be sent to  makeInitialNode- which does all the encoding/decoding for you as an 8-puzzle
    mapping_from_subproblem_tiles_to_8puzzle = {0:0,  1:1,  2:2,  4:3,  5:4, 6:5,  8:6,  9:7,  10:8}
    return [mapping_from_subproblem_tiles_to_8puzzle[tile] for tile in subproblemState] # = eightPuzzleState


def convertState_8puzzle_ReMapTiles_ToSubproblem(eightpuzzleState):
    mapping_tiles_from_8puzzle_to_subproblem = {0:0,  1:1,  2:2,  3:4,  4:5, 5:6,  6:8,  7:9,  8:10}
    return [mapping_tiles_from_8puzzle_to_subproblem[tile] for tile in eightpuzzleState] # = subproblem state


'''
What is my goal with the 8-puzzle subproblem? plug-and-play into the existing, working 8-puzzle generator
Input from Solver to DB ---> Subproblem State (Could just be encoded.... honestly thats seems betterm to have an 
encoding function.
Maybe I could generate a parallel database to see if they give the same value? yeah that sounds cool...
The only "encoding" i'd need to look stuff up in the 8-puzzle database is the mappings of the tiles
so I can generate the database key
'''





def encode15puzzle_fringe_DummyTile(pattern):    # odd length pattern
# e.g.     pattern2 = [3,7,0,12,13,14,15] ---> b'\x13\x70\xcd\xef'
# this is an odd-length pattern and the left-most 1 in the encoding is a dummy -
# it will be cleaved off during decoding.
# although this means there is technically room to store the location of the empty tile,
# I won't here to make it compatible with my existing implementation that tracks it separately
# That way, I can just plug-and-play the 15-puzzle.
# There is an encoding option that does include the empty tile in unittests.py
    encoding = [16, 0, 0, 0]
    i=0
    for n in pattern:
        encoding[ceil(i/2)] += n*(1<<(4*(i&1)))
        i+=1
            
#    # DEBUG:
#    print(encoding)
#    print([hex(n) for n in encoding])
#    print(bytes(encoding))
    return bytes(encoding)


def decode15puzzle_fringe_DummyTile(bytestr):
# e.g.     pattern2 = b'\x13\x70\xcd\xef' ---> [3,7,0,12,13,14,15]
    decoded = []
    for n in bytestr:
        decoded.append((n//16) % 16)
        decoded.append(n%16)
    del decoded[0]    # cleaves off the dummy leftmost digit
    return tuple(decoded)