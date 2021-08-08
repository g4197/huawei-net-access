import requests

tenantName = "OneHoldsThree@tenant.com"
tenantMagicNumber = "huawei12#$"
host = "139.9.213.72"
port = "18002"
BASE_URL = "https://" + host + ":" + port
POST_TOKEN_URL = "/controller/v2/tokens"
GET_SITES_URL = "/controller/campus/v3/sites"
GET_DEVICES_URL = "/controller/campus/v3/devices"
GET_SSID_CONFIG_URL = "/controller/campus/v3/networkconfig/site"
APPLICATION_JSON = "application/json"
headers = {"Content-Type": APPLICATION_JSON, "Accept": APPLICATION_JSON}


def print_list(lst: list):
	for element in lst:
		print(element)
		print()
	print("end***************************")


def get_token():
	"""
	Before using other functions, please get_token() first.

	:return: None
	"""
	global headers
	post_token_url = BASE_URL + POST_TOKEN_URL
	response = requests.post(
		post_token_url,
		headers=headers,
		json={
			"userName": tenantName,
			"password": tenantMagicNumber
		},
		verify=False
	)
	token_id = response.json()["data"]["token_id"]
	headers = {
		"Content-Type": APPLICATION_JSON,
		"Accept": APPLICATION_JSON,
		"X-AUTH-TOKEN": token_id
	}


def get_sites(name: str = "", uuid: str = ""):
	"""
	:param str name: Fuzzy query of site name
	:param str uuid: If uuid != "": accurate query according to site id
	:return: A list of all sites, each site contains: "id", "tenantId", "name", "description",
		"type", "latitude", "longtitude", "contact", "tag", "isolated", "email", "phone",
		"postcode", "address"
	"""
	get_token()
	get_sites_url = BASE_URL + GET_SITES_URL
	response = requests.get(
		get_sites_url,
		params={
			"name": name,
			"id": uuid
		},
		headers=headers,
		verify=False
	)
	sites_list = response.json()["data"]
	return sites_list


def create_site(site: dict):
	"""
	:param dict site: Each element in the sites contains the following keys
		name: str,
		description: str = "",
		latitude: str = "",
		longtitude: str = "",
		contact: str = "",
		email: str = "",
		phone: str = "",
		postcode: str = "",
		address: str = ""

	:return: A dict, including the results of creating each site

	:Warning: I cannot guarantee the correctness when len(sites) != 1
	"""
	get_token()
	get_sites_url = BASE_URL + GET_SITES_URL
	response = requests.post(
		get_sites_url,
		headers=headers,
		json={
			"sites": [site]
		},
		verify=False
	)

	""" The following code is for creating multiple sites.
	message = []  # the results of creating each site
	for i in range(len(sites)):
		message.append({})

	pos = {}  # key: name, value: index in sites
	for i, site in enumerate(sites):
		if site["name"] not in pos:
			pos[site["name"]] = i
		else:  # If there are the same names, only the first one is considered
			message[i]["result"] = False
			message[i]["errmsg"] = "The site name is already in use."

	for site in response.json()["success"]:
		index = pos[site["name"]]
		message[index] = site
		message[index]["result"] = True
		# message[index]["id"] = site["id"]
		# message[index]["type"] = site["type"]

	for site in response.json()["fail"]:
		index = pos[site["data"][0]["name"]]
		if "result" not in message[index]:
			# ""result" in message[index]" means site of the same name has been processed
			message[index]["result"] = False
			message[index]["errmsg"] = site["errmsg"]"""
	message = {}
	if response.json()["success"]:
		message = response.json()["success"][0]
		message["result"] = True
	else:
		message = response.json()["fail"][0]
		message["result"] = False

	return message


def delete_sites(ids: list):
	"""
	:param list ids: Each element in ids is a string and means the uuid of the site which user wants
		to delete.

	:return: A bool variable, meaning whether the delete operation was successful. If one of the
		sites is failed to delete, the return will be False.
	"""
	get_token()
	get_sites_url = BASE_URL + GET_SITES_URL
	response = requests.delete(
		get_sites_url,
		headers=headers,
		json={
			"ids": ids
		},
		verify=False
	)
	if "success" in response.json():
		return True
	else:
		return False
#
#
# def clear_all_sites():
# 	"""
# 	.. warning::
#
# 		Think twice before using this function
# 	"""
# 	get_token()
# 	sites = get_sites()
# 	ids = []
# 	for site in sites:
# 		ids.append(site["id"])
# 	delete_sites(ids)


