# NBA Stats Cherry Picker

'FirstName' 'LastName' is the first player since 'Good Player'  in 'year' to record 'x' points, 'y' assists, 'z' rebounds and 'n' steals.

With the awesome NBA Stats API!

Requires `python3.6` or above, so make sure to have that.

## Data

The best data from can be found [here](https://nba-data-bucket.s3-us-west-2.amazonaws.com/filtered_players.csv). Also checkout [here](https://nba-data-bucket.s3-us-west-2.amazonaws.com/filtered_legends.csv) for a csv of some greats out there. This data is a csv with the following columns: `,Name,ID,Date,Team,PTS,AST,REB,STL,BLK,TOV`

For users not wanting to go through the whole process of getting all of the data again (this takes a long time), we recommend using the above data, which you should put 

There is a different dataset available (but beware, missing data from the way older years, such as Wilt Chamberlains's time) online [here](https://nba-data-bucket.s3-us-west-2.amazonaws.com/all_players.csv). This dataset is harder to work with than the previous one, and it is highly
recommended to use the former one.

`player_id,"[game_1, game_2 ... game_n]`, where `player_id` is an integer of the player's unique id (according to stats.nba.com), `n` denotes **every** game played in **every** season they played. Each `game_i` is a list that consists of the following:

`[GAME_DATE, MATCHUP, WL, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT,
        FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV,
        PF, PTS`]

## Easy Run

## Usage

Given that you have all of the necessary Python packages installed,
We need to first analyze `main.py` to understand how to work with the code.

- 
