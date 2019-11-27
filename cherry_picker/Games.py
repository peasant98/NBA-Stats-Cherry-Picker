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
        for p_id in nl:
            for year in nl[p_id]:
                pass
            # each player: go through all of the seasons, make requests there,
            # throw into file, every game ever from every player
        # legends passthrough
        for p_id in l:
            # create multiprocesses here
            jobs = []
            for year in l[p_id]:
                pass
                # store key stats from each game in list?
    
    def get_every_game_season(self, player_id, year):
        pass

v = PlayerSeasonCSVCreator('non_legends_dict.csv', 'legends_dict.csv', True)
# v.l - legends' seasons
# v.nl - non-legends' seasons