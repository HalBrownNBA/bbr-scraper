import requests
from julienne import Julienne
from BeautifulSoup import BeautifulSoup
import pickle

# http://www.basketball-reference.com/players/d/duranke01/gamelog/2015/

# for each NBA team
# TODO: add TS% back

def scrape():
    map_from_team_to_player_game_stats = {}
    for each_team_name, each_team_url in all_nba_teams():
        map_from_team_to_player_game_stats[each_team_name] = {}
        for nba_player_name, nba_player_gamelog_url in all_nba_players_gamelog_urls(each_team_url):
            soup = BeautifulSoup(requests.get(nba_player_gamelog_url).text)
            player_init_table = soup.find(id="pgl_basic").prettify()
            player_table = Julienne(player_init_table).select(columns=['3P', '3P%', 'PTS', 'TRB', 'AST', 'MP'])
            map_from_team_to_player_game_stats[each_team_name][nba_player_name] = player_table

    return map_from_team_to_player_game_stats

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





def all_nba_players_gamelog_urls(team_url):
	# visit www.basketball-reference.com/teams/ATL/2015.html
	soup = BeautifulSoup(requests.get(team_url).text)
	# there's only one table on the page; it contains player names and salaries. 
	# we know the only hyperlinks in that table are links to the player pages
	list_of_player_pages = []
	for player_a_tag in soup.find(id="all_roster").findAllNext('a'):
		# we want to return these player urls: 
		# http://www.basketball-reference.com/players/h/horfoal01/gamelog/2015/
                player_url = "http://www.basketball-reference.com" + player_a_tag['href'].replace('.html', "") + "/gamelog/2015/"
                player_name = player_a_tag.string
                list_of_player_pages.append((player_name, player_url))
	
	return list_of_player_pages

# define "each NBA team" to be
def all_nba_teams():
	# when you go to http://www.basketball-reference.com/teams/
	all_teams = requests.get('http://www.basketball-reference.com/teams/')
	soup = BeautifulSoup(all_teams.text)
	# to look at 'active franchises', we need to look at the first table
	# we know that tables have the html class "stw," so we'll ask beautiful soup for all of the element with the class stw
	all_stw_tables = soup.findAll(True, "stw")
	active_teams_table = all_stw_tables[0]
	# only the children of the table whose class is full_table
	list_of_team_urls = []
	for each_a_tag in active_teams_table.findAll('a'):
		current_year = "2015"
                team_name = each_a_tag.string
                team_url = "http://www.basketball-reference.com" + each_a_tag['href'] + current_year + ".html"
		list_of_team_urls.append((team_name, team_url))
        print(list_of_team_urls)
	return list_of_team_urls
		
alldata = scrape()
pickle.dump(alldata, open("nba_player_data.pickle", "wb"))
transform_scraped_data(alldata)
