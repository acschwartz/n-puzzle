import pandas as pd

inputFilename = 'data/Experiment 1 (100 8-puzzles)/8puz_AStar_h1___May12-2021_02-37-50PM.json'


df = pd.read_json(inputFilename)
df = df.transpose()
# transposing because pd dataframe format in JSON is:
# {'col1': {'row1': ..., 'row2': ...}, 'col2': {'row1': ..., 'row2': ... }}



# puzzle  algo  heuristic  'h val'  'solution length'  'timed out?'  'timeout (min)'  'runtime (sec)'  'nodes generated'  'search depth'  'time complexity (nodes)'  'space complexity (nodes)' 

'''
if algo == 'A*':
    time complexity = nodes generated
    space complexity = nodes generated
else:  # IDA* family
    time complexity = nodes generated
    space complexity = search depth
'''

del df['foundSol']
df = df.rename(columns={
    'algo': 'Algo',
    'init': 'Puzzle',
    'goal': 'Goal',
    'max_path_len': 'Search depth',
    'nodes_gen': 'Nodes generated',
    'runtime_sec': 'Runtime (sec)',
    'sol_len': 'Solution length',
    'timedOut': 'Timed out?'
    })

df = df.rename(columns={
    'algo': 'algo',
    'init': 'puzzle',
    'goal': 'goal',
    'max_path_len': 'search depth',
    'nodes_gen': 'nodes generated',
    'runtime_sec': 'runtime (sec)',
    'sol_len': 'solution length',
    'timedOut': 'timed out?'
    })

heuristicNames = {
    'perfect': 'perfect',
    'h1': 'hamming',  # misplaced tiles
    'h2': 'manhattan',
    'h3': 'MHD + linear conflicts',  # manhattan + linear conflicts
}

class DFBuilder:
    def __init__(self, filename, heuristic, timeout_min, experiment=None, n_puzzle=None):
