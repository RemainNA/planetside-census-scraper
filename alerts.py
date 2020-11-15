# Retrieves and stores a list of all alerts
import sys
import requests
import json

if len(sys.argv) != 2:
	print("Usage: weapons.py serviceId")
	sys.exit()

url = 'http://census.daybreakgames.com/s:'+sys.argv[1]+'/get/ps2:v2/metagame_event?c:limit=500&c:lang=en'
req = requests.get(url = url)
data = req.json()

alerts = {}

for i in data["metagame_event_list"]:
	try:
		alerts[i["metagame_event_id"]] = {
			"name": i["name"]["en"],
			"description": i["description"]["en"]
		}
	except:
		continue

alertsJSON = json.dumps(alerts, indent=4, sort_keys=True)

file = open('alerts.json', 'w')
file.write(alertsJSON)