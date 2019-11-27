from nba_api.stats.endpoints import playergamelog

m = playergamelog.PlayerGameLog(2544, season='2012-13')
print(m.player_game_log.data)
with open('document.csv','a') as fd:
    fd.write('ff')
# "SEASON_ID", 0
# "Player_ID",
# "Game_ID",
# "GAME_DATE", 3
# "MATCHUP", 4
# "WL",
# "MIN", 6
# "FGM",
# "FGA",
# "FG_PCT",
# "FG3M",
# "FG3A",
# "FG3_PCT",
# "FTM",
# "FTA",
# "FT_PCT",
# "OREB",
# "DREB",
# "REB",
# "AST",
# "STL",
# "BLK",
# "TOV",
# "PF",
# "PTS",
# "PLUS_MINUS",
# "VIDEO_AVAILABLE"