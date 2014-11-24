import json

def deserialize_record_adhoc(record):
    record_fields = record.strip().split(',')
    player_team, player_name = (record_fields[0], record_fields[1])
    player_table = json.loads(','.join(record_fields[2:len(record_fields)]))
    return (player_team, player_name, player_table)

def serialize_record_adhoc(team_name, player_name, player_table):
    return team_name + "," + player_name + "," + json.dumps(player_table)
