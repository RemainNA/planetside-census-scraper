# Retrieves and stores a list of all vehicles, including name, description, and image

import sys
import requests
import json

if len(sys.argv) != 2:
	print("Usage: vehicles.py serviceId")
	sys.exit()

url = 'http://census.daybreakgames.com/s:'+sys.argv[1]+'/get/ps2:v2/vehicle?c:limit=100&c:lang=en'
req = requests.get(url = url)
data = req.json()

vehicles = {}

for vehicle in data["vehicle_list"]:
	vehicles[vehicle["vehicle_id"]] = {
		"name": vehicle["name"]["en"]
	}
	try:
		vehicles[vehicle["vehicle_id"]]["description"] = vehicle["description"]["en"]
	except:
		pass
	try:
		vehicles[vehicle["vehicle_id"]]["image_id"] = vehicle["image_id"]
	except:
		pass

vehiclesJSON = json.dumps(vehicles, indent=4, sort_keys=True)

file = open('vehicles.json', 'w')
file.write(vehiclesJSON)