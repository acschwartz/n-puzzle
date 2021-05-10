#!/usr/bin/env python3
import sqlite3

def initDB(db_file=None):
	if not db_file:
		con = sqlite3.connect(':memory:')
	else:
		con = sqlite3.connect(db_file)
		
	cur = con.cursor()
	return con, cur


def createTables(cur, n_tables, base_name='PatternCosts_EmptyTileLocation_'):
	tablenames = []
	for n in range(0, n_tables):
		tablename = f'{base_name}{n}'
#		TODO: add logging
#		if DEBUG: print(f'\nCreating table {tablename}  ({n+1} of {n_tables}) ...')
		cur.execute('''
		CREATE TABLE %s(
			pattern BLOB PRIMARY KEY,
			cost INTEGER
			) WITHOUT ROWID;
		'''%tablename)
		#		TODO: add logging
#		if DEBUG: print('Success!')
		tablenames.append(tablename)
	return tablenames


def insert(cur, table, pattern, cost):
	cur.execute("""INSERT INTO %s(pattern, cost) 
						VALUES (?,?);"""%table, (pattern, cost))

def checkRowExists(cur, tablename, value, attribute='pattern'):
	# gonna assume the table and attribute exist, etc
	cur.execute("SELECT EXISTS ( SELECT * from %s where %s = ?)"%(tablename, attribute), (value,))
	exists = cur.fetchone()[0]
	return bool(exists)