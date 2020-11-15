# Retrieves and stores a list of all implants, and automatically handles the difference between common and exceptionals.

import sys
import requests
import json

def getObj(implants, name):
	try:
		return implants[name]
	except:
		implant = {
			"1": "",
			"2": "",
			"3": "",
			"4": "",
			"5": "",
			"image": ""
		}
		return implant

if len(sys.argv) != 2:
	print("Usage: implants.py serviceId")
	sys.exit()

url = 'http://census.daybreakgames.com/s:'+sys.argv[1]+'/get/ps2:v2/item?item_category_id=133&item_type_id=45&c:limit=1000&c:lang=en'
req = requests.get(url = url)
data = req.json()

implants = {}

for implant in data["item_list"]:
	if implant["name"]["en"][-1:] == "1":
		obj = getObj(implants, implant["name"]["en"][:-2])
		obj["1"] = implant["description"]["en"]
		implants[implant["name"]["en"][:-2]] = obj 
	elif implant["name"]["en"][-1:] == "2":
		obj = getObj(implants, implant["name"]["en"][:-2])
		obj["2"] = implant["description"]["en"]
		implants[implant["name"]["en"][:-2]] = obj 
	elif implant["name"]["en"][-1:] == "3":
		obj = getObj(implants, implant["name"]["en"][:-2])
		obj["3"] = implant["description"]["en"]
		implants[implant["name"]["en"][:-2]] = obj 
	elif implant["name"]["en"][-1:] == "4":
		obj = getObj(implants, implant["name"]["en"][:-2])
		obj["4"] = implant["description"]["en"]
		implants[implant["name"]["en"][:-2]] = obj 
	elif implant["name"]["en"][-1:] == "5":
		obj = getObj(implants, implant["name"]["en"][:-2])
		obj["5"] = implant["description"]["en"]
		obj["image"] = implant["image_id"]
		implants[implant["name"]["en"][:-2]] = obj
	else:
		implants[implant["name"]["en"]] = {
			"desc": implant["description"]["en"],
			"image": implant["image_id"]
		}

implantsJSON = json.dumps(implants, indent=4, sort_keys=True)

file = open('implants.json', 'w')
file.write(implantsJSON)