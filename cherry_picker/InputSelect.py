# allow user to input a player's data, and compare that to the history of all nba players
import numpy as np
import pandas as pd
import time

STATS_POWER_SET = [['PTS'],['AST'],['REB'],['STL'],['TOV'],['BLK'],['PTS','AST'],
['PTS','REB'],['PTS','STL'],['PTS','TOV'],['PTS','BLK'],['AST','REB'],['AST','STL'],
['AST','TOV'],['AST','BLK'],['REB','STL'],['REB','TOV'],['REB','BLK'],['STL','TOV'],
['STL','BLK'],['TOV','BLK'],['PTS','AST','REB'],['PTS','AST','STL'],['PTS','AST','TOV'],
['PTS','AST','BLK'],['PTS','REB','STL'],['PTS','REB','TOV'],['PTS','REB','BLK'],
['PTS','STL','TOV'],['PTS','STL','BLK'],['PTS','TOV','BLK'],['AST','REB','STL'],
['AST','REB','TOV'],['AST','REB','BLK'],['AST','STL','TOV'],['AST','STL','BLK'],
['AST','TOV','BLK'],['REB','STL','TOV'],['REB','STL','BLK'],['REB','TOV','BLK'],
['STL','TOV','BLK'],['PTS','AST','REB','STL'],['PTS','AST','REB','TOV'],
['PTS','AST','REB','BLK'],['PTS','AST','STL','TOV'],['PTS','AST','STL','BLK'],
['PTS','AST','TOV','BLK'],['PTS','REB','STL','TOV'],['PTS','REB','STL','BLK'],
['PTS','REB','TOV','BLK'],['PTS','STL','TOV','BLK'],['AST','REB','STL','TOV'],
['AST','REB','STL','BLK'],['AST','REB','TOV','BLK'],['AST','STL','TOV','BLK'],
['REB','STL','TOV','BLK'],['PTS','AST','REB','STL','TOV'],['PTS','AST','REB','STL','BLK'],
['PTS','AST','REB','TOV','BLK'],['PTS','AST','STL','TOV','BLK'],['PTS','REB','STL','TOV','BLK'],
['AST','REB','STL','TOV','BLK'],['PTS','AST','REB','STL','TOV','BLK'] ]

def inputter(player_game_dict, game_info, file_name):
    # given a players stats vector
    # consists of pts, ast, reb, stl
    df = pd.read_csv(file_name)
    # try combinations of different entries
    # look throught the powerset for interesting values
    for subset in STATS_POWER_SET:
        init = False
        x = None
        for i in range(len(subset)):
            stat_name = subset[i]
            if not init:
                if stat_name == 'TOV':
                    x = (df[stat_name] <= player_game_dict[stat_name])
                else:
                    x = (df[stat_name] >= player_game_dict[stat_name])
                init = True
            else:
                if stat_name == 'TOV':
                    x = x & (df[stat_name] <= player_game_dict[stat_name])
                else:
                    x = x & (df[stat_name] >= player_game_dict[stat_name])
        print(subset)
        print(f'{len(df.loc[x])} games found.')
        print(df.loc[x])
    # entries = df[df['PTS'] > player_vec[0]]
    # calculate if there is any way we can make the player look good.
    # go through dataframe, apply filters to find if player is THAT good

def read_all_players_csv(file_name, is_legend=False):
    df = pd.read_csv(file_name)
    print(df[['PTS', 'AST']])
    x = (df['PTS'] > 20) &  (df['AST'] >= 10) & (df['REB'] >= 10)
    print(df.loc[x])
    print(STATS_POWER_SET)

    # medataframe of players every game

# read_all_players_csv('filtered_players.csv'
game = {'PTS': 34, 'AST':5, 'REB': 11, 'TOV':2, 'BLK':0, 'STL':1}
inputter(game, 'Game', 'filtered_players.csv')


