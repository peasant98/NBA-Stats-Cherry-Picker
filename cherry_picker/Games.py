# NBA Stats Cherry Picker
# Copyright Matthew Strong, 2019

import numpy as np
import pandas as pd
import csv

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
        v1 = int(non_legend_len / 4) + 1
        v2 = int(legend_len / 4) + 1
        split_non_legend_ids = np.array_split(no_hall_of_fame, v1)
        split_legend_ids = np.array_split(hall_of_fame, v2)

        manager = Manager()
        non_legends_dict = manager.dict()
        legends_dict = manager.dict()
        self.players_process(split_non_legend_ids, non_legends_dict)
        self.players_process(split_legend_ids, legends_dict)
        # print(legends_dict)
        # print(non_legends_dict)
        self.nl_dict = non_legends_dict
        self.l_dict = legends_dict
        with open('non_legends_dict.csv', 'w', newline="") as csv_file: 
            writer = csv.writer(csv_file)
            for key, value in non_legends_dict.items():
                writer.writerow([key, value])
        # set what happens to legends_dict after!
        with open('legends_dict.csv', 'w', newline="") as csv_file: 
            writer = csv.writer(csv_file)
            for key, value in legends_dict.items():
                writer.writerow([key, value])

    def get_season(self, player_id, dictionary):
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        arr = list(career.get_data_frames()[0]['SEASON_ID'].values)
        name = players.find_player_by_id(player_id)['full_name']
        # print the name, because who cares about id?
        print(f'{name} processed.')
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


class PlayerSeasonCSVCreator():
    def __init__(self, file_path, legends_file_path, is_csv_loaded):
        if not is_csv_loaded:
            # given file path to ids and top players, get all of the players
            # legends in separate arrays
            all_players = np.loadtxt(file_path, dtype=int)
            all_legends = np.loadtxt(legends_file_path, dtype=int)

            non_legends = np.array(list(set(all_players) - set(all_legends)))
            # get all seasons
            ps = PlayerSeasons(non_legends, all_legends)
            self.nl = ps.nl_dict
            self.l = ps.l_dict
        else:
            pcg = PlayerCSVGetter(file_path, legends_file_path)
            self.nl = pcg.nl_dict
            self.l = pcg.l_dict

class PlayerCSVGetter():
    def __init__(self, non_legend_csv, legend_csv):
        with open(non_legend_csv) as csv_file:
            reader = csv.reader(csv_file)
            mydict = dict(reader)
            for key in mydict:
                res = (mydict[key].strip('][').split(' '))
                m = [eval(r) if r!='' else '' for r in res]
                mydict[key] = m
            self.nl_dict = mydict
            
        with open(legend_csv) as csv_file:
            reader = csv.reader(csv_file)
            mydict = dict(reader)
            for key in mydict:
                res = (mydict[key].strip('][').split(' '))
                m = [eval(r) if r!='' else '' for r in res]
                mydict[key] = m
            self.l_dict = mydict

class PlayerGameLog():
    def __init__(self, nl, l):
        # given all of the seasons, find all of the years
        # two dictionaries
        # non-legends passthrough
        # max rows is 82 games * 22 seasons 
        m = 82 * 22
        n = 22 # indices 3 to 25
        manager = Manager()
        nl_games_dict = manager.dict()
        l_games_dict = manager.dict()
        arr = Array('d', m*n)
        self.player_process(nl, nl_games_dict, 'all_players.csv')
        self.player_process(l, l_games_dict, 'legend_players.csv')

        # since previous is blocking, add to csv file here to prevent mem error
        
        # each player: go through all of the seasons, make requests there,
        # throw into file, every game ever from every player
        
        # store key stats from each game in list?

    def player_process(self, seasons_dict, season_games_dict, file_path):
        
        player_keys = np.array(list(seasons_dict.keys()))
        v1 = int(len(player_keys) / 4) + 1

        split_players = np.array_split(player_keys, v1)
        for split in split_players:
            # each group of player ids
            jobs = []
            for p_id in split:
                # create some jobs
                # new process for ALL of players' seasons
                season_games_dict[p_id] = []
                p = Process(target=self.get_every_game_season, args=(p_id, seasons_dict, season_games_dict))
                jobs.append(p)
                p.start()
            for j in jobs:
                j.join()
            with open(file_path, 'a', newline="") as csv_file: 
                writer = csv.writer(csv_file)
                for key, value in season_games_dict.items():
                    writer.writerow([key, value])
            for p_id in split:
                season_games_dict.pop(p_id)
            # multiple processes are spawned in the context of one player with multiple seasons.

    def get_every_game_season(self, player_id, season_dict, season_games_dict):
        # go through every season for a player, get all of the games
        # each year
        name = players.find_player_by_id(player_id)['full_name']
        res = []
        for year in season_dict[player_id]:
            
            player_season = playergamelog.PlayerGameLog(player_id, season=year)
            # lock temporary array
            print(f'{name} - {year}')
            # make it two-dimensional
            if player_season.player_game_log.data['data'] != []:
                # played some time
                # all games in a season
                for game in player_season.player_game_log.data['data']:
                    temp = []
                    for i in range(3,25):
                        temp.append(game[i])
                    res.append(temp)

        player_dict = {player_id: res}
        season_games_dict.update(player_dict)
        
        # print the name, because who cares about id?
        print(f'{name} processed.')
        # played some games
        # format [[x1...], [x2...]...[xn...]]

        # get important stats

v = PlayerSeasonCSVCreator('non_legends_dict.csv', 'legends_dict.csv', True)
# v.l - legends' seasons
# v.nl - non-legends' seasons
PlayerGameLog(v.nl, v.l)
print('done')
