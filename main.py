"""
Goal of this currently is quite simple: Find out the matches that X and I have played together. 
Then, see if we killed eachother / how we did. 
"""

import requests
import pprint
BEARER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJiNmYyYWI3MC0yNGYyLTAxMzYtNWU4Yy01ZDJiZjJmY2I5ZmMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTI0MDI3MzYxLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InN3YWdtYWVzdHJvcyJ9.EczYy1SqgEAi-JJKyNxjufRyOh1w3n3UbRlnrqwycoo"
BASE_URL = "https://api.playbattlegrounds.com/shards/pc-na" 

def get(url, auth=True): 
	"""
	Make a get request to a url. Auth is optional.
	"""
	headers = {"Accept": "application/vnd.api+json"} 
	if auth:
		headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
	r = requests.get(url, headers=headers)
	return r.json()

def get_matches(player_name):
	"""
	Acquire a list of matches based on a player.
	"""
	player_info = get(f"{BASE_URL}/players?filter[playerNames]={player_name}")
	match_ids = [match['id'] for match in player_info['data'][0]['relationships']['matches']['data']]
	return match_ids

# Find our matches
rodney_matches = get_matches("Watersedge")
shroud_matches = get_matches("shroud")
shared_rounds = []

# Find our shared matches 
for s_id in shroud_matches:
	for r_id in rodney_matches:
		if r_id == s_id:
			print("=====We have a match======")
			print(r_id)
			print("==========================")
			shared_rounds.append(r_id)

class Match():
	pass 	

# Find the telemetry object in each match. 
# Fuck Bunghole for designing their API like this. 
telem_urls = []
for id in shared_rounds:	
	match_data = get(f"{BASE_URL}/matches/{id}")
	telemetry_id = match_data['data']['relationships']['assets']['data'][0]['id']
	telem_data = {}
	# Get the telemetry_url 
	for asset in match_data['included']:
		if asset['id'] == telemetry_id:
			# We've found our telem data. 
			telem_data = asset
			break 

	telem_urls.append(telem_data['attributes']['URL'])

print(telem_urls)

pprint.pprint(get(telem_urls[0], auth=False))