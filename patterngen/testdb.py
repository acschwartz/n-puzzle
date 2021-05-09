#!/usr/bin/env python3

import sqlite3
import pprint
from argparse import ArgumentParser
from time import perf_counter
from helpers.getmaxrss import *
from helpers.time import *
import dummyvalues

##==============================================================================================##

SEPARATOR = '=========================================================================='
SEPARATOR_SM = '--------------------------------------------------------------------------'

##==============================================================================================##

generate_dataset= {'ints_repr_hexvalues': dummyvalues.ints_repr_hexvalues,
			'hexstrings': dummyvalues.hexstrings, 
			'tuples_len8_pickled': dummyvalues.tuples_len8_pickled,
			'string_repr_tuples_of_ints': dummyvalues.string_repr_tuples_of_ints,
			'string_repr_tuples_whole_puzzle': dummyvalues.string_repr_tuples_whole_puzzle,
		}

def parseArgs():
	parser = ArgumentParser()
	parser.add_argument('datasetName', help='which dataset?', choices=list(generate_dataset.keys()))
	parser.add_argument( '-n', dest='n_entries', action = 'store', type = int, help = 'number of entries', default=10**6)
	parser.add_argument( '-d', dest='debug', action = 'store_true', help = 'debug mode (prints more stuff)')
	args = parser.parse_args()
	return args.datasetName, args.n_entries, args.debug


##==============================================================================================##
##==============================================================================================##

if __name__ == '__main__':
	datasetName, n_entries, DEBUG = parseArgs()
	
	DICT = generate_dataset[datasetName](n_entries)
	
	con = sqlite3.connect(':memory:')
	cur = con.cursor()

	
	if DEBUG: print('Creating table...')
	
	if datasetName in ['hexstrings', 'string_repr_tuples_of_ints', 'string_repr_tuples_whole_puzzle']:
		cur.execute('''
		CREATE TABLE patterncosts(
			pstring TEXT PRIMARY KEY,
			cost INTEGER
			) WITHOUT ROWID;
		''')
	
	elif datasetName == 'ints_repr_hexvalues':
		cur.execute('''
		CREATE TABLE patterncosts(
			pstring INTEGER PRIMARY KEY,
			cost INTEGER
			) WITHOUT ROWID;
		''')
	
	elif datasetName in ['tuples_len8_pickled']:
		cur.execute('''
		CREATE TABLE patterncosts(
			pstring BLOB PRIMARY KEY,
			cost INTEGER
			) WITHOUT ROWID;
		''')
	
	if DEBUG: print('Table created.')
	if DEBUG: print('Inserting values...')
	
	
	maxrss_start = getMaxRSS()
	time_start = perf_counter()
	for key in DICT:
	#	cur.execute(f'INSERT INTO patterncosts VALUES ({key}, {DICT[key]})')	# <-- didn't work for strings
		cur.execute("""INSERT INTO patterncosts(pstring, cost) 
							VALUES (?,?);""", (key, DICT[key]))
	
	del DICT
	
	time_delta = timeDelta(time_start)
	maxrss_after_populate_table = getMaxRSS()
	maxrss_delta_pretty = rawMaxRSStoPrettyString(maxrss_after_populate_table - maxrss_start)
	
	res = cur.execute("SELECT * from patterncosts LIMIT 1")
	for row in res:
		example_row = row
	
	if DEBUG:
		res = cur.execute("SELECT * from patterncosts")
		for row in res:
			print(row)
	
	if DEBUG: print(f'maxrss_after_populate_table: {maxrss_after_populate_table}')
	
	n_entries = len(DICT)
#	print('\n')
#	print(f'\n{SEPARATOR_SM}')
	print(f'\nPrimary key type: {datasetName}\t\te.g. {example_row}')
#	print(SEPARATOR_SM)
	print(f'{prettyTime(time_delta)} to insert {n_entries} entries')
	print(f'memory used: {maxrss_delta_pretty}')
#	print(SEPARATOR)