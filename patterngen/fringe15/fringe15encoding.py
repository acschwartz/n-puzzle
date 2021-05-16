#!/usr/bin/env python3

def encode_pattern(pattern, DEBUG=None):
	if DEBUG: print(f'\n{myself()}: pattern: {pattern}')
	
	if DEBUG: 
			print('\nk = n*(1<<(4*(~i&1)))')
			print(f'i\tfloor(i/2)\tn\tk\thex(k)')
			
	encoding = [0, 0, 0, 0]
	i=0
	for n in pattern:
		if DEBUG: 
			k = 16**(~i&1)*n
			print(f'{i}\t{ceil(i/2)}\t\t{n}\t{k}\t{hex(k)}')
		encoding[floor(i/2)] += n*(1<<(4*(~i&1)))
		i+=1
	
	if DEBUG:
		print(encoding)
		print([hex(n) for n in encoding])
		print(bytes(encoding))
		
	return bytes(encoding)