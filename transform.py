import sys
from scraper import deserialize_record_adhoc

def deserialize_data(datafile):
    alldata = {} # this is map_from_team_to_player_game_stats
    for line in open(datafile).readlines():
        team_name, player_name, player_table = deserialize_record_adhoc(line)
        if not alldata.get(team_name, None):
            alldata[team_name] = {} # hash to hold statistic names
        alldata[team_name][player_name] = player_table

    return alldata

def transform_scraped_data(map_from_team_to_player_game_stats):
    STATS = ['3P', '3P%', 'PTS', 'TRB', 'AST', 'MP', 'FG%']

    result = {}
    for stat in STATS:
        result[stat] = {}
    for team_name in map_from_team_to_player_game_stats:
        team_players = map_from_team_to_player_game_stats[team_name]

        for player_name in team_players:
            player_games = team_players[player_name]

            for game in player_games:
                for stat_name in game:
                    stat_value = game[stat_name]

                    if not result.get(team_name, None):
                        result[team_name] = {} # dict team => stat
                    if not result[team_name].get(stat_name, None):
                        result[team_name][stat_name] = {} # dict stat => name
                    if not result[team_name][stat_name].get(player_name, None): 
                        result[team_name][stat_name][player_name] = [] # list of stat values

                    result[team_name][stat_name][player_name].append(stat_value) 
    return result

# csv with 
# team
# stat
# games: 1 2 3 ...
# playername: statvalue1 statvalue2 ...
def print_csv(transformed_data):
    for team in transformed_data:
        print(team)
        stats = transformed_data[team]
        for stat in stats:
            print(stat)
            for player in stats[stat]:
                stats_sans_nulls = [s if s != None else "" for s in stats[stat][player]]
                print player + ',' + ','.join(stats_sans_nulls)

map_from_team_to_player_game_stats = deserialize_data(sys.argv[1])
print_csv(transform_scraped_data(map_from_team_to_player_game_stats))
