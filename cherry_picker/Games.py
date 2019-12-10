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

# get all data from every game from every player!

# player seasons class to grab all active seasons for a player
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
        self.nl_dict = non_legends_dict
        self.l_dict = legends_dict
        # write to dictionary csv files to get gamelogs later
        with open('non_legends_dict.csv', 'w', newline="") as csv_file: 
            writer = csv.writer(csv_file)
            for key, value in non_legends_dict.items():
                writer.writerow([key, value])
        with open('legends_dict.csv', 'w', newline="") as csv_file: 
            writer = csv.writer(csv_file)
            for key, value in legends_dict.items():
                writer.writerow([key, value])

    def get_season(self, player_id, dictionary):
        # get the seasons that player_id played
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        # get all of the seasons a player played in
        arr = list(career.get_data_frames()[0]['SEASON_ID'].values)
        name = players.find_player_by_id(player_id)['full_name']
        # print the name for a measure of the speed of this program.
        print(f'{name} processed.')
        player_dict = {player_id: arr}
        # update the dictionary in shared memory
        dictionary.update(player_dict)

    def players_process(self, arr, dictionary):
        for split in arr:
            jobs = []
            for player_id in split:
                # get each season
                p = Process(target=self.get_season, args=(player_id, dictionary))
                jobs.append(p)
                p.start()
            for j in jobs:
                j.join()

# csv creator class depending on if the csv is already loaded on the computer
# serves to grab all of the seasons that players played in
class PlayerSeasonCSVCreator():
    def __init__(self, file_path, legends_file_path, is_csv_loaded):
        '''
        file_path need to be the txt file if not loaded, otherwise needs to 
        be csv file. Same for legends_file_path.
        '''
        if not is_csv_loaded:
            # given file path to ids and top players, get all of the players
            # legends in separate arrays
            all_players = np.loadtxt(file_path, dtype=int)
            all_legends = np.loadtxt(legends_file_path, dtype=int)

            non_legends = np.array(list(set(all_players) - set(all_legends)))
            # get all seasons from players
            ps = PlayerSeasons(non_legends, all_legends)
            # corresponding dictionares for normal players and legends
            self.nl = ps.nl_dict
            self.l = ps.l_dict
        else:
            # if you already loaded the csv files, will be used later
            pcg = PlayerCSVGetter(file_path, legends_file_path)
            self.nl = pcg.nl_dict
            self.l = pcg.l_dict

class PlayerCSVGetter():
    def __init__(self, non_legend_csv, legend_csv):
        '''
        In the case that the csvs for the seasons that the players played
        in exists, get the dictionaries again.
        '''
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

# player game log class for getting all of the season data for each season.
class PlayerGameLog():
    def __init__(self, nl, l):
        '''
        Requires the non-legends and legends dictionaries in memory
        in order to run properly.
        '''
        # given all of the seasons, find all of the years
        # two dictionaries
        # non-legends passthrough
        # max rows is 82 games * 22 seasons 
        m = 82 * 22
        n = 22 # indices 3 to 25
        manager = Manager()
        nl_games_dict = manager.dict()
        l_games_dict = manager.dict()
        # shared array for data from the processes
        arr = Array('d', m*n)
        # all_players and legend_players is csv file
        self.player_process(nl, nl_games_dict, 'all_players.csv')
        self.player_process(l, l_games_dict, 'legend_players.csv')


    def player_process(self, seasons_dict, season_games_dict, file_path):
        '''
        gets all of the game data from the seasons 
        '''
        player_keys = np.array(list(seasons_dict.keys()))
        v1 = int(len(player_keys) / 4) + 1

        split_players = np.array_split(player_keys, v1)
        for split in split_players:
            # each group of player ids
            jobs = []
            for p_id in split:
                # create many jobs as the size of each split, in this case, 4
                # new process for ALL of players' seasons
                season_games_dict[p_id] = []
                p = Process(target=self.get_every_game_season, args=(p_id, seasons_dict, season_games_dict))
                jobs.append(p)
                p.start()
            for j in jobs:
                j.join()
            # instead of writing to file at the end (and overloading memory), 
            # write as each group of processes finish to the end of the file
            with open(file_path, 'a', newline="") as csv_file: 
                writer = csv.writer(csv_file)
                for key, value in season_games_dict.items():
                    writer.writerow([key, value])
            for p_id in split:
                # reset dictionary to save memory and for next batch of processes
                season_games_dict.pop(p_id)
            # multiple processes are spawned in the context of one player with multiple seasons.

    def get_every_game_season(self, player_id, season_dict, season_games_dict):
        # go through every season for a player, get all of the games
        name = players.find_player_by_id(player_id)['full_name']
        res = []
        for year in season_dict[player_id]:
            # http request is made here
            player_season = playergamelog.PlayerGameLog(player_id, season=year)
            print(f'{name} - {year}')
            # ignore empty data
            if player_season.player_game_log.data['data'] != []:
                # played some time
                # all games in a season
                for game in player_season.player_game_log.data['data']:
                    temp = []
                    for i in range(3,25):
                        # indices 3 to 25 give the important stats
                        temp.append(game[i])
                    res.append(temp)

        player_dict = {player_id: res}
        season_games_dict.update(player_dict)
        # update shared dictionary
        
        print(f'{name} processed.')
