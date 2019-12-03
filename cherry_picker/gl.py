from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playercareerstats


m = playergamelog.PlayerGameLog('7', season='2012-13')
career = playercareerstats.PlayerCareerStats(player_id='7')
player_season = playergamelog.PlayerGameLog('7', season='1985-86')
print(player_season.player_game_log.data['data'] == [])
print(m.player_game_log.data['data'])
with open('document.csv','a') as fd:
    fd.write('ff')
