# Retrieves and stores a list of all ASP unlocks

import sys
import requests
import json

if len(sys.argv) != 2:
	print("Usage: asp.py serviceId")
	sys.exit()

url = 'http://census.daybreakgames.com/s:'+sys.argv[1]+'/get/ps2/item?item_category_id=133&item_type_id=1&c:limit=500&c:lang=en'
req = requests.get(url = url)
data = req.json()

unlocks = {}

for unlock in data["item_list"]:
	unlocks[unlock["item_id"]] = {
		"name": unlock["name"]["en"],
		"description": unlock["description"]["en"]
	}

aspJSON = json.dumps(unlocks, indent=4, sort_keys=True)

file = open('asp.json', 'w')
file.write(aspJSON)