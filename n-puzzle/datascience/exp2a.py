import pickle as pkl
from data_processing import *


# EXPERIMENT NO2 - first set of inputs (20), IDA only. (no R)
experiment_no = 2
timeout_min = 9
input_filename_prefix = 'data/Exp 2 (20 15-puzzles, t9)/'
input_filenames = [

'10korf_IDA__h1___May13-2021_11-09-49PM.json',
'10MOREkorf_IDA_h1___May12-2021_05-07-13PM.json',

'10korf_IDA_h2___May12-2021_04-00-11PM.json',
'10MOREkorf_IDA_h2___May12-2021_05-02-23PM.json',

'10korf_IDA_h3___May12-2021_03-51-17PM.json',
'10MOREkorf_IDA_h3___May12-2021_05-03-36PM.json',

# '10korf_IDA-R_h1___May12-2021_03-55-22PM.json',

# '10korf_IDA-R_h2___May12-2021_03-55-51PM.json',
# '10MOREkorf_IDA-R_h2___May12-2021_05-04-31PM.json',

# '10korf_IDA-R_h3___May12-2021_03-56-18PM.json',
]

exp2a = {}

for filename in input_filenames:
    df = processJsonToDataframe(experiment_no, timeout_min, input_filename_prefix, filename)

    df_nickname = df['algo'][1].replace('*', '') + '_' + df['heuristic'][1]  # e.g. 'A_h1'

    try:
        exp2a[df_nickname] # check if entry already exists
        exp2a[df_nickname] = exp2a[df_nickname].append(df)
    except KeyError:
        exp2a[df_nickname] = df.copy()
    
  
with open(f'exp2a.pkl', 'wb') as f:
    pkl.dump(exp2a, f, protocol=0)

print('\ndict name:\texp2a')
print(exp2a.keys())