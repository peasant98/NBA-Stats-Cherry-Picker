import numpy as np
import nba_api
import cherry_picker.Games as CPGames
import cherry_picker.CreateDF as CPCreateDF
import cherry_picker.InputSelect as CPInputSelect


def create_data(is_seasons_created, is_gamelogs_created=False):
    # purely to create files, no analysis here.
    v = None
    if not is_seasons_created:
        # create the data of player seasons. Will take some time
        v = CPGames.PlayerSeasonCSVCreator('docs/player_ids.txt', 'docs/legend_ids.txt', False)
    else:
        v = CPGames.PlayerSeasonCSVCreator('non_legends_dict.csv', 'legends_dict.csv', True)
    
    if not is_gamelogs_created:
        CPGames.PlayerGameLog(v.nl, v.l)
        # check if gamelogs are created, if not, create em
        # this will take a LONG time
        # a long time later, these two functions will execute
        CPCreateDF.get_filtered_player_df('all_players.csv', False)
        CPCreateDF.get_filtered_player_df('legend_players.csv', True)

def run_analysis(player_games_vec, games_info, name, legends_file_name, players_file_name):
    CPInputSelect.n_games_inputter(player_games_vec, games_info, name, legends_file_name)
    CPInputSelect.n_games_inputter(player_games_vec, games_info, name, players_file_name)

