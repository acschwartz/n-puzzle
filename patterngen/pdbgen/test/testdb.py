#!/usr/bin/env python3

import sqlite3
import pprint
import os
import subprocess
from argparse import ArgumentParser
from helpers.memorytools import *
from helpers.timetools import *
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
            'binary_blob': dummyvalues.binary_blob,
        }

def parseArgs():
    parser = ArgumentParser()
    parser.add_argument('datasetName', help='which dataset?', choices=list(generate_dataset.keys()))
    parser.add_argument( '-n', dest='n_entries', action = 'store', type = int, help = 'number of entries', default=10**6)
    parser.add_argument( '-d', dest='debug', action = 'store_true', help = 'debug mode (prints more stuff)')
    args = parser.parse_args()
    return args.datasetName, args.n_entries, args.debug

def getRSS(pid=None):
    if not pid:
        pid = os.getpid()
    cmd_get_current_rss = f'ps -o rss= {pid}'
    output = subprocess.check_output(cmd_get_current_rss, shell=True)
    return int(output)
    

##==============================================================================================##
##==============================================================================================##

if __name__ == '__main__':
    datasetName, n_entries, DEBUG = parseArgs()
    pid = os.getpid()
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    
    DICT = generate_dataset[datasetName](n_entries)
    maxrss_start = getMaxRSS()
    time_start = pCounter()
    
    if DEBUG: print('Creating table...')
    
    if datasetName in ['hexstrings', 'string_repr_tuples_of_ints', 'string_repr_tuples_whole_puzzle']:
        cur.execute('''
        CREATE TABLE patterncosts(
            pattern TEXT PRIMARY KEY,
            cost INTEGER
            ) WITHOUT ROWID;
        ''')
    
    elif datasetName == 'ints_repr_hexvalues':
        cur.execute('''
        CREATE TABLE patterncosts(
            pattern INTEGER PRIMARY KEY,
            cost INTEGER
            ) WITHOUT ROWID;
        ''')
    
    elif datasetName in ['binary_blob', 'tuples_len8_pickled']:
        cur.execute('''
        CREATE TABLE patterncosts(
            pattern BLOB PRIMARY KEY,
            cost INTEGER
            ) WITHOUT ROWID;
        ''')
    
    if DEBUG: print('Table created.')
    if DEBUG: print('Inserting values...')
    
    
    for key in DICT:
    #    cur.execute(f'INSERT INTO patterncosts VALUES ({key}, {DICT[key]})')    # <-- didn't work for strings
        cur.execute("""INSERT INTO patterncosts(pattern, cost) 
                            VALUES (?,?);""", (key, DICT[key]))
    
    if DEBUG: print(f'current rss before del DICT: {getRSS()}')
    del DICT
    if DEBUG: print(f'current rss after del DICT: {getRSS()}')
    
    time_delta = timeDelta(time_start)
    maxrss_after_populate_table = getMaxRSS()
    maxrss_delta = maxrss_after_populate_table - maxrss_start
    maxrss_delta_pretty = prettyMemory(maxrss_delta)
    
    current_rss = getRSS()
    
    res = cur.execute("SELECT * from patterncosts LIMIT 1")
    for row in res:
        example_row = row
    
    if DEBUG:
        try:
            blob = b'\xfe\xff\x08\x06\x0f\x0f\x08\x06\x02'
            res = cur.execute("SELECT * from patterncosts where pattern=?", (blob,))
            print(f'\nres = {res}')
            for row in res:
                print(f'row = {row}')
        except:
            pass
    
    if DEBUG:
        def checkExists(cur, tablename, attribute, value):
            if DEBUG: print('\nHello from checkExists()!')
            res = cur.execute("SELECT EXISTS ( SELECT * from %s where %s = ?)"%(tablename, attribute), (value,))
            print(f'\nres = {res}')
#            for row in res:
#                print(f'row = {row}')
#                # row = (0,) if exists returned true
            exists = res.fetchone()[0]
            print(bool(exists))
            if DEBUG: print('Goodbye from checkExists()!\n')
            
        checkExists(cur, 'patterncosts', 'pattern', example_row[0])
    
    if DEBUG:
        blob = b'\xfe\xff\x08\x06\x0f\x0f\x08\x06\x02'
        res = cur.execute("SELECT EXISTS ( SELECT * from patterncosts where pattern= ? )", (blob,))
        print(f'\nres = {res}')
        for row in res:
            print(f'row = {row}')
            # row = (0,) if exists returned true
    
    if DEBUG:
        existing_blob = example_row[0]
        res = cur.execute("SELECT EXISTS ( SELECT * from patterncosts where pattern=?)", (existing_blob,))
        print(f'\nres = {res}')
        for row in res:
            print(f'row = {row}')
            # row = (1,) if exists returned true
    
    if DEBUG:
        i = input('press p if you want to see the table (SELECT * from patterncosts) ')
        if i == 'p':
            res = cur.execute("SELECT * from patterncosts")
            for row in res:
                print(row)
    
    if DEBUG: print(f'maxrss_start: {maxrss_start}\t{prettyMemory(maxrss_start)}')
    if DEBUG: print(f'maxrss_after_populate_table: {maxrss_after_populate_table}\t{prettyMemory(maxrss_after_populate_table)}')
    if DEBUG: print(f'maxrss_delta: {maxrss_delta}\t{prettyMemory(maxrss_delta)}')
    
    if DEBUG: print(f'pid: {pid}')
    if DEBUG: print(f'current rss from \'ps -o rss= {pid}\': {current_rss}')
    
    
    print(f'\nPrimary key type: {datasetName}\t\te.g. {example_row}')
    print(f'{prettyTime(time_delta)} to insert {n_entries:,} entries')
    print(f'memory used (to store DB): {prettyMemory(current_rss)}')
    