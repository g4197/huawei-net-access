def get_mock_create_site_return_value():
	return {
		"result": True,
		"id": "4d39440b-a9a9-41ca-81fb-2d9123642bc1",
		"name": "No.10",
		"description": "PM",
		"type": [
			"AP"
		],
		"pattern": 1,
		"latitude": "50",
		"longtitude": "111",
		"contact": "guohao",
		"tag": None,
		"isolated": None,
		"email": "t***t@huawei.com",
		"phone": "152******23",
		"postcode": "215000",
		"address": "Downing Street No.10"
	}


def get_mock_create_device_return_value():
	return {
		"result": True,
		"id": "cf0061d6-267a-46e9-a22a-81fd8511896d",
		"name": "AR1",
		"esn": "2102351BTJ0000000664",
		"description": "AR",
		"resourceId": "HUAWEI",
		"tenantId": "f3cf2391-f199-4973-888f-95f62c387309",
		"siteId": "2d974615-e437-4803-a0b4-aea7ab311622",
		"deviceModel": "AP4050DN",
		"tags": [],
		"systemIp": "192.168.1.0",
		"ztpConfirm": True,
		"role": [
			"Gateway"
		]
	}


def get_mock_get_sites_return_value():
	return [
		{
			"id": "1c44db61-aa01-4046-9ae0-32eb0214b4fd",
			"tenantId": "f3cf2391-f199-4973-888f-95f62c387309",
			"name": "asd",
			"description": "asd",
			"type": [
				"AP"
			],
			"latitude": "50.0",
			"longtitude": "111.0",
			"contact": "David",
			"tag": [],
			"isolated": None,
			"email": "t***t@huawei.com",
			"phone": "152******23",
			"postcode": "215000",
			"address": "66 JiangYun Road"
		}
	]


def get_mock_get_devices_return_value():
	return [{
		"id": "123"
	}]