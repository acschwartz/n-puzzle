#!/usr/bin/env python3
#from time import perf_counter
import sqlite3
from npuzzle.pdb.eightpuzzle.full8puzzle import full8puzzle
from npuzzle.pdb.eightpuzzle.subprof15 import subprof15


def initDB(pdbtype):
#    print(f'_____ calling initDB_____')
    info = PDBINFO[pdbtype]
    dbfile = info['dbfile']
    connection = sqlite3.connect(dbfile)    
    return connection


def queryPDB(tablename, pattern, connection):
    if connection is None:
        return None
    cur = connection.cursor()
    cur.execute("SELECT * from %s where pattern = ?"%(tablename), (pattern,))
    return cur.fetchone()[1]





PDBINFO = {
    'full8puzzle': full8puzzle.PUZZLE_INFO,
    '8SubPrOf15': subprof15.PUZZLE_INFO,
#    '15fringe': {
#            'file':     'npuzzle/pdb/15puzzle/4732363__15fringe_database.pickle',
#            'size':        4,
#            'goal_state': 'zero_first',
#            'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
#            'empty tile': 0,
#        },
#    'max15fringeLC':{
#            'file':     'npuzzle/pdb/15puzzle/4732363__15fringe_database.pickle',
#            'size':        4,
#            'goal_state': 'zero_first',
#            'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
#            'empty tile': 0,
#        },
}
