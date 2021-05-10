#!/usr/bin/env python3

import unittest
from math import floor, ceil
from timeit import timeit

import inspect
myself = lambda: inspect.stack()[1][3]

from dbtools import db
from pdbgen import generator
from pdbgen import logger
from pdbgen import encoding
from pdbgen import patterns

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
	
	
	def test_encode_stub(self):
		def encodePattern(pattern):
			patternEvenLength = bool(~len(pattern)&1)
			
			# this if statement should be later removed for optimization - pick an encoding!
			if DEBUG: print(f'\n{myself()}: pattern: {pattern}')
			if patternEvenLength:
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
		encoding1 = encodePattern(pattern1)
		self.assertEqual(encoding1, b'\x13\x7b\xcd\xef')
		if TIMEIT: print(f'\n{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern1))}')
		
		pattern2 = [3,7,0,12,13,14,15]
		encoding2 = encodePattern(pattern2)
		self.assertEqual(encoding2, b'\x13\x70\xcd\xef')
		if TIMEIT: print(f'{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern2))}')
		
		pattern3 = [0,3,7,11,12,13,14,15]
		encoding3 = encodePattern(pattern3)
		self.assertEqual(encoding3, b'\x03\x7b\xcd\xef')
		if TIMEIT: print(f'{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern3))}')
		
		pattern4 = [12,1,4,5,14,9,10,0]
		encoding4 = encodePattern(pattern4)
		self.assertEqual(encoding4, b'\xc1\x45\xe9\xa0')
		if TIMEIT: print(f'{myself()}: timeit encodePattern: {timeit(lambda: encodePattern(pattern4))}')
		
		eightpuzzle1 = [1,2,3,4,5,6,7,8]
		encode_8p1 = encodePattern(eightpuzzle1)
		self.assertEqual(encode_8p1, b'\x12\x34\x56\x78')
	
	def test_decode_stub(self):
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
		if TIMEIT: print(f'\n{myself()}: timeit decodebytes: {timeit(lambda: decodebytes(b1, False))}')
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
		
		eightpuzzle1 = (1,2,3,4,5,6,7,8)
		decode_8p1 = decodebytes(b'\x12\x34\x56\x78', True)
		if DEBUG: print(decode_8p1)
		self.assertEqual(decode_8p1, eightpuzzle1)
		# TODO: Fix this "include empty tile" business!! 
		# this puzzle doesn't even include the empty tile.. ugh lol
	
	
	if TIMEIT:
		def test_target_pattern_list_compr(self):
			pname = 'full8puzzle'
			ptiles = patterns.PATTERN_INFO[pname]['pattern tiles']
			goalstate = patterns.PATTERN_INFO[pname]['goal state']
			pattern = []
			
			def forloop():
				for tile in ptiles:
					pattern.append(goalstate.index(tile))
			
			def listcompr():
				pattern = [goalstate.index(tile) for tile in ptiles]
			
			print(f'{myself()}: timeit forloop: {timeit(forloop)}')
			print(f'{myself()}: timeit listcompr: {timeit(listcompr)}')


class DatabaseTestsInMemory(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(DatabaseTestsInMemory, self).__init__(*args, **kwargs)
		
	def test_initDB_memory(self):
		con, cur = db.initDB(':memory:')
		self.assertIsNotNone(con)
		self.assertIsNotNone(cur)
		con.close()
	
	def test_createTables_memory(self):
		con, cur = db.initDB(':memory:')
		tablenames = db.createTables(cur, n_tables=2, base_name='table')
		self.assertEqual(set(tablenames), set(['table0', 'table1']))
		con.close()
	
	def test_insert(self):
		con, cur = db.initDB(':memory:')
		tablenames = db.createTables(cur, n_tables=1, base_name='table')
		
		table = tablenames[0]
		data = ( (bytes([1]), 21), (bytes([2]), 22), (bytes([255]), 99))
		for pattern, cost in data:
			db.insert(cur, table, pattern, cost)
		
		cur.execute("SELECT * from %s"%table)
		results = set(cur.fetchall())
		expected_results = set(data)
		self.assertEqual(results, expected_results)
		con.close()
	# TODO: what happens when insert duplicate value?
	
	
	def test_checkRowExists(self):
		con, cur = db.initDB(':memory:')
		tablenames = db.createTables(cur, n_tables=1, base_name='table')
		
		table = tablenames[0]
		data = ( (bytes([1]), 21), (bytes([2]), 22), (bytes([255]), 99))
		for pattern, cost in data:
			db.insert(cur, table, pattern, cost)
			
		exists1 = db.checkRowExists(cur, table, data[2][0], attribute='pattern')
		self.assertTrue(exists1)
		exists2 = db.checkRowExists(cur, table, bytes(2), attribute='pattern')
		self.assertFalse(exists2)
		con.close()

#class DatabaseTests(unittest.TestCase):
#	def __init__(self, *args, **kwargs):
#		super(DatabaseTests, self).__init__(*args, **kwargs)
#		from dbtools import db
#		self.con, self.cur = db.initDB()
#		self.assertIsNotNone(self.con)
#		self.assertIsNotNone(self.cur)
#	
#	def test_1(self):
#		pass

class LoggerTests(unittest.TestCase):
	def test_logging(self):
		log, logfile = logger.initLogger(logfile='test/testlog.log')
		
		print()
		log.debug(f'{myself()}: debug message. it should not be printed to the logfile')
		log.log(15, f'{myself()}: level 15. it should go to stdout only, not the logfile')
		log.info(f'{myself()}: info message. this should go to stdout AND BE PRINTED TO THE LOGFILE')

class TestEncoding(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super(TestEncoding, self).__init__(*args, **kwargs)
		self.eightpuzzles = (
			{ 'pattern': (1,2,3,4,5,6,7,8), 'encoding': b'\x12\x34\x56\x78' },
			{ 'pattern': (0,6,2,7,4,3,8,1), 'encoding': b'\x06\x27\x43\x81' },
			{ 'pattern': (8,0,7,3,1,6,5,4), 'encoding': b'\x80\x73\x16\x54' },
			{ 'pattern': (8,4,7,3,1,6,5,0), 'encoding': b'\x84\x73\x16\x50' },
		)
	
	def test_encode8puzzle(self):
		puzzles = self.eightpuzzles
		res = []
		for p in puzzles:
			res.append(encoding.encode8puzzle(p['pattern']))
		
		for i, e in enumerate(res):
			self.assertEqual(e, puzzles[i]['encoding'])
			
	
	def test_decode8puzzle(self):
		puzzles = self.eightpuzzles
		res = []
		for p in puzzles:
			res.append(encoding.decode8puzzle(p['encoding']))
			
		for i, e in enumerate(res):
			self.assertEqual(e, puzzles[i]['pattern'])
			
	def test_makeInitialNode(self):
		pname = 'full8puzzle'
		ptiles = patterns.PATTERN_INFO[pname]['pattern tiles']
		goalstate = patterns.PATTERN_INFO[pname]['goal state']
		emptytile = patterns.PATTERN_INFO[pname]['empty tile']
		encode = patterns.PATTERN_INFO[pname]['encode']
		decode = patterns.PATTERN_INFO[pname]['decode']
		
		initnode, len_encoded_pattern = generator.makeInitialNode(ptiles, emptytile, goalstate, encode)
		pattern, nodeinfo = generator.splitNode(initnode, len_encoded_pattern)
		print(decode(pattern))
		print(nodeinfo)
		

##==============================================================================================##
if __name__ == '__main__':
	unittest.main()