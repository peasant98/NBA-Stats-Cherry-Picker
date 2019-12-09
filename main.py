# NBA Stats Cherry Picker
# Copyright Matthew Strong, 2019

import numpy as np
import argparse

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
    
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--legends_path", type=str, default='docs/legends.txt', help="path to NBA legends file")
    opt = parser.parse_args()
    file_path = opt.legends_path
    # get all of the ids and put in text files
    get_legends(file_path)
    get_all_players()
    all_players = players.get_players()
    # game = ()
    
