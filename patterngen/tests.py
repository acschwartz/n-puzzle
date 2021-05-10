#!/usr/bin/env python3

import unittest
from math import ceil
from timeit import timeit

import inspect
myself = lambda: inspect.stack()[1][3]

DEBUG = False
TIMEIT = True



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
			
	if DEBUG:
		def test_visually_encoding_logic(self):
			print(myself())
			pattern = [3,7,11,12,13,14,15]
			print()
			for i, n in enumerate(pattern):
				print(i, n, hex(16**(i&1)*n), 16**(i&1)*n)
			print()
			for i, n in enumerate(pattern):
				print(i&1, 1<<4, 1<<(4*(i&1)), n*(1<<(4*(i&1))))
		
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
				

		
	def test_encode(self):
		def encodePattern(pattern):
			encoding = [16, 0, 0, 0]
			for i, n in enumerate(pattern):
				k = ceil(i/2)
				encoding[k] += 16**(i&1) * n
			return bytes(encoding)
		
		pattern = [3,7,11,12,13,14,15]
		encoding = encodePattern(pattern)
		self.assertEqual(encoding, b'\x13\x7b\xcd\xef')
#		if TIMEIT: print(f'\n{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern))}')
	
	
	def test_encode_optimize(self):
		def encodePattern(pattern):
			encoding = [16, 0, 0, 0]
			i=0
			for n in pattern:
				encoding[ceil(i/2)] += n*(1<<(4*(i&1)))
				i+=1
			return bytes(encoding)

		pattern = [3,7,11,12,13,14,15]
		encoding = encodePattern(pattern)
		self.assertEqual(encoding, b'\x13\x7b\xcd\xef')
		if TIMEIT: print(f'\n{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern))}')
	
	
	def test_decode(self):
		def decodebytes(bytestr):
			decoded = []
			for n in bytestr:
				decoded.append((n//16) % 16)
				decoded.append(n%16)
			del decoded[0]
			return tuple(decoded)
		
		b = b'\x13\x7b\xcd\xef'
		if DEBUG: print(decodebytes(b))
		if TIMEIT: print(f'{myself()}: timeit decodebytes: {timeit(lambda: decodebytes(b))}')
		self.assertEqual(decodebytes(b), (3,7,11,12,13,14,15))



##==============================================================================================##
if __name__ == '__main__':
	unittest.main()