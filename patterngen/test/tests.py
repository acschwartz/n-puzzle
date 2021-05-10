#!/usr/bin/env python3

import unittest
from math import floor, ceil
from timeit import timeit

import inspect
myself = lambda: inspect.stack()[1][3]

DEBUG = False
TIMEIT = False



##==============================================================================================##

#  U N I T   T E S T S

##==============================================================================================##

class TestStubs(unittest.TestCase):
	
	def test_bitwise_even_odd(self):
		odds = [1,3,5,7,9,11,13]
		evens = [0,2,4,6,8,10,12]
		for n in odds:
			self.assertEqual(n&1, 1)
			self.assertEqual(~n&1, 0)
		for n in evens:
			self.assertEqual(n&1, 0)
			self.assertEqual(~n&1, 1)
	
	def test_isolate_digits(self):
		def get10sDigit(n, base=10):  # 10s digit in base 10, whatever you call it in base 16, 16's place ?
			return (n//base) % base
		def get1sDigit(n, base=10):  # 1s digit in base 10, whatever you call it in base 16, 16's place ?
			return n % base
		
		self.assertEqual(get10sDigit(23), 2)
		self.assertEqual(get1sDigit(23), 3)
		self.assertEqual(get1sDigit(10), 0)
		self.assertEqual(get10sDigit(1), 0)
		# hex(16) = '0x10'
		self.assertEqual(get10sDigit(16, 16), 1)
		self.assertEqual(get1sDigit(16, 16), 0)
		# hex(117) = '0x75'
		self.assertEqual(get10sDigit(117, 16), 7)
		self.assertEqual(get1sDigit(117, 16), 5)
		# hex(250) = '0xfa'
		self.assertEqual(get10sDigit(250, 16), 15)
		self.assertEqual(get1sDigit(250, 16), 10)
		
		
	def test_digit_shift(self):
		for i, n in enumerate(range(256)):
			self.assertEqual(16**(i&1)*n, n*(1<<(4*(i&1))))
			
#	if DEBUG:
#		def test_visually_encoding_logic(self):
#			print(myself())
#			pattern = [3,7,11,12,13,14,15]
#			print()
#			for i, n in enumerate(pattern):
#				print(i, n, hex(16**(i&1)*n), 16**(i&1)*n)
#			print()
#			for i, n in enumerate(pattern):
#				print(i&1, 1<<4, 1<<(4*(i&1)), n*(1<<(4*(i&1))))
		
#	if TIMEIT:
#		def test_timing_exp_vs_bitwise(self):
#			print(myself())
#			pattern = [3,7,11,12,13,14,15]
#			
#			bitwise = lambda i,n: n*(1<<(4*(i&1)))
#			exp = lambda i,n: 16**(i&1)*n
#			
#			bitwise_listcompr = lambda: [bitwise(i,n) for i,n in enumerate(pattern)]
#			exp_listcompr = lambda: [exp(i,n) for i,n in enumerate(pattern)]
#			
#			t1 = timeit(bitwise_listcompr)
#			t2 = timeit(exp_listcompr)
#			print(f'\n{myself()}: timeit bitwise n*(1<<(4*(i&1))): {t1}')
#			print(f'{myself()}: timeit exp 16**(i&1)*n: {t2}')
#			
#			print(f'\n{myself()}: timeit bitwise n*(1<<(4*(i&1))) -- more granular')
#			for i,n in enumerate(pattern):
#				print(timeit(lambda: bitwise(i,n)))
#			
#			print(f'\n{myself()}: timeit exp 16**(i&1)*n -- more granular')
#			for i,n in enumerate(pattern):
#				print(timeit(lambda: exp(i,n)))
	
	
	def test_encode_logic(self):
		def encodePattern(pattern, includeEmptyTile):
			# this if statement should be later removed for optimization - pick an encoding!
			if DEBUG: print(f'\n{myself()}: pattern: {pattern}')
			if includeEmptyTile:
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
			else:
				if DEBUG: 
					print('\nk = n*(1<<(4*(i&1)))')
					print(f'i\tceil(i/2)\tn\tk\thex(k)')
				encoding = [16, 0, 0, 0]
				i=0
				for n in pattern:
					k = n*(1<<(4*(i&1)))
					if DEBUG: 
						print(f'{i}\t{ceil(i/2)}\t\t{n}\t{k}\t{hex(k)}')
					encoding[ceil(i/2)] += k
					i+=1
			
			if DEBUG:
				print(encoding)
				print([hex(n) for n in encoding])
				print(bytes(encoding))
			return bytes(encoding)

		pattern1 = [3,7,11,12,13,14,15]
		encoding1 = encodePattern(pattern1, False)
		self.assertEqual(encoding1, b'\x13\x7b\xcd\xef')
		if TIMEIT: print(f'\n{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern1, False))}')
		
		pattern2 = [3,7,0,12,13,14,15]
		encoding2 = encodePattern(pattern2, False)
		self.assertEqual(encoding2, b'\x13\x70\xcd\xef')
		if TIMEIT: print(f'{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern2, False))}')
		
		pattern3 = [0,3,7,11,12,13,14,15]
		encoding3 = encodePattern(pattern3, True)
		self.assertEqual(encoding3, b'\x03\x7b\xcd\xef')
		if TIMEIT: print(f'{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern3, True))}')
		
		pattern4 = [12,1,4,5,14,9,10,0]
		encoding4 = encodePattern(pattern4, True)
		self.assertEqual(encoding4, b'\xc1\x45\xe9\xa0')
		if TIMEIT: print(f'{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern4, True))}')
	
	
	def test_decode(self):
		def decodebytes(bytestr, includeEmptyTile):
			decoded = []
			for n in bytestr:
				decoded.append((n//16) % 16)
				decoded.append(n%16)
			if not includeEmptyTile:	# remove if statement for optimization
				del decoded[0]
			return tuple(decoded)
		
		b1 = b'\x13\x7b\xcd\xef'
		if DEBUG: print(decodebytes(b1, False))
		if TIMEIT: print(f'{myself()}: timeit decodebytes: {timeit(lambda: decodebytes(b1, False))}')
		self.assertEqual(decodebytes(b1, False), (3,7,11,12,13,14,15))
		
		b2 = b'\x13\x70\xcd\xef'
		if DEBUG: print(decodebytes(b2, False))
		if TIMEIT: print(f'{myself()}: timeit decodebytes: {timeit(lambda: decodebytes(b2, False))}')
		self.assertEqual(decodebytes(b2, False), (3,7,0,12,13,14,15))
		
		b3 = b'\x03\x7b\xcd\xef'
		if DEBUG: print(decodebytes(b3, True))
		if TIMEIT: print(f'{myself()}: timeit decodebytes: {timeit(lambda: decodebytes(b3, True))}')
		self.assertEqual(decodebytes(b3, True), (0,3,7,11,12,13,14,15))
		
		b4 = b'\xc1\x45\xe9\xa0'
		if DEBUG: print(decodebytes(b4, True))
		if TIMEIT: print(f'{myself()}: timeit decodebytes: {timeit(lambda: decodebytes(b4, True))}')
		self.assertEqual(decodebytes(b4, True), (12,1,4,5,14,9,10,0))



##==============================================================================================##
if __name__ == '__main__':
	unittest.main()