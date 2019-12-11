# NBA Stats Cherry Picker

'FirstName' 'LastName' is the first player since 'Good Player'  in 'year' to record 'x' points, 'y' assists, 'z' rebounds and 'n' steals.

With the awesome NBA Stats API!

Requires `python3.6` or above, so make sure to have that.

## Data

There is a dataset available (but beware, missing data from the way older years, such as Wilt Chamberlains's time) online [here](https://nba-data-bucket.s3-us-west-2.amazonaws.com/all_players.csv). This dataset contains every registered game from every player to play in the NBA.

You can use this csv with a separate project as well, and is also recommended.
The format is that each row is of the form

`player_id,"[game_1, game_2 ... game_n]`, where `player_id` is an integer of the player's unique id (according to stats.nba.com), `n` denotes **every** game played in **every** season they played. Each `game_i` is a list that consists of the following:

`[GAME_DATE, MATCHUP, WL, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT,
        FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV,
        PF, PTS`]


## Usage
