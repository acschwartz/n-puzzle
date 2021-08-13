from collections import namedtuple
import pandas as pd

import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from get_heuristic_value import get_h_value


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
        'puzzle',
        'goal',             # TODO: not sure where this goes
        'nodes gen', 
        'search depth',
    ]

    df = df[column_order]