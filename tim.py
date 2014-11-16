import requests
from julienne import Julienne
from BeautifulSoup import BeautifulSoup
# http://www.basketball-reference.com/players/d/duranke01/gamelog/2014/

# for each NBA team
def scrape():
	for each_team_url in all_nba_teams():
		# TODO: we really want both the player's name and URL inside here
		for nba_player_gamelog_url in all_nba_players_gamelog_urls(each_team_url):
			# visit this url
			soup = BeautifulSoup(requests.get(nba_player_gamelog_url).text)
			print(nba_player_gamelog_url)
			player_init_table = soup.find(id="pgl_basic").prettify()
			player_table = Julienne(player_init_table).select(columns=['3P', '3P%', 'PTS', 'TRB', 'AST', 'MP'])
			print player_table
			return player_table
                        # advanced_table_soup = soup.find(id="pgl_advanced").prettify()
			# player_advanced_table = Julienne(advanced_table_soup).select(columns=['TS%'])
			# player_table.rows()
			
			# game_records_with_ts_percentage_added = []
			# for game_record in player_table.rows():
				# for advanced_game_record in player_advanced_table.rows():
					# game_records_with_ts_percentage_added.append(game_record.update(advanced_game_record))
			# now we have a collection of game records for a given player with all the stats we want
			# [{PTS: 31, TS%: 65}, {}, {}

def transform_scraped_data(map_from_team_to_player_game_stats):
    # STATS = ['3P', '3P%', 'PTS', 'TRB', 'AST', 'TS%']
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
	# visit www.basketball-reference.com/teams/ATL/2014.html
	soup = BeautifulSoup(requests.get(team_url).text)
	# there's only one table on the page; it contains player names and salaries. 
	# we know the only hyperlinks in that table are links to the player pages
	list_of_player_pages = []
	# TODO: instead of just grabbing all tables, we need to find t
	for player_a_tag in soup.find(id="all_roster").findAllNext('a'):
		# we want to return these player urls: 
		# http://www.basketball-reference.com/players/h/horfoal01/gamelog/2014/
                list_of_player_pages.append("http://www.basketball-reference.com" + player_a_tag['href'].replace('.html', "") + "/gamelog/2014/")
	
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
		current_year = "2014"
		list_of_team_urls.append("http://www.basketball-reference.com" + each_a_tag['href'] + current_year + ".html")
        print(list_of_team_urls)
	return list_of_team_urls
		
transform_scraped_data(scrape())
