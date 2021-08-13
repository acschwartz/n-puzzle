from collections import namedtuple
import pandas as pd

from get_heuristic_value import get_h_value


experiment = 1

inputFilename = 'data/Experiment 1 (100 8-puzzles)/8puz_AStar_h1___May12-2021_02-37-50PM.json'
df = pd.read_json(inputFilename)
df = df.transpose()


del df['foundSol']

df = df.rename(columns={
    'algo': 'algo',
    'init': 'puzzle',
    'goal': 'goal',
    'max_path_len': 'search depth',
    'nodes_gen': 'nodes generated',
    'runtime_sec': 'runtime (sec)',
    'sol_len': 'sol length',
    'timedOut': 'timed out?'
    })

df.insert(0, "exp", [experiment]*len(df), False)
df.insert(1, "N", [len(eval(df.loc[1, 'puzzle']))-1]*len(df), False)    # N = 8, 15, etc..


# puzzle  algo  heuristic  'h val'  'sol length'  'timed out?'  'timeout (min)'  'runtime (sec)'  'nodes generated'  'search depth'  'time complexity (nodes)'  'space complexity (nodes)' 

'''
if algo == 'A*':
    time complexity = nodes generated
    space complexity = nodes generated
else:  # IDA* family
    time complexity = nodes generated
    space complexity = search depth
'''



HeuristicNames = namedtuple('HeuristicNames', ['fn', 'solverpy', 'dataframe', 'desc'])
h = [
    None,
    HeuristicNames('h1', solverpy='hamming', dataframe='hamming', desc='misplaced tiles'),
    HeuristicNames('h2', 'manhattan', 'manhattan', desc=None),
    HeuristicNames('h3', 'linearconflicts', 'MHD + linear conflicts', desc='MHD + linear conflicts')
]

# class DFBuilder:
#     def __init__(self, filename, heuristic, timeout_min, experiment=None, n_puzzle=None):