# def test_sites():
# 	get_token()
# 	clear_all_sites()
# 	create_site([
# 		{
# 			"name": "No.9",
# 			"description": "qwe2",
# 			"latitude": "50",
# 			"longtitude": "111",
# 			"contact": "guohao",
# 			"email": "tenant@huawei.com",
# 			"phone": "15277431823",
# 			"postcode": "215000",
# 			"address": "Downing Street No.10"
# 		}
# 	])
#
# 	message = create_site([
# 		{
# 			"name": "No.9",
# 			"description": "qwe2",
# 			"latitude": "50",
# 			"longtitude": "111",
# 			"contact": "guohao",
# 			"email": "tenant@huawei.com",
# 			"phone": "15277431823",
# 			"postcode": "215000",
# 			"address": "Downing Street No.10"
# 		},
# 		{
# 			"name": "zxc",
# 			"description": "qwe",
# 			"latitude": "50",
# 			"longtitude": "111",
# 			"contact": "guohao",
# 			"email": "tenant@huawei.com",
# 			"phone": "15277431823",
# 			"postcode": "215000",
# 			"address": "Downing Street No.10"
# 		}
# 	])
# 	print(get_sites())
# 	delete_sites([message[1]["id"]])
# 	print(get_sites())


def get_devices(device_type: str = "", site_id: str = ""):
	"""
	:param str device_type: "AR", "AP", "LSW" or "FW", separated by ",". For example, "AP,AR"
	:param str site_id: If site_id != "", query according to site id
	:return: A list, each element in the list contains "createTime" etc.
	"""
	get_token()
	get_devices_url = BASE_URL + GET_DEVICES_URL
	response = requests.get(
		get_devices_url,
		params={
			"deviceType": device_type,
			"siteId": site_id
		},
		headers=headers,
		verify=False
	)
	devices_list = response.json()["data"]
	return devices_list


def create_device(device: dict):
	"""
	:param dict device: Each element in the sites contains the following keys
		esn: str = "",
		name: str = "",
		siteId: str = "",
		deviceModel: str = "",
		description: str = "",
		resourceId: str = "",
		systemIp: str = "",
		ztpConfirm: bool = True,
		role: list = []

		esn, name, siteId, deviceModel is required.

	:return: A dict, including the results of creating device

	:Warning: There is a bug! Because esn may be "". LENGTH OF DEVICES CANNOT EXCEED 1. Maybe fixed.
	"""
	get_token()
	get_devices_url = BASE_URL + GET_DEVICES_URL
	response = requests.post(
		get_devices_url,
		headers=headers,
		json={
			"devices": [device]
		},
		verify=False
	)
	""" The following code is for creating multiple devices a time.
	message = []  # the results of creating each site
	for i in range(len(devices)):
		message.append({})

	pos = {}  # key: name, value: index in sites
	for i, device in enumerate(devices):
		if device["esn"] not in pos:
			pos[device["esn"]] = i
		else:  # If there are the same names, only the first one is considered
			message[i]["result"] = False
			message[i]["errmsg"] = "The ESN is duplicate, it may have been used by the current tenant or other tenants"

	for device in response.json()["success"]:
		index = pos[device["esn"]]
		message[index] = device
		message[index]["result"] = True

	for device in response.json()["fail"]:
		index = pos[device["data"]["esn"]]
		if "result" not in message[index]:
			# ""result" in message[index]" means site of the same name has been processed
			message[index]["result"] = False
			message[index]["errmsg"] = device["errmsg"]"""
	message = {}
	if response.json()["success"]:
		message = response.json()["success"][0]
		message["result"] = True
	else:
		message["errmsg"] = response.json()["fail"][0]
		message["result"] = False

	return message


def delete_devices(ids: list):
	"""
	:param list ids: Each element in ids is a string and means the id of the device which user wants
		to delete.

	:return: If some devices are deleted successfully, the return will be a list of devices which
		are deleted successfully. Else the return will be False.
	"""
	get_token()
	get_devices_url = BASE_URL + GET_DEVICES_URL
	response = requests.delete(
		get_devices_url,
		headers=headers,
		json={
			"deviceIds": ids
		},
		verify=False
	)
	if response.json()["success"]:
		return response.json()["success"]
	else:
		"""for device in response.json()["fail"]:
			print(device["data"])  # device id"""
		return False
#
#

# def clear_all_devices():
# 	"""
# 	.. warning::
#
# 		Think twice before using this function
# 	"""
# 	get_token()
# 	devices = get_devices()
# 	ids = []
# 	for device in devices:
# 		ids.append(device["id"])
# 	delete_devices(ids)


