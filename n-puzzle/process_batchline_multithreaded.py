import multiprocessing as mp
from solver import solver

# logging functionality removed to enable multithreading
def process_batchline_multithreaded(line, argslist):
    argsThisRun = argslist.copy()
    argsThisRun.append('-ints')
    puzzle = line.split()
    argsThisRun.extend(puzzle)
    
    outcome = solver(argsThisRun)

    if outcome: 
        success, logheader, resultSet = outcome

    else:
        success = None
        logheader = None
        resultSet = None

    return resultSet