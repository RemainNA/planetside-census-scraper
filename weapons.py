# Retrieves a list of all weapons, then queries the details of each

import sys
import requests
import json

if len(sys.argv) != 2:
	print("Usage: weapons.py serviceId")
	sys.exit()

# Get list of all weapons
url = 'http://census.daybreakgames.com/s:'+sys.argv[1]+'/get/ps2:v2/item?item_type_id=26&c:limit=5000&c:lang=en'
req = requests.get(url = url)
data = req.json()

file = open('weapons2.json', 'r')
jsonData = file.read()
weapons = json.loads(jsonData)
ids = []

for i in data["item_list"]:
	try:
		ids.append(i["item_id"])
	except:
		continue

for i in ids:
	print(i)

	# Block below used to ignore weapons already present
	try:
		weapons[str(i)]["name"] == weapons[str(i)]["name"]
		continue
	except:
		pass

	# Look up weapon details
	url = 'http://census.daybreakgames.com/s:'+sys.argv[1]+'/get/ps2/item?item_id='+i+'&c:lang=en&c:join=fire_mode^inject_at:fire_mode^list:1,item_to_weapon^inject_at:fire_mode_2(weapon,weapon_to_fire_group^on:weapon_id^to:weapon_id^list:1(fire_group^on:fire_group_id^to:fire_group_id,fire_group_to_fire_mode^on:fire_group_id^to:fire_group_id^list:1(fire_mode_2^on:fire_mode_id^to:fire_mode_id^list:1(player_state_group^list:1^inject_at:player_state_group,player_state_group_2^on:player_state_group_id^to:player_state_group_id^inject_at:player_state_group_2^list:1,fire_mode_to_projectile^on:fire_mode_id^to:fire_mode_id^inject_at:projectile(projectile^on:projectile_id^to:projectile_id^inject_at:projectile_details))))))&c:join=weapon_datasheet^inject_at:ammo&c:join=item_category^on:item_category_id^to:item_category_id^inject_at:category&c:join=item_attachment^on:item_id^to:item_id^list:1^inject_at:attachments(item^on:attachment_item_id^to:item_id^inject_at:attachment(zone_effect^on:passive_ability_id^to:ability_id^inject_at:attachment_effects^list:1(zone_effect_type^on:zone_effect_type_id^to:zone_effect_type_id^inject_at:attachment_effects_description)))'
	req = requests.get(url = url)
	data = req.json()

	weapData = data["item_list"][0]
	try:
		weapons[i] = {
			"name": weapData["name"]["en"],
			"description": weapData["description"]["en"]
		}
		if "image_id" in weapData:
			weapons[i]["image_id"] = weapData["image_id"]
		else: #literally only for the Armory War Asset Orbital Strike at time of writing
			weapons[i]["image_id"] = -1
	except:
		continue

	try:
		weapons[i]["fireRate"]= weapData["ammo"]["fire_rate_ms"]
		weapons[i]["reload"]= weapData["ammo"]["reload_ms"]
		weapons[i]["clip"]= weapData["ammo"]["clip_size"]
		weapons[i]["ammo"]= weapData["ammo"]["capacity"]
	except:
		pass

	try:
		weapons[i]["category"] = weapData["category"]["name"]["en"]
	except:
		pass
	
	# Explosive gun
	try:
		weapons[i]["directDamage"]= weapData["ammo"]["direct_damage"]
		weapons[i]["indirectDamage"]= weapData["ammo"]["indirect_damage"]
	except:
		pass

	try:
		try:
			weapons[i]["maxDamage"] = weapData["fire_mode"][0]["damage_max"]
			weapons[i]["maxDamageRange"] = weapData["fire_mode"][0]["damage_max_range"]
			weapons[i]["minDamage"] = weapData["fire_mode"][0]["damage_min"]
			weapons[i]["minDamageRange"] = weapData["fire_mode"][0]["damage_min_range"]
		except:
			try: #specifically for the GODSAW
				weapons[i]["maxDamage"] = weapData["fire_mode"][1]["damage_max"]
				weapons[i]["maxDamageRange"] = weapData["fire_mode"][1]["damage_max_range"]
				weapons[i]["minDamage"] = weapData["fire_mode"][1]["damage_min"]
				weapons[i]["minDamageRange"] = weapData["fire_mode"][1]["damage_min_range"]
			except:
				pass
		try:
			weapons[i]["damage"] = weapData["fire_mode"][0]["damage"] #Only for the Tomoe?  Unsure
		except:
			pass
		try:
			weapons[i]["reload"] = weapData["fire_mode"][0]["reload_time_ms"]
		except:
			pass
		try:
			weapons[i]["chamber"] = weapData["fire_mode"][0]["reload_chamber_time_ms"]
		except:
			pass
		try:
			weapons[i]["pellets"] = weapData["fire_mode"][0]["pellets_per_shot"]
		except:
			pass
		try:
			weapons[i]["pelletSpread"] = weapData["fire_mode"][0]["pellet_spread"]
		except:
			pass
		try:
			weapons[i]["speed"] = weapData["fire_mode"][0]["speed"]
		except:
			pass
		try:
			weapons[i]["defZoom"] = weapData["fire_mode"][1]["default_zoom"]
		except:
			pass
	except:
		pass

	try:
		weapons[i]["heatCapacity"] = weapData["fire_mode_2"]["weapon_id_join_weapon"]["heat_capacity"]
		weapons[i]["heatBleedOff"] = weapData["fire_mode_2"]["weapon_id_join_weapon"]["heat_bleed_off_rate"]
		weapons[i]["overheatPenalty"] = weapData["fire_mode_2"]["weapon_id_join_weapon"]["heat_overheat_penalty_ms"]
	except:
		pass

	try:
		firemode = weapData["fire_mode_2"]["weapon_id_join_weapon_to_fire_group"][0]["fire_group_id_join_fire_group_to_fire_mode"][0]["fire_mode_id_join_fire_mode_2"][0]
		try:
			weapons[i]["hipCofRecoil"] = firemode["cof_recoil"]
		except:
			pass
		try:
			weapons[i]["heatPerShot"] = firemode["heat_per_shot"]
			weapons[i]["heatRecoveryDelay"] = firemode["heat_recovery_delay_ms"]
		except:
			pass
		try:
			weapons[i]["recoilAngleMax"] = firemode["recoil_angle_max"]
			weapons[i]["recoilAngleMin"] = firemode["recoil_angle_min"]
			weapons[i]["recoilHorizontalMax"] = firemode["recoil_horizontal_max"]
			weapons[i]["recoilHorizontalMin"] = firemode["recoil_horizontal_min"]
			weapons[i]["firstShotMultiplier"] = firemode["recoil_first_shot_modifier"]
		except:
			pass
		try:
			weapons[i]["recoilHorizontalTolerance"] = firemode["recoil_horizontal_tolerance"]
		except:
			pass
		try:
			weapons[i]["verticalRecoil"] = firemode["recoil_magnitude_max"]
			weapons[i]["headshotMultiplier"] = firemode["damage_head_multiplier"]
		except:
			pass
		try:
			weapons[i]["standingCofMin"] = firemode["player_state_group_2"][0]["cof_min"]
			weapons[i]["standingCofMax"] = firemode["player_state_group_2"][0]["cof_max"]
		except:
			pass
		try:
			weapons[i]["crouchingCofMin"] = firemode["player_state_group_2"][1]["cof_min"]
			weapons[i]["crouchingCofMax"] = firemode["player_state_group_2"][1]["cof_max"]
		except:
			pass
		try:
			weapons[i]["runningCofMin"] = firemode["player_state_group_2"][2]["cof_min"]
			weapons[i]["runningCofMax"] = firemode["player_state_group_2"][2]["cof_max"]
		except:
			pass
		try:
			weapons[i]["sprintingCofMin"] = firemode["player_state_group_2"][3]["cof_min"]
			weapons[i]["sprintingCofMax"] = firemode["player_state_group_2"][3]["cof_max"]
		except:
			pass
		try:
			weapons[i]["fallingCofMin"] = firemode["player_state_group_2"][4]["cof_min"]
			weapons[i]["fallingCofMax"] = firemode["player_state_group_2"][4]["cof_max"]
		except:
			pass
		try:
			weapons[i]["crouchWalkingCofMin"] = firemode["player_state_group_2"][5]["cof_min"]
			weapons[i]["crouchWalkingCofMax"] = firemode["player_state_group_2"][5]["cof_max"]
		except:
			pass
	except: # Exception as e: 
		# print(e)
		pass
	
	try:
		firemode = weapData["fire_mode_2"]["weapon_id_join_weapon_to_fire_group"][0]["fire_group_id_join_fire_group_to_fire_mode"][1]["fire_mode_id_join_fire_mode_2"][0]
		weapons[i]["adsCofRecoil"] = firemode["cof_recoil"]
		weapons[i]["adsMoveSpeed"] = firemode["move_modifier"]
		try:
			weapons[i]["standingCofMinADS"] = firemode["player_state_group_2"][0]["cof_min"]
			weapons[i]["standingCofMaxADS"] = firemode["player_state_group_2"][0]["cof_max"]
		except:
			pass
		try:
			weapons[i]["crouchingCofMinADS"] = firemode["player_state_group_2"][1]["cof_min"]
			weapons[i]["crouchingCofMaxADS"] = firemode["player_state_group_2"][1]["cof_max"]
		except:
			pass
		try:
			weapons[i]["runningCofMinADS"] = firemode["player_state_group_2"][2]["cof_min"]
			weapons[i]["runningCofMaxADS"] = firemode["player_state_group_2"][2]["cof_max"]
		except:
			pass
		try:
			weapons[i]["sprintingCofMinADS"] = firemode["player_state_group_2"][3]["cof_min"]
			weapons[i]["sprintingCofMaxADS"] = firemode["player_state_group_2"][3]["cof_max"]
		except:
			pass
		try:
			weapons[i]["fallingCofMinADS"] = firemode["player_state_group_2"][4]["cof_min"]
			weapons[i]["fallingCofMaxADS"] = firemode["player_state_group_2"][4]["cof_max"]
		except:
			pass
		try:
			weapons[i]["crouchWalkingCofMinADS"] = firemode["player_state_group_2"][5]["cof_min"]
			weapons[i]["crouchWalkingCofMaxADS"] = firemode["player_state_group_2"][5]["cof_max"]
		except:
			pass
	except:
		pass

	fireModes = []

	try:
		firemode = weapData["fire_mode_2"]["weapon_id_join_weapon_to_fire_group"]#[0]["fire_group_id_join_fire_group_to_fire_mode"]
		for j in firemode:
			try:
				if j["fire_group_id_join_fire_group_to_fire_mode"][0]["fire_mode_id_join_fire_mode_2"][0]["description"]["en"] not in fireModes:
					fireModes.append(j["fire_group_id_join_fire_group_to_fire_mode"][0]["fire_mode_id_join_fire_mode_2"][0]["description"]["en"])
			except Exception as e:
				print(e)
				pass
		weapons[i]["fireModes"] = fireModes
	except Exception as e:
		print(e)

	weaponsJSON = json.dumps(weapons, indent=4, sort_keys=True)

	file = open('weapons2.json', 'w')
	file.write(weaponsJSON)
