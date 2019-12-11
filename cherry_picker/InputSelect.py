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
['AST','REB','STL','TOV','BLK'],['PTS','AST','REB','STL','TOV','BLK']]

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

def n_games_inputter(player_games_vec, games_info, name, file_name, single_game_threshold):
    # player_games_vec is n x 6 matrix
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
        inputter(df, player_game_dict, games_info, name, single_game_threshold)
        return
    # worry about 1 game here??
    player_careers = df.groupby('ID')
    for subset in STATS_POWER_SET:
        # each subset, get the slice of game
        amt = 0
        for m in player_careers:
            # m[1] is the dataframe associated with the player
            player_df = m[1]
            for g in player_df.groupby(player_df.index // n):
                # every n games of player's career
                n_games_df = g[1]
                x = subset_iter(subset, n_games_df, player_game_dict)
                if len(n_games_df.loc[x]) == n:
                    amt+=1
                    best_name = n_games_df.loc[x]['Name'].values[0]
                    best_date = n_games_df.loc[x]['Date'].values[0]
        if amt == 0:
            res = construct_string(subset, player_game_dict['PTS'], player_game_dict['AST'],
                                    player_game_dict['REB'], player_game_dict['STL'],
                                    player_game_dict['BLK'], player_game_dict['TOV'])
            print(f'{name} is the first player EVER {res} in {n} straight games.')
            print('')

        elif amt == 1:

            res = construct_string(subset, player_game_dict['PTS'], player_game_dict['AST'],
                                    player_game_dict['REB'], player_game_dict['STL'],
                                    player_game_dict['BLK'], player_game_dict['TOV'])
            print(f'{name} is the first player since {best_name} on {best_date} {res} in {n} straight games.')
            print('')

            # name = player_df['Name'].values[0]
            # print(f'{name} processed.')

def construct_string(subset: list, p, a, r, s, b, t):
    str_arr = np.zeros(6).astype(str)
    str_arr[0] = f'to score at least {p} points' if 'PTS' in subset else ''
    str_arr[1] = f'to dish out at least {a} assists' if 'AST' in subset else ''
    str_arr[2] = f'to snag at least {r} rebounds' if 'REB' in subset else ''
    str_arr[3] = f'to have at least {s} steals' if 'STL' in subset else ''
    str_arr[4] = f'to register at least {b} blocks' if 'BLK' in subset else ''
    str_arr[5] = f'to have at most {t} turnovers' if 'TOV' in subset else ''
    if len(subset) == 1:
        res = ''
        for s in str_arr:
            res += s
        return res
    elif len(subset) == 2:
        res = ''
        cnt = 0
        for s in str_arr:
            if s != '':
                if cnt==1:
                    res+=('and ' + s)
                    return res
                else:
                    res+=(s + ' ')
                    cnt+=1
    else:
        res = ''
        cnt = 0
        for s in str_arr:
            if s != '':
                if cnt==len(subset)-1:
                    res+=('and ' + s)
                    return res
                else:
                    res+=(s + ', ')
                    cnt+=1
 
    # return 


def string_list(names_list, dates_list, games_list):
    if len(names_list) == 1:
        return f'{names_list[0]} on {dates_list[0]} in the game {games_list[0]}'
    elif len(names_list) == 2:
        return f'{names_list[0]} on {dates_list[0]} in the game {games_list[0]} and {names_list[1]} on {dates_list[1]} in the game {games_list[1]}'
    else:
        # more than 2 names
        player_string = ''
        for ind,val in enumerate(names_list):
            if ind == len(names_list) - 1:
                player_string += (f'and {val} on {dates_list[-1]} in the game {games_list[-1]}')
                break
            player_string += (val+ ' on ' + dates_list[ind] + ' in the game '+ games_list[ind] + ', ')
        return player_string


def inputter(df, player_game_dict, game_info, name, single_game_threshold):
    # given a players stats vector
    # consists of pts, ast, reb, stl
    # try combinations of different entries
    # look throught the powerset for interesting values
    
    for subset in STATS_POWER_SET:
        x = subset_iter(subset, df, player_game_dict)
        game_amt = len(df.loc[x])
        if game_amt == 0:
            res = construct_string(subset, player_game_dict['PTS'], player_game_dict['AST'],
                                    player_game_dict['REB'], player_game_dict['STL'],
                                    player_game_dict['BLK'], player_game_dict['TOV'])
            print(f'{name} in {game_info} is the first player EVER {res}.')
            print('')
        elif game_amt <= single_game_threshold:
            res = construct_string(subset, player_game_dict['PTS'], player_game_dict['AST'],
                                    player_game_dict['REB'], player_game_dict['STL'],
                                    player_game_dict['BLK'], player_game_dict['TOV'])
            other_names = string_list(df.loc[x]['Name'].values, df.loc[x]['Date'].values,
                                    df.loc[x]['Team'].values)
            res_string = f'{name} in {game_info} is the first player since ' \
                        f'{other_names} {res}.'
            print(res_string)
            print('')

        
            

# game = np.array([[40,11,9,4,1,1]])
# n_games_inputter(game, 'LAL vs MIN, DEC 09 2019', 'Anthony Davis', 'filtered_legends.csv')
# arr = np.array([[39, 2, 9, 2, 3, 1], [50, 6, 7, 4, 1, 1]])

