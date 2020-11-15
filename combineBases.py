# Used to handle different Esamir on PS4 and PC

import json

file = open('bases.json', 'r')
jsonData = file.read()
bases1 = json.loads(jsonData)

file = open('bases2.json', 'r')
jsonData = file.read()
bases2 = json.loads(jsonData)

basesCombine = {}

for x,y in bases2.items():
	basesCombine[x] = y

for x,y in bases1.items():
	basesCombine[x] = y


basesJSON = json.dumps(basesCombine, indent=4, sort_keys=True)

file = open('bases3.json', 'w')
file.write(basesJSON)