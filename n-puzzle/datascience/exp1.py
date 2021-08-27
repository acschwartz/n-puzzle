import pickle as pkl
from data_processing import *



# INPUTS
experiment_no = 1
timeout_min = pd.NA
input_filename_prefix = 'data/Experiment 1 (500 8-puzzles)/'
input_filenames = [
    '500_astar_h1___08-20-2021_08-48-56PM.json', 
    '500_astar_h2___08-20-2021_08-49-46PM.json', 
    '500_astar_h3___08-20-2021_08-50-01PM.json',

    '500_ida_h1___08-20-2021_08-50-19PM.json',
    '500_ida_h2___08-20-2021_08-50-48PM.json',
    '500_ida_h3___08-20-2021_08-51-11PM.json',
    
    '500_ida-R_h1___08-20-2021_08-51-49PM.json', 
    '500_ida-R_h2___08-20-2021_08-52-30PM.json', 
    '500_ida-R_h3___08-20-2021_08-52-43PM.json',   
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

