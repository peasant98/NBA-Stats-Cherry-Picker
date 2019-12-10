import ast
import csv
import numpy as np
import pandas as pd
import sys

from nba_api.stats.static import players

# the work for getting the dataframe of vectors from the dataframe.
# take the massive csvs
def get_filtered_player_df(file_name, is_legends=False):
    csv.field_size_limit(sys.maxsize)
    res = pd.read_csv(file_name, header=None)
    all_games = []
    keep_indices = [0, 1, -1, 16, 15, 17, 18, 19]
    for player_id, career in zip(res[0], res[1]):
        player = players.find_player_by_id(player_id)['full_name']
        print(f'{player} selected.')
        career_arc = ast.literal_eval(career)
        for game in career_arc:
            # in this case,
            temp = [game[i] for i in keep_indices]
            temp.insert(0, player_id)
            temp.insert(0, player)

            all_games.append(temp)
            # each python list of each game
    filtered_player_df = pd.DataFrame(all_games, columns=['Name', 'ID', 'Date', 'Team', 
                                                        'PTS', 'AST', 'REB', 'STL', 'BLK',
                                                        'TOV'])
    filtered_player_df.to_csv('filtered_legends.csv') if is_legends else filtered_player_df.to_csv('filtered_players.csv')
