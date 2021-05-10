#!/usr/bin/env python3
from math import floor, ceil

def encode8puzzle(pattern):
	encoding = [0, 0, 0, 0]
	i=0
	for n in pattern:
		encoding[floor(i/2)] += n*(1<<(4*(~i&1)))
		i+=1
	return bytes(encoding)

def decode8puzzle(bytestr):
	decoded = []
	for n in bytestr:
		decoded.append((n//16) % 16)
		decoded.append(n%16)
	return tuple(decoded)