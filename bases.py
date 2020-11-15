# Retrieves and stores a list of all bases

import sys
import requests
import json

if len(sys.argv) != 2:
	print("Usage: bases.py serviceId")
	sys.exit()

url = 'http://census.daybreakgames.com/s:'+sys.argv[1]+'/get/ps2:v2/map_region?c:limit=500' # There appear to be 331 bases as of writing
req = requests.get(url = url)
data = req.json()

bases = {}

for base in data["map_region_list"]:
	try:
		bases[base["facility_id"]] = {
			"name": base["facility_name"],
			"type": base["facility_type"],
			"continent": base["zone_id"]
		}
	except:
		pass

basesJSON = json.dumps(bases, indent=4, sort_keys=True)

file = open('bases.json', 'w')
file.write(basesJSON)