#
# def test_devices():
# 	get_token()
# 	print_list(get_devices())
# 	sites = get_sites()
# 	message = create_device([
# 		{
# 			"esn": "",
# 			"name": "ASD",
# 			"siteId": sites[0]["id"],
# 			"deviceModel": "AP4050DN",  # the following keys are not required
# 			"description": "AP",
# 			"resourceId": "HUAWEI",
# 			"systemIp": "192.168.3.3",
# 			"ztpConfirm": True,
# 			"role": ["Gateway"]
# 		}
# 	])
# 	print_list(get_devices())
# 	delete_devices([message[0]["id"]])
# 	print_list(get_devices())


# def get_ssid_config_url(site_id: str):
# 	return BASE_URL + GET_SSID_CONFIG_URL + "/" + site_id + "/apssid"
#
#
# def create_ssid_config(
# 		site_id: str,
# 		name: str,
# 		enable: bool,
# 		connection_mode: str,
# 		hided_enable: bool,
# 		relative_radios: int,
# 		max_user_number: int,
# 		user_separation: bool,
# 		ssid_auth,
# 		ssid_policy
# ):
# 	"""
# 	:param site_id: site id (uuid)
# 	:param name: ssid name
# 	:param enable: whether the working status is on
# 	:param connection_mode: "bridge" or "nat"
# 	:param hided_enable: whether to hide ssid
# 	:param relative_radios: from 1 to 7, means radio frequency
# 	:param max_user_number: from 1 to 512
# 	:param user_separation:
# 	:param ssid_auth: contains the following keys: (* means optional)
# 		"mode": "open", "psk", "ppsk", "dot1x" or "mac"
# 		* "pskEncryptType": "wep", "wpa1AndWpa2", "wpa2"
# 		* "securityKey": password?
# 		* "securityKeyType": "AES", "AES-TKIP" or "TKIP", encryption method
# 		* "dot1xEncryptType": "wpa1AndWpa2", "wpa2"
# 		"portal": contains the following keys
# 			"mode": "portalDisable" means portal authentication is not enabled
# 		"macAutoBinding": bool
#
# 	:param ssid_policy: {} is ok
# 	:return: info about ssid configuration, too complex
# 	"""
# 	get_token()
# 	url = get_ssid_config_url(site_id)
# 	response = requests.post(
# 		url,
# 		headers=headers,
# 		json={
# 			"name": name,
# 			"enable": enable,
# 			"connectionMode": connection_mode,
# 			"hidedEnable": hided_enable,
# 			"maxUserNumber": max_user_number,
# 			"relativeRadios": relative_radios,
# 			"userSeparation": user_separation,
# 			"ssidAuth": ssid_auth,
# 			"ssidPolicy": ssid_policy
# 		},
# 		verify=False
# 	)
# 	if "data" not in response.json():
# 		return False
# 	else:
# 		return response.json()["data"]  # TODO
#
#
# def get_ssid_config(site_id: str):
# 	"""
# 	:param site_id:
# 	:return: a list of ssid configurations
# 	"""
# 	get_token()
# 	url = get_ssid_config_url(site_id)
# 	response = requests.get(
# 		url,
# 		headers=headers,
# 		verify=False
# 	)
# 	ssid_config_list = response.json()["data"]
# 	return ssid_config_list
#
#
# def delete_ssid_config(site_id: str, ids: list):
# 	"""
# 	:param site_id:
# 	:param ids: Each element in ids is an id of ssid configuration
# 	:return: An ssid configuration could be deleted twice. The ssid configurations which are deleted
# 		successfully is in return["success"], the ssid configurations which fail to be deleted
# 		is in return["fail"].
# 	"""
# 	get_token()
# 	url = get_ssid_config_url(site_id)
# 	response = requests.delete(
# 		url,
# 		headers=headers,
# 		json={
# 			"ids": ids
# 		},
# 		verify=False
# 	)
# 	return response.json()
#
#
# def test_ssid_config():
# 	get_token()
# 	print(create_ssid_config(
# 		site_id="2d974615-e437-4803-a0b4-aea7ab311622",
# 		name="Huawei-Guest12",
# 		enable=True,
# 		connection_mode="nat",
# 		hided_enable=False,
# 		max_user_number=10,
# 		relative_radios=3,
# 		user_separation=False,
# 		ssid_auth={
# 			"mode": "ppsk",
# 			"pskEncryptType": "wpa2",
# 			"securityKeyType": "AES",
# 			"portal": {"mode": "portalDisable"},
# 			"macAutoBinding": True
# 		},
# 		ssid_policy={}
# 	))
# 	print()
# 	ssid_config_list = get_ssid_config(site_id="2d974615-e437-4803-a0b4-aea7ab311622")
# 	if type(ssid_config_list) == list:
# 		for ssid_config in ssid_config_list:
# 			print(ssid_config, end="\n\n")
#
# 	delete_ssid_config(
# 		site_id="2d974615-e437-4803-a0b4-aea7ab311622",
# 		ids=[ssid_config_list[-1]["id"]]
# 	)
#
# 	print()
# 	ssid_config_list = get_ssid_config(site_id="2d974615-e437-4803-a0b4-aea7ab311622")
# 	if type(ssid_config_list) == list:
# 		for ssid_config in ssid_config_list:
# 			print(ssid_config, end="\n\n")


# def get_device_network_rate(
# 		mode: str,
# 		uuid: str,
# 		time_dimension: str,
# 		begin_time: int,
# 		end_time: int
# ):
# 	"""
# 	I have no rights...
#
# 	:param mode: "device", "site"
# 	:param id: uuid. If mode == "device", id is the device id. If mode == "site", id is the site id.
# 	:param time_dimension: "day", "week", "month"
# 	:param begin_time: int64, timestamp
# 	:param end_time: int64, timestamp
# 	:return: A list, each element in list is a dict, which contains the following keys:
# 		"timestamp": int64
# 		"uplinkRate": float
# 		"downlinkRate": float
# 		"unit": str
# 	"""
# 	get_token()
# 	url = BASE_URL + "/controller/campus/v1/performanceservice/basicperformance/networktraffic"
# 	response = requests.get(
# 		url,
# 		headers=headers,
# 		params={
# 			"mode": mode,
# 			"id": uuid,
# 			"timeDimension": time_dimension,
# 			"beginTime": begin_time,
# 			"endTime": end_time
# 		},
# 		verify=False
# 	)
# 	print(response.json())
# 	return response.json()["data"]
#
#
# def get_site_connected_terminals(
# 		site_id: str,
# 		time_dimension: str,
# 		begin_time: int,
# 		end_time: int,
# 		device_type: str
# ):
# 	"""
#
# 	:param site_id:
# 	:param time_dimension: "day", "week", "month", "year"
# 	:param begin_time: int64
# 	:param end_time: int64
# 	:param device_type: filter by device type, for example: "AP"
# 	:return: A list, each element contains the following keys:
# 		"timestamp":
# 		"user24G": the number of 2.4G user
# 		"user5G":the number of 5G user
# 	"""
# 	get_token()
# 	url = BASE_URL + "/controller/campus/v1/performanceservice/basicperformance/station/sites/" + site_id
# 	response = requests.get(
# 		url,
# 		headers=headers,
# 		params={
# 			"timeDimension": time_dimension,
# 			"beginTime": begin_time,
# 			"endTime": end_time,
# 			"deviceType": device_type
# 		},
# 		verify=False
# 	)
# 	print(response.json())
# 	return response.json()["data"]
#
#
# def get_device_connected_terminals(
# 		device_id: str,
# 		time_dimension: str,
# 		begin_time: int,
# 		end_time: int,
# ):
# 	"""
# 	The device must be belong to the current tenant.
#
# 	:param device_id:
# 	:param time_dimension: "day", "week", "month", "year"
# 	:param begin_time: int64
# 	:param end_time: int64
# 	:return: A list, each element contains the following keys:
# 		"timestamp":
# 		"clients": number of terminals
# 	"""
# 	get_token()
# 	url = BASE_URL + "/controller/campus/v1/performanceservice/basicperformance/station/device/" + device_id
# 	response = requests.get(
# 		url,
# 		headers=headers,
# 		params={
# 			"timeDimension": time_dimension,
# 			"beginTime": begin_time,
# 			"endTime": end_time
# 		},
# 		verify=False
# 	)
# 	print(response.json())
# 	if "data" in response.json():
# 		return response.json()["data"]
# 	else:
# 		return response.json()["errmsg"]


# def test3func():
# 	get_token()
# 	sites = get_sites()  # sites[0] has device d4a74df9-890d-4436-9c8d-8dedc53507e8
# 	# print(get_device_network_rate(
# 	# 	mode="device",
# 	# 	uuid="db815f68-5b69-4c9b-887e-f5828b9c812d",
# 	# 	time_dimension="day",
# 	# 	begin_time=1537408636,
# 	# 	end_time=1537495036
# 	# ))
# 	devices = get_devices()
# 	get_site_connected_terminals(
# 		site_id=sites[-1]["id"],
# 		time_dimension="day",
# 		begin_time=1537408636,
# 		end_time=1537495036,
# 		device_type="AP"
# 	)
# 	get_device_connected_terminals(
# 		device_id=devices[-1]["id"],
# 		time_dimension="day",
# 		begin_time=1537408636,
# 		end_time=1537495036,
# 	)

