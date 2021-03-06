# NBA Stats Cherry Picker
# Copyright Matthew Strong, 2019

import numpy as np
import argparse
import os.path

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
import data_engine
    
def get_id(val):
    return val['id']

def get_player_id(line):
    res = players.find_players_by_full_name(line.rstrip('\n'))[0]['id']
    return res

def get_legends(path):
    # gets legends from text file
    file = open(path, "r")
    ids = np.array(list(map(get_player_id, file)))[:100]
    np.savetxt('docs/legend_ids.txt', ids, fmt='%d')

def get_all_players():
    all_player_ids = np.array(list(map(get_id, players.get_players())))
    np.savetxt('docs/player_ids.txt', all_player_ids, fmt='%d')

def try_input_number(str, default_num, optional_string=None):
    try:
        num = int(input(str))
        return num
    except:
        if optional_string != None:
            print(optional_string)
        return default_num


if __name__ == '__main__':
    if not (os.path.isfile('docs/player_ids.txt') and os.path.isfile('docs/legend_ids.txt')):
    
        parser = argparse.ArgumentParser()
        parser.add_argument("--legends_path", type=str, default='docs/legends.txt', help="path to NBA legends file")
        opt = parser.parse_args()
        file_path = opt.legends_path
        # get all of the ids and put in text files
        # legend_ids.txt
        get_legends(file_path)
        # player_ids.txtu
        get_all_players()
    data_engine.create_data(is_seasons_created=True, is_gamelogs_created=True,
                            include_legends_with_players=True, is_analysis_df_created=True)
    
    g = try_input_number('Number of Games: ', 1, 'Selecting 1 game')
    games = np.zeros((g, 6))
    for i in range(g):
        p = try_input_number('Points: ', 20)
        a = try_input_number('Assists: ', 6)
        r = try_input_number('Rebounds: ', 7)
        s = try_input_number('Steals: ', 2)
        b = try_input_number('Blocks: ', 1)
        t = try_input_number('Turnovers: ', 3)
        games[i] = np.array([p,a,r,s,b,t])
    name = str(input('Enter player name: '))
    game_info = str(input('Enter game info: '))
    # game = np.array([[50,6,7,4,1,1]])
    data_engine.run_analysis(games, game_info, name,
                                'filtered_legends.csv', 'filtered_players.csv', single_game_threshold=4)
    # data time
        
