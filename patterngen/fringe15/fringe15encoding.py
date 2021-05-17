#!/usr/bin/env python3

from math import floor, ceil

def encode_pattern(pattern, DEBUG=None):
	"""
	Input: pattern repr. WITH empty tile | Return: bytes encoding
	e.g. in: (0,3,7,11,12,13,14,15) | out: b'x\03x\7bx\cdx\ef'
	"""
#	if DEBUG: print(f'\npattern: {pattern}')
	
#	if DEBUG: 
#			print('\nk = n*(1<<(4*(~i&1)))')
#			print(f'i\tfloor(i/2)\tn\tk\thex(k)')
			
	encoding = [0, 0, 0, 0]
	i=0
	for n in pattern:
#		if DEBUG: 
#			k = 16**(~i&1)*n
#			print(f'{i}\t{ceil(i/2)}\t\t{n}\t{k}\t{hex(k)}')
		encoding[floor(i/2)] += n*(1<<(4*(~i&1)))
		i+=1
	
#	if DEBUG:
#		print(encoding)
#		print([hex(n) for n in encoding])
#		print(bytes(encoding))
		
	return bytes(encoding)


def decode_pattern(bytestr):
	"""
	Input: byte encoding | Return: pattern repr. WITH empty tile
	e.g. out: b'x\03x\7bx\cdx\ef' | out: (0,3,7,11,12,13,14,15)
	"""
	decoded = []
	for n in bytestr:
		decoded.append((n//16) % 16)
		decoded.append(n%16)
	return tuple(decoded)