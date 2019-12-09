# allow user to input a player's data, and compare that to the history of all nba players
import numpy as np
import pandas as pd

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



def subset_iter(subset, df, player_game_dict):
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
    return x

def n_games_inputter(player_games_vec, games_info, file_name):
    # player_games_vec is n x 6 matrix
    # index by n
    if len(np.array(player_games_vec)) == 1:
        pass
    n = len(player_games_vec)
    game_thresh_arr = np.zeros(6)
    for i in range(6):
        game_thresh_arr[i] = min(player_games_vec[::,i])
    # 
    player_game_dict = {'PTS': game_thresh_arr[0], 'AST': game_thresh_arr[1],
                        'REB': game_thresh_arr[2], 'STL': game_thresh_arr[3],
                        'BLK': game_thresh_arr[4], 'TOV': game_thresh_arr[5] }

    df = pd.read_csv(file_name)
    if n == 1:
        # only 1 game
        inputter(df, player_game_dict, games_info)
        return
    # worry about 1 game here??
    player_careers = df.groupby('ID')
    for subset in STATS_POWER_SET:
        # each subset, get the slice of game
        for m in player_careers:
            # m[1] is the dataframe associated with the player
            player_df = m[1]
            for g in player_df.groupby(player_df.index // n):
                # every n games of player's career
                n_games_df = g[1]
                x = subset_iter(subset, n_games_df, player_game_dict)
                if len(n_games_df.loc[x]) == n:
                    print(subset)
                    print(n_games_df.loc[x])
            name = player_df['Name'].values[0]
            print(f'{name} processed.')
 
def inputter(df, player_game_dict, game_info):
    # given a players stats vector
    # consists of pts, ast, reb, stl
    # try combinations of different entries
    # look throught the powerset for interesting values
    
    for subset in STATS_POWER_SET:
        x = subset_iter(subset, df, player_game_dict)
        print(subset)
        print(f'{len(df.loc[x])} games found.')
        print(df.loc[x])

game = np.array([[50,6,7,4,1,1]])
n_games_inputter(game, 'Game', 'filtered_legends.csv')
# arr = np.array([[39, 2, 9, 2, 3, 1], [50, 6, 7, 4, 1, 1]])
# n_games_inputter(arr, 'Game', 'filtered_legends.csv')
# n_games_inputter(arr, 'Game', 'filtered_players.csv')

