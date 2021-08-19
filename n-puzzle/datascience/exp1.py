import pickle as pkl
from data_processing import *



# INPUTS
experiment_no = 1
timeout_min = pd.NA
input_filename_prefix = 'data/Experiment 1 (100 8-puzzles)/'
input_filenames = [
    '8puz_AStar_h1___May12-2021_02-37-50PM.json',
    '8puz_AStar_h2___May12-2021_02-38-57PM.json',
    '8puz_AStar_h3___May12-2021_02-39-18PM.json',
    '8puz_IDA-R_h1___May12-2021_02-54-58PM.json',
    '8puz_IDA-R_h2___May12-2021_02-57-21PM.json',
    '8puz_IDA-R_h3___May12-2021_02-57-44PM.json',
    '8puz_IDA_h1___May12-2021_02-46-49PM.json',
    '8puz_IDA_h2___May12-2021_02-49-36PM.json',
    '8puz_IDA_h3___May12-2021_02-50-13PM.json'
]

exp1 = {}

for filename in input_filenames:
    df = processJsonToDataframe(experiment_no, timeout_min, input_filename_prefix, filename)

    df_nickname = df['algo'][1].replace('*', '') + '_' + df['heuristic'][1]  # e.g. 'A_h1'
    exp1[df_nickname] = df.copy()
  
with open(f'exp{experiment_no}.pkl', 'wb') as f:
    pkl.dump(exp1, f, protocol=0)

print('\ndict name:\texp1')
print(exp1.keys())

# to "flatten" dict into single df:for k in data.keys():
# exp1_all = pd.DataFrame()
# for k in exp1.keys():
#     exp1_all = exp1_all.append(exp1[k])

# from pandasgui import show
# show(exp1_all)