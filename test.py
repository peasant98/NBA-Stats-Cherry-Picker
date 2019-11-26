from nba_api.stats.endpoints import commonplayerinfo

# Basic Request
player_info = commonplayerinfo.CommonPlayerInfo(player_id=2544)
print(player_info)



from nba_api.stats.endpoints import playercareerstats
# Anthony Davis
career = playercareerstats.PlayerCareerStats(player_id=2544)
print(career.get_data_frames()[0])

