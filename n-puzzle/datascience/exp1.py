from collections import namedtuple
import numpy as np
import pandas as pd

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

        return bstar


to_process = [
    {
        'experiment': 1,
        'timeout (min)': None,

        'file': 'data/Experiment 1 (100 8-puzzles)/8puz_AStar_h1___May12-2021_02-37-50PM.json',
        'h': 'h1',
    },
]


HeuristicInfo = namedtuple('HeuristicNames', ['solverpy', 'fordataframe', 'desc'])
heuristics = {
    'h1': HeuristicInfo(solverpy='hamming', fordataframe='hamming', desc='misplaced tiles'),
    'h2': HeuristicInfo('manhattan', 'manhattan', desc=None),
    'h3': HeuristicInfo('linearconflicts', 'MHD + linear conflicts', desc='MHD + linear conflicts')
}


for metadata in to_process:
    df = pd.read_json(metadata['file'])
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
    df.insert(0, "exp", [metadata['experiment']] * len(df), False)
    df.insert(1, "N", [len(eval(df.loc[1, 'puzzle']))-1] * len(df), False)    # N = 8, 15, etc..
    df.insert(2, 'heuristic', [heuristics[metadata['h']].fordataframe] * len(df), False)
    df.insert(3, 'timeout (min)', [metadata['timeout (min)']] * len(df), False)
    df['time (nodes)'] = df['nodes gen']
    df['space (nodes)'] = df['nodes gen'].where(df['algo'] == 'A*', df['search depth'])
    df['h val'] = list(map(lambda puz: get_h_value(heuristics[metadata['h']].solverpy, puz), df['puzzle'].to_list() ))

    
    # calculate effective branching factor
    list_nodesgen = df['nodes gen'].to_list()
    list_depth = df['search depth'].to_list()

    list_bstar = [] # effective branching factor
    for i in range(1, len(df)+1):
        list_bstar.append(calcEffectiveBranchingFactor(df, i))
    
    df['b*'] = list_bstar


    # re-order cols
    column_order = [
        'exp',
        'N',
        'algo',
        'heuristic',
        'h val',
        'sol length',
        'timeout (min)',   # TODO: not sure where this goes
        'runtime (sec)',
        'time (nodes)',
        'space (nodes)',
        'b*',
        'nodes gen', 
        'search depth',
        'puzzle',
        'goal',             # TODO: not sure where this goes
    ]
    df = df[column_order]

    # display max columns 
    pd.set_option('display.max_columns', None)
    print(df)
    
    


    
