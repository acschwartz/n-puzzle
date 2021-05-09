#!/usr/bin/env python3

from os import remove as os_remove

from pdbgen_bytes import *
doNotImport = ['generatePDB', 'generateChildren', 'handle_exception']
for name in doNotImport:
	del globals()[name]

##==============================================================================================##
	
def handle_exception(exc_type, exc_value, exc_traceback):
# Source: https://stackoverflow.com/questions/6234405/logging-uncaught-exceptions-in-python
	if issubclass(exc_type, KeyboardInterrupt):
		sys.__excepthook__(exc_type, exc_value, exc_traceback)
		return
	
	logger.critical("\nUncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
	logger.info('\n')
	
sys.excepthook = handle_exception

##==============================================================================================##
OUTPUT_PATH = None

def initOutputPath(subdir):
	initDirectory(OUTPUT_DIRECTORY)
	global OUTPUT_PATH
	if '/' not in subdir:
		subdir += '/'
	OUTPUT_PATH = f'{OUTPUT_DIRECTORY}{subdir}'
	initDirectory(OUTPUT_PATH)
	return OUTPUT_PATH

##==============================================================================================##
#	 G E N E R A T E   P A T T E R N   D A T A B A S E
##==============================================================================================##

def generatePDBs(initNode, dim, num_ptiles, moveSet, oppMoves, t_start, logger, output_path=OUTPUT_PATH):
	queue = deque([initNode])
	frontier = set()
	frontier.add(initNode[:num_ptiles])
	
	visited = list(map((lambda i: {}), range(dim*dim)))
	visitedCount = 0
	'''
	The visited set is split into sub-databases indexed by the location of the 0-tile in the puzzle
	i.e. 
	visited[0] = the dictionary which contains entries for patterns that start with \x00 ...
	visited[15] = the dictionary which contains entries for patterns that start with \x0f ...
	'''
	
	try:
		# Generate Pattern Database using breadth-first search "backwards" from goal state.
		while queue:
			node = queue.popleft()
			state_repr = node[:num_ptiles]
			state_info = node[num_ptiles:]
			bucket = state_repr[0]
			
			for child_state, child_info in generateChildrenOptimized(state_repr, state_info, dim, moveSet, oppMoves):
				if (child_state not in visited[bucket]) and (child_state not in frontier):
					queue.append(child_state+child_info)
					frontier.add(child_state)
					
			visited[bucket][state_repr] = bytes([state_info[0]])
			visitedCount += 1
			frontier.remove(state_repr)
			
			#DEBUG
#			if visitedCount == 10000:
##				import pprint
##				pprint.pp(visited, indent=1)
#				break
			
			if visitedCount % 10000 == 0:
				print("Entries collected:", visitedCount)
				
	except KeyboardInterrupt as e:
			# TODO : This could be handled better
			logger.info('\nKeyboardInterrupt: Aborted search. No database files created.')
			return visitedCount
	

	logger.info(f'Entries collected: {visitedCount}')
	t_finished_generating_entries = perf_counter()
	t_delta = t_finished_generating_entries - t_start
	
	_ = writeDBfiles(output_path, visited, visitedCount)
	
	logger.info(f'\n{SECTION_SEPARATOR}')
	logger.info(f'Generated {visitedCount} entries in {sec_to_hours(t_delta)}')
					
	return visitedCount



def writeDBfiles(output_path, visited, visitedCount):
	
	n_bucket = 0	# not pythonic but seems to be a time/space savings, and need all optimizations
	for bucket in visited:
		filename = f'pdb_{n_bucket:0>2d}_of{len(visited)-1}'
		outfile = f'{output_path}{filename}'
		bucketSize = len(bucket)
		
		logger.info(f'\nBUCKET {n_bucket}: writing entries to file {filename} .....')
		logger.info(f'Bucket size: {bucketSize} entries')

		Retry = True
		while Retry is True:
			try:
				f = open(outfile, "wb")
				pickle.dump(visited, f, pickle.HIGHEST_PROTOCOL)
				
				
				#DEBUG:
#				import time
#				time.sleep(2)
#				if n_bucket == 5:
#					raise OSError
				
				logger.info('Done!')
				f.close()
				Retry = False
			except (OSError, KeyboardInterrupt) as err:
				f.close()
				logger.exception(err)
				os_remove(outfile)
				logger.info(f'Deleting file {outfile}')
				
				maxrss = rawMaxRSStoPrettyString(getMaxRSS())
				logger.debug(f'Maxrss: {maxrss}. can check current actual memory usage in terminal\n')
				
				Retry = input('\nRetry? type N to abort, or any other key to retry  ')
				if Retry != 'N':
					logger.info('\nRetrying ....')
					Retry = True
				else:
					logger.info('User aborted.')
					Retry = False
					return False
			
			if not Retry:
				visited[n_bucket] = None 	# hopefully this would free up memory?
				n_bucket += 1
				

##==============================================================================================##
#		M	A 	I	N
##==============================================================================================##
if __name__ == '__main__':
	pname, ptiles, dim, pdb_id = initVars()
	output_path = initOutputPath(pdb_id)
	logger, logfile = initLogger(__name__, pdb_id, output_path)
	logger.debug(f'Output directory: {output_path}')
	printHeader(logger, pdb_id, pname)
	
	t_start = perf_counter()
	maxrss_start = getMaxRSS()
	
	db_len = generatePDBs(generateInitialNode(ptiles), dim, len(ptiles), MOVES, OPP_MOVES, t_start, logger, output_path)
	
	# TODO: update generateStats.... screws up timing since it keeps counting during pauses, etc
	stats = generateStats(t_start, maxrss_start, db_len)
	printStats(logger, stats, title="Overall Stats")
	# VERY END:
	logger.debug(f'logfile: {logfile}')