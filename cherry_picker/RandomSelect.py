# file with function to randomly select user from all of the data, all of the games
import ast
import csv
import numpy as np
import pandas as pd
import sys

from nba_api.stats.static import players

def get_random_player(file_name, legends=False):
    csv.field_size_limit(sys.maxsize)
    # the rows are really long!
    res = pd.read_csv(file_name, header=None)
    r = np.random.randint(0, len(res.values))
    arr = ast.literal_eval(res.values[r][1])
    player = players.find_player_by_id(res.values[r][0])['full_name']
    print(f'{player} selected.')
    r_idx = np.random.randint(0, len(arr))
    print(arr[r_idx])
    return player, arr

def get_players(file_name, legends=False):
    csv.field_size_limit(sys.maxsize)
    res = pd.read_csv(file_name, header=None)
    # print(ast.literal_eval(res.values[0][1]))
    for v in res.values:
        arr = ast.literal_eval(v[1])


player, arr = get_random_player('legend_players.csv', True)
# print(arr)