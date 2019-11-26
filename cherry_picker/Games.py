# NBA Stats Cherry Picker
# Copyright Matthew Strong, 2019

import numpy as np
import pandas as pd

from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playerdashboardbyyearoveryear

from nba_api.stats.static import players
from multiprocessing import Process, Value, Array, Manager

# games log endpoint from stats.nba.com

# get all data from every game from every player

class PlayerSeasons():
    def __init__(self, no_hall_of_fame, hall_of_fame):
        # two np arrays, non legends, and legends, as previously specified by user.
        # go through each array of ids, needs to be sparse, use dictionary instead
        non_legend_len = len(no_hall_of_fame)
        legend_len = len(hall_of_fame)
        # break  up into chunks
        v1 = int(non_legend_len / 15) + 1
        v2 = int(legend_len / 15) + 1
        split_non_legend_ids = np.array_split(no_hall_of_fame, v1)
        split_legend_ids = np.array_split(hall_of_fame, v2)

        manager = Manager()
        non_legends_dict = manager.dict()
        legends_dict = manager.dict()
        self.players_process(split_non_legend_ids, non_legends_dict)
        self.players_process(split_legend_ids, legends_dict)
        self.non_legends_dict = non_legends_dict
        self.legends_dict = legends_dict
        print(legends_dict)
        print(non_legends_dict)
        # set what happens to legends_dict after!

    def get_season(self, player_id, dictionary):
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        arr = career.get_data_frames()[0]['SEASON_ID'].values
        print(f'{player_id} processed.')
        player_dict = {player_id: arr}
        dictionary.update(player_dict)

    def players_process(self, arr, dictionary):
        for split in arr:
            jobs = []
            for player_id in split:
                # get important stats from each year
                p = Process(target=self.get_season, args=(player_id, dictionary))
                jobs.append(p)
                p.start()
            for j in jobs:
                j.join()


class PlayerGameLogs():
    def __init__(self, file_path, legends_file_path):
        # given file path to ids and top players, get all of the players
        # legends in separate arrays
        all_players = np.loadtxt(file_path, dtype=int)
        all_legends = np.loadtxt(legends_file_path, dtype=int)

        non_legends = np.array(list(set(all_players) - set(all_legends)))
        # get all seasons
        ps = PlayerSeasons(non_legends, all_legends)


m = PlayerGameLogs('docs/player_ids.txt', 'docs/legend_ids.txt')






# N_VAL = 12

# # get data for specific season from every player out of active players today who was active.
# def get_id_from_players_list(entry):
#     return entry['id']

# def place_player(ind, player_id, year, arr, m, n):
#     player_year = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id=player_id,
#                                             season=year)
#     with arr.get_lock():
#         print(f'{player_id} found.')
#         np_arr = np.frombuffer(arr.get_obj()) # mp_arr and arr share the same memory
#         # make it two-dimensional
#         b = np_arr.reshape((m,n))
#         if player_year.overall_player_dashboard.data['data'] != []:
#             player_season = player_year.overall_player_dashboard.data['data'][0]
#             # season is available from active player
#             # games played
#             b[ind, 0] = player_id
#             num = np.array([5,29,22,21,24,25,23,18,12,15,17])
#             # gp, pts, ast, reb, stl, blk, tov, ft_pct, fg_pct, fg3_pct, fta
#             for i,val in enumerate(num):
#                 b[ind, i+1] = player_season[val]

# def get_season_data(year, debug=True):
#     n = N_VAL
#     all_players = players.get_active_players()
#     # ids of all active players
#     ids = np.array(list(map(get_id_from_players_list, all_players)))
#     m = len(ids)
#     jobs = []
#     v = int(m / 15) + 1
#     split_ids = np.array_split(ids, v)
#     arr = Array('d', m*n)
#     np_arr = np.frombuffer(arr.get_obj())
#     ind = 0
#     for split in split_ids:
#         jobs = []
#         for player_id in split:
#             # get important stats from each year
#             p = Process(target=place_player, args=(ind, player_id, year, arr, m, n))
#             jobs.append(p)
#             p.start()
#             ind+=1
#         for j in jobs:
#             j.join()
#     b = np_arr.reshape((m,n))
#     # from m x n matrix b, construct dataframe
#     # m rows - each person
#     columns = np.array(['PlayerID','GP','PTS','AST','REB','STL','BLK','TOV',
#                 'FT_PCT', 'FG_PCT', 'FG3_PCT', 'FTA'])
#     # gp, pts, ast, reb, stl, blk, tov, ft_pct, fg_pct, fg3_pct, fta
#     df = pd.DataFrame(b, columns=columns)
#     to_int = ['PlayerID', 'GP', 'PTS', 'AST', 'REB', 'STL', 'BLK', 'TOV']
#     df[to_int] = df[to_int].astype(int)
#     df_filtered = df[df['GP'] > 0] 
#     if debug:
#         print(df_filtered)
#     # also export to csv
#     df_filtered.to_csv(f'{year}_nba_players.csv')
#     return df_filtered
