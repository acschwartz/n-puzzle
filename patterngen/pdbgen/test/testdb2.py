#!/usr/bin/env python3

import sqlite3
import pprint
import os
import subprocess
from argparse import ArgumentParser
from time import perf_counter
from helpers.memorytools import *
from helpers.timetools import *

#import sys
# I did #sys.path.insert(0, '..')
# and not gonna lie idk if that persisted or what lol :/

#print(sys.path[0])
#exit()

##==============================================================================================##
# FAV SQLITE TUTORIAL:   https://docs.python.org/3/library/sqlite3.html
##==============================================================================================##


def parseArgs():
    parser = ArgumentParser()
    parser.add_argument( '-n', dest='n_entries', action = 'store', type = int, help = 'number of entries', default=10**6)
    parser.add_argument( '-ntables', dest='n_tables', action = 'store', type = int, help = 'number of tables', default=16)
    parser.add_argument( '-d', dest='debug', action = 'store_true', help = 'debug mode (prints more stuff)')
    parser.add_argument( '-p', '-persist', dest='persist', action = 'store_true', help = 'save DB to hard drive')
    args = parser.parse_args()
    return args.n_entries, args.n_tables, args.debug, args.persist

    
##==============================================================================================##
def createTables(cur, n_tables, base_name='PatternCosts'):
    tablenames = []
    for n in range(0, n_tables):
        tablename = f'{base_name}{n}'
        if DEBUG: print(f'\nCreating table {tablename}  ({n+1} of {n_tables}) ...')
        cur.execute('''
        CREATE TABLE %s(
            pattern BLOB PRIMARY KEY,
            cost INTEGER
            ) WITHOUT ROWID;
        '''%tablename)
        if DEBUG: print('Success!')
        tablenames.append(tablename)
    return tablenames


def checkExists(cur, tablename, value, attribute='pattern'):
    # gonna assume the table and attribute exist, etc
    res = cur.execute("SELECT EXISTS ( SELECT * from %s where %s = ?)"%(tablename, attribute), (value,))
    exists = res.fetchone()[0]
    return bool(exists)



def populateTableWithBinaryBlobs(cur, tablename, n_entries, len_blob=4, max_cost=100, max_bytevalue=255):
## e.g. 'b'\x00\x03\x07\x0b\x0c\r\x0e\x0f'' representing (0, 3, 7, 9, 11, 12, 13, 14, 15)
    from random import randint
    
    if DEBUG: print(f'\nPopulating table: {tablename} ...')
    
    first_key = bytes([0]*len_blob)
    key_mutable = [0]*len(first_key)
    
    NUM_ENTRIES = 0
    while True:
        for i in range(len(first_key)):
            if NUM_ENTRIES > n_entries:
                if DEBUG: print(f'Inserted {(NUM_ENTRIES-1):,} into {tablename}\n')
                return #NUM_ENTRIES
            key_mutable[i] = randint(0, max_bytevalue)
            next_key = bytes(key_mutable)
            if checkExists(cur, tablename, next_key):
                continue
            else:
                NUM_ENTRIES += 1
                cost = NUM_ENTRIES % max_cost
                cur.execute("""INSERT INTO %s(pattern, cost) 
                                    VALUES (?,?);"""%tablename, (next_key, cost))

def getSplits(dividend, divisor):
# e.g. getSplits(1000,3) returns [334, 333, 333]
    if not divisor: return None
    splits = [dividend//divisor] * divisor
    splits[0] += dividend % divisor
    return splits

##==============================================================================================##

if __name__ == '__main__':
    n_entries, n_tables, DEBUG, persist = parseArgs()
    pid = os.getpid()
    
    if persist:
        con = sqlite3.connect('testdb2.db')
    else:
        con = sqlite3.connect(':memory:')

    cur = con.cursor()
    
    maxrss_start = getMaxRSS()
    time_start = perf_counter()
    
    tables = createTables(cur, n_tables)
    if DEBUG: print(f'\nTable names: {tables}')
    
    splits = getSplits(n_entries, n_tables)
    for n, table in enumerate(tables):
        populateTableWithBinaryBlobs(cur, table, splits[n])
    
    
    time_delta = timeDelta(time_start)
    maxrss_after_populate_table = getMaxRSS()
    maxrss_delta = maxrss_after_populate_table - maxrss_start
    maxrss_delta_pretty = prettyMemory(maxrss_delta)
    current_rss = getRSS()
    

    res = cur.execute("SELECT * from %s LIMIT 1"%tables[0])
    for row in res:
        example_row = row
#        
#    if DEBUG:
#        i = input('press p if you want to see the table (SELECT * from patterncosts) ')
#        if i == 'p':
#            res = cur.execute("SELECT * from patterncosts")
#            for row in res:
#                print(row)
#                
    if DEBUG: print(f'maxrss_start: {maxrss_start}\t{prettyMemory(maxrss_start)}')
    if DEBUG: print(f'maxrss_after_populate_table: {maxrss_after_populate_table}\t{prettyMemory(maxrss_after_populate_table)}')
    if DEBUG: print(f'maxrss_delta: {maxrss_delta}\t{prettyMemory(maxrss_delta)}')
    
    if DEBUG: print(f'current rss (after populating tables into memory):\t{current_rss}\t{prettyMemory(current_rss)}')
    
    
    print(f'\nPrimary key type: Binary blob\t\te.g. {example_row}')
    print(f'Number of tables: {n_tables}')
    print(f'{prettyTime(time_delta)} to insert {n_entries:,} entries')
    print(f'DB size: {prettyMemory(maxrss_delta)}')
    
    con.commit()
    con.close()
    