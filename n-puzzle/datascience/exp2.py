import pickle as pkl
from data_processing import *


# this is literally the same as exp1.py except the inputs are changed
# INPUTS
experiment_no = 2
timeout_min = pd.NA
input_filename_prefix = 'data/Experiment 2 (80 15-puzzles)/'
input_filenames = [
    '80_ida_h2_.json',
    '80_ida_h3___08-26-2021_07-12-59PM.json',
    
    '80_ida-R_h3___08-26-2021_07-13-50PM.json',
]

dict_of_dataframes = {}

for filename in input_filenames:
    df = processJsonToDataframe(experiment_no, timeout_min, input_filename_prefix, filename)

    df_nickname = df['algo'][1].replace('*', '') + '_' + df['heuristic'][1]  # e.g. 'A_h1'
    dict_of_dataframes[df_nickname] = df.copy()
  
with open(f'exp{experiment_no}/exp{experiment_no}_dict_of_dataframes.pkl', 'wb') as f:
    pkl.dump(dict_of_dataframes, f, protocol=0)

print('\ndict name:\tdict_of_dataframes')
print(dict_of_dataframes.keys())

# load dict of DFs from pkl file:
# with open('{FILENAME}.pkl', 'rb') as f:
    # a = pkl.load(f)
    # print(a.keys())


# to "flatten" dict into single df:
data = pd.DataFrame()
for k in dict_of_dataframes.keys():
    data = data.append(dict_of_dataframes[k])
    print(data.info())

df = data  # alternate name

# from pandasgui import show
# show(data)

with open(f'exp{experiment_no}/exp{experiment_no}_all.pkl', 'wb') as f:
    data.to_pickle(f)


# load pickled Pandas DataFrame:
# with open(f'exp{experiment_no}_all.pkl', 'rb') as f:
#     data = pd.read_pickle(f)
#     print(data.info())

