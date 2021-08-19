from collections import namedtuple
import numpy as np
import pandas as pd
import re

# to be able to import from get_heuristic_value
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from get_heuristic_value import get_h_value


def calcEffectiveBranchingFactor(df, row_index):
        # calculating effective branching factor (b*)
        # formula:  N = (b*)^1 + (b*)^2 + ... + (b*)^d
        # solve for b*
        # values needed: N = nodes generated, d = max depth

        # 1. get N and d  (for entry i)
        d = df['search depth'][row_index]
        N = df['nodes gen'][row_index]

        # 2. construct numpy coefficient array
        # docs: https://numpy.org/doc/stable/reference/generated/numpy.roots.html#numpy.roots
        coeff = [1] * d
        coeff.append(-1 * N)

        # 3. get roots
        
        roots = np.roots(coeff)

        # 4. extract real, positive root
        mask = np.logical_and(np.isreal(roots), roots > 1)
        bstar = float(roots[mask][0])   # hopefully there is only one!

        return np.around(bstar, 2)

def calcHeuristicPercentError(df, row_index):
    i = row_index
    percent_error = np.abs( df['h val'][i] - df['sol length'][i] ) / df['sol length'][i] * 100
    return np.around(percent_error, 1)


HeuristicNames = namedtuple('HeuristicNames', ['solverpy', 'fordataframe', 'desc'])
heuristics = {
    'h1': HeuristicNames(solverpy='hamming', fordataframe='hamming', desc='misplaced tiles'),
    'h2': HeuristicNames('manhattan', 'manhattan', desc=None),
    'h3': HeuristicNames('linearconflicts', 'mhd+linear conflicts', desc='MHD + linear conflicts')
}


def processJsonToDataframe(experiment_no, timeout_min, input_file_prefix, input_filename):

    df = pd.read_json(input_file_prefix+input_filename)
    df = df.transpose()

    del df['foundSol']
    del df['timedOut']

    df = df.rename(columns={
        'algo': 'algo',
        'init': 'puzzle',
        'goal': 'goal',
        'max_path_len': 'search depth',
        'nodes_gen': 'nodes gen',
        'runtime_sec': 'runtime (sec)',
        'sol_len': 'sol length',
        })

    # populate new fields
    df.insert(0, "exp", [experiment_no] * len(df), False)
    df.insert(1, "N", [len(eval(df.loc[1, 'puzzle']))-1] * len(df), False)    # N = 8, 15, etc..
    heuristic_code = re.search('_(h\d)_', input_filename).group(1)
    df.insert(2, 'heuristic', [heuristic_code] * len(df), False)
    df.insert(3, 'timeout (min)', [timeout_min] * len(df), False)
    df['time (nodes)'] = df['nodes gen']
    df['space (nodes)'] = df['nodes gen'].where(df['algo'] == 'A*', df['search depth'])
    df['h val'] = list(map(lambda puz: get_h_value(heuristics[heuristic_code].solverpy, puz), df['puzzle'].to_list() ))


    # convert sol length = -1 to null (for ability to easily query % non-null)
    df['sol length'] = df['sol length'].where(df['sol length'] > 0, pd.NA)

    # round runtimes
    df['runtime (sec)'] = [np.around(df['runtime (sec)'][i], 1) for i in range(1, len(df)+1)]
    
    # calculate effective branching factor (b*)
    df['b*'] = [ calcEffectiveBranchingFactor(df, i) for i in range(1, len(df)+1) ]

    # calculate heuristic % error
    df['h % error'] = [ calcHeuristicPercentError(df, i) for i in range(1, len(df)+1) ]

    cols = {
        'exp': 'Int64',
        'algo': 'string',
        'heuristic': 'string',
        'h val': 'Int64',
        'sol length': 'Int64',
        'h % error': 'Float64',
        'timeout (min)': 'Int64',
        'runtime (sec)': 'Float64',
        'time (nodes)': 'Int64',
        'space (nodes)': 'Int64',
        'b*': 'Float64',
        'nodes gen': 'Int64', 
        'search depth': 'Int64',
        'puzzle': 'string',
        'N': 'Int64',
        'goal': 'string',
    }

    # re-order columns
    df = df[list(cols.keys())]

    # set column data types
    df = df.astype(cols)

    # display max columns 
    pd.set_option('display.max_columns', None)
    print(df)
    print(df.info())

    return df

