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
    game = np.array([[50,6,7,4,1,1]])
    data_engine.run_analysis(game, 'LAL vs. MIN, DEC 08 2019', 'Anthony Davis',
                                'filtered_legends.csv', 'filtered_players.csv', single_game_threshold=4)
    # data time
        
