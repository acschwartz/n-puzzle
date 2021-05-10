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

#def encode15puzzle_fringe(pattern):
## includes the location of the empty tile because there is room for it anyway
## (digit in the byte string not used by any pattern tiles
## e.g. a pattern like this: [0,3,7,11,12,13,14,15] ---> b'\x03\x7b\xcd\xef'

def encode15puzzle_fringe(pattern):	# odd length pattern
# e.g. 	pattern2 = [3,7,0,12,13,14,15] ---> b'\x13\x70\xcd\xef'
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
			
#	# DEBUG:
#	print(encoding)
#	print([hex(n) for n in encoding])
#	print(bytes(encoding))
	return bytes(encoding)


def decode15puzzle_fringe(bytestr):
# e.g. 	pattern2 = b'\x13\x70\xcd\xef' ---> [3,7,0,12,13,14,15]
	decoded = []
	for n in bytestr:
		decoded.append((n//16) % 16)
		decoded.append(n%16)
	del decoded[0]	# cleaves off the dummy leftmost digit
	return tuple(decoded)