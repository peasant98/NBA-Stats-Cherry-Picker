# file with function to randomly select user from all of the data, all of the games
import ast
import csv
import numpy as np
import pandas as pd
import sys

from nba_api.stats.static import players

# some fun little work to get a random player
def get_random_player(file_name):
    def need_s(num):
        return 's' if num!=1 else ''
    csv.field_size_limit(sys.maxsize)
    # the rows are really long!
    res = pd.read_csv(file_name, header=None)
    r = np.random.randint(0, len(res.values))
    arr = ast.literal_eval(res.values[r][1])
    player = players.find_player_by_id(res.values[r][0])['full_name']
    print(f'{player} selected.')
    r_idx = np.random.randint(0, len(arr))
    game = arr[r_idx]
    x = f'On {game[0]}, {player} scored {game[-1]} point{need_s(game[-1])}, dished out '\
        f'{game[16]} assist{need_s(game[16])}, grabbed {game[15]} rebound{need_s(game[15])}, '\
        f'had {game[17]} steal{need_s(game[17])}, and had {game[18]} block{need_s(game[18])}.'
    print(x)
    return player, arr