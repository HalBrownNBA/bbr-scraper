import requests
from julienne import Julienne
from BeautifulSoup import BeautifulSoup
import json

# http://www.basketball-reference.com/players/d/duranke01/gamelog/2015/

# for each NBA team
# TODO: add TS% back

def scrape():
    map_from_team_to_player_game_stats = {}
    for each_team_name, each_team_url in all_nba_teams():
        print("Processing " + each_team_name + "...")
        map_from_team_to_player_game_stats[each_team_name] = {}
        for nba_player_name, nba_player_gamelog_url in all_nba_players_gamelog_urls(each_team_url):
            print("Processing " + nba_player_name + "...")
            soup = BeautifulSoup(requests.get(nba_player_gamelog_url).text)
            player_gamelogs = soup.find(id="pgl_basic")
            if player_gamelogs:
                cleaned_gamelogs = player_gamelogs.prettify()
                player_table = Julienne(cleaned_gamelogs).select(columns=['3P', '3P%', 'PTS', 'TRB', 'AST', 'MP', 'FG%'])

                print(serialize_record_adhoc(each_team_name, nba_player_name, player_table))

# a record is basically a comma-separated list of player team, player name, player game logs
# we are heavily relying on the idea that there are no commas in player team or player name
def deserialize_record_adhoc(record):
    record_fields = record.strip().split(',')
    player_team, player_name = (record_fields[0], record_fields[1])
    player_table = json.loads(','.join(record_fields[2:len(record_fields)]))
    return (player_team, player_name, player_table)

def serialize_record_adhoc(team_name, player_name, player_table):
    return team_name + "," + player_name + "," + json.dumps(player_table)

def all_nba_players_gamelog_urls(team_url):
    if "NJN" in team_url: # TODO: fix this
        team_url = team_url.replace("NJN", "BRK")
    if "CHA" in team_url: # TODO: fix this
        team_url = team_url.replace("CHA", "CHO")
    if "NOH" in team_url: # TODO: fix this
        team_url = team_url.replace("NOH", "NOP")
    # visit www.basketball-reference.com/teams/ATL/2015.html
    soup = BeautifulSoup(requests.get(team_url).text)
    # there's only one table on the page; it contains player names and salaries. 
    # we know the only hyperlinks in that table are links to the player pages
    list_of_player_pages = []
    for player_a_tag in soup.find(id="all_roster").findChildren('a'):
        if "player" in player_a_tag['href'] and len(player_a_tag.string) > 1:
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

scrape()
