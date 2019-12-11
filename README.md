# NBA Stats Cherry Picker

'FirstName' 'LastName' is the first player since 'Good Player'  in 'year' to record 'x' points, 'y' assists, 'z' rebounds and 'n' steals.

With the awesome NBA Stats API!

Requires `python3.6` or above, so make sure to have that.

## Data

The best data from can be found [here](https://nba-data-bucket.s3-us-west-2.amazonaws.com/filtered_players.csv). Also checkout [here](https://nba-data-bucket.s3-us-west-2.amazonaws.com/filtered_legends.csv) for a csv of some greats out there. This data is a csv with the following columns: `,Name,ID,Date,Team,PTS,AST,REB,STL,BLK,TOV`

For users not wanting to go through the whole process of getting all of the data again (this takes a long time), we recommend using the above data.

There is a different dataset available (but beware, missing data from the way older years, such as Wilt Chamberlains's time) online [here](https://nba-data-bucket.s3-us-west-2.amazonaws.com/all_players.csv). This dataset is harder to work with than the previous one, and it is highly recommended to use the former one.

`player_id,"[game_1, game_2 ... game_n]`, where `player_id` is an integer of the player's unique id (according to stats.nba.com), `n` denotes **every** game played in **every** season they played. Each `game_i` is a list that consists of the following:

`[GAME_DATE, MATCHUP, WL, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT,
        FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV,
        PF, PTS`]

## Easy Run

- `git clone https://github.com/peasant98/NBA-Stats-Cherry-Picker`
- `cd NBA-Stats-Cherry-Picker`
- Getting the data
- `wget https://nba-data-bucket.s3-us-west-2.amazonaws.com/filtered_players.csv`
- `wget https://nba-data-bucket.s3-us-west-2.amazonaws.com/filtered_legends.csv`
- `python3.6 main.py`
- Follow the instructions to see what shakes loose!

## Usage

If you want to have some more power of controlling the Cherry Picker interface:
We need to first analyze `main.py` to understand how to work with the code.

If the files `'docs/legend_ids.txt'` and `'docs/players_ids.txt'` do not exist, you will
be prompted for `--legends_path`, which is the path to a file of great players. There is a default option, and the code will take care of writing to the files for the player and legends ids.

The line `data_engine.create_data(is_seasons_created=True, is_gamelogs_created=True,
                            include_legends_with_players=True, is_analysis_df_created=True)`
creates data if `is_seasons_created` is False (the csv for all of the players' active seasons), `is_gamelogs_created` is False (every game for every player, ever), or `is_analysis_df_created` is False (the df and csv that was the first download link on this readme). The argument `include_legends_with_players` will toss the legends into the massive csv file with the players. Feel free to change this as you see fit. It is currently setup for the steps in Easy Run.

The other line to worry about is `data_engine.run_analysis(games, game_info, name,
                                'filtered_legends.csv', 'filtered_players.csv', single_game_threshold=4)`
In this case, `single_game_threshold` means that we display every cherry picked stat subset if 4 games or less include that stat. If this argument is too high, then some of the results don't look at impressive because 10+ games have had this certain, ultra-specific, statline.

## Cool Fact
Stay tuned for interesting posts on real players as the 2019-20 NBA season progresses!

1. Anthony Davis in LAL vs. MIN is the first player EVER to score at least 50.0 points, to dish out at least 6.0 assists, to snag at least 7.0 rebounds, to have at least 4.0 steals, to register at least 1.0 block, and to have at most 1.0 turnover.


## Misc

If you went about the steps in usage to generate `all_players.csv` and `legend_players.csv`, run `python3.6 random_stat_generator.py` just for some random games generation!

Enjoy!!!
