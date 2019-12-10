import numpy as np
import nba_api
import cherry_picker.Games as CPGames
import cherry_picker.CreateDF as CPCreateDF
import cherry_picker.InputSelect as CPInputSelect


def create_data(is_seasons_created, is_analysis_df_created=False, 
                is_gamelogs_created=False, include_legends_with_players=False):
    # purely to create files, no analysis here.
    v = None
    if not is_seasons_created:
        # create the data of player seasons. Will take some time
        v = CPGames.PlayerSeasonCSVCreator('docs/player_ids.txt', 'docs/legend_ids.txt', False,
                                            include_legends_with_players=include_legends_with_players)
        CPGames.PlayerGameLog(v.nl, v.l)

    elif ((is_seasons_created) and (not is_gamelogs_created)):
        # dictionaries already created
        v = CPGames.PlayerSeasonCSVCreator('non_legends_dict.csv', 'legends_dict.csv', True)
        CPGames.PlayerGameLog(v.nl, v.l)
        # check if gamelogs are created, if not, create em
        # this will take a LONG time
        # a long time later, these two functions will execute
        
    if not is_analysis_df_created:
        # create the main dataframe to be used for analysis
        CPCreateDF.get_filtered_player_df('all_players.csv', False)
        CPCreateDF.get_filtered_player_df('legend_players.csv', True)

def run_analysis(player_games_vec, games_info, name, legends_file_name, players_file_name=None):
    
    print('----- Comparing to select legends -----')
    print()
    CPInputSelect.n_games_inputter(player_games_vec, games_info, name, legends_file_name)
    if players_file_name != None:
        print()
        print('----- Comparing to all players -----')
        print()
        CPInputSelect.n_games_inputter(player_games_vec, games_info, name, players_file_name)

