#!/usr/bin/env python3
import sqlite3

def initDB(logger, db_file=None):
	if not db_file:
		db_file = ':memory:'
	else:
		db_file = ''.join([db_file, '.db'])
	
	con = sqlite3.connect(db_file)
	
	logger.debug(f'Opened connection with database: {db_file}')
	return con, db_file


def createTables(con, n_tables, logger, base_name='PatternCosts_EmptyTileLocation_'):
	cur = con.cursor()
	tablenames = []
	for n in range(0, n_tables):
		tablename = f'{base_name}{n}'
		logger.debug(f'\nCreating table {tablename}  ({n+1} of {n_tables}) ...')
		cur.execute('''
		CREATE TABLE %s(
			pattern BLOB PRIMARY KEY,
			cost INTEGER NOT NULL
			) WITHOUT ROWID;
		'''%tablename)
		logger.debug('Success!')
		tablenames.append(tablename)
	return tablenames


def insert(con, table, pattern, cost):
	cur = con.cursor()
	cur.execute("""INSERT INTO %s(pattern, cost) 
						VALUES (?,?);"""%table, (pattern, cost))


def checkRowExists(con, tablename, value, attribute='pattern'):
	# gonna assume the table and attribute exist, etc
	cur = con.cursor()
	cur.execute("SELECT EXISTS ( SELECT * from %s where %s = ?)"%(tablename, attribute), (value,))
	exists = cur.fetchone()[0]
	return bool(exists)