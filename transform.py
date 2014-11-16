def transform_scraped_data(map_from_team_to_player_game_stats):
    STATS = ['3P', '3P%', 'PTS', 'TRB', 'AST', 'MP']

    result = {}
    for stat in STATS:
        result[stat] = {}
    print map_from_team_to_player_game_stats
    for team_name, team_players in map_from_team_to_player_game_stats:
        for player_name, player_games in team_players:
            for game in player_games:
                for stat_name, stat_value in game:
                    if not result[team]:
                        result[team] = {} # dict team => stat
                    if not result[team][stat_name]:
                        result[team][stat_name] = {} # dict stat => name
                    if not result[team][stat_name][player]: 
                        result[team][stat_name][player] = [] # list of stat values

                    result[team][stat_name][player] += stat_value 
    return result

scraped_data = pickle.load(open("nba_player_data.pickle", "rb"))
transform_scraped_data(scraped_data)
