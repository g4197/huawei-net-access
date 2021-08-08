from django.test import TestCase, Client
import json
from .utils import modify
from .patch_code import get_mock_create_device_return_value, get_mock_create_site_return_value,\
	get_mock_get_sites_return_value, get_mock_get_devices_return_value
from .config import MAGIC_NUMBER, GUEST
import random
from unittest import mock


class BackendTest(TestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.json_content = "application/json"
		self.username = "g4197"
		self.password = "91463777c12498832dd21eb557a19b98"
		self.profile = {
			"name": "GuoHao",
			"username": self.username,
			"password": self.password,
			"email": "cfhmgh@163.com",
			"telephone": "1234567890",
			"address": "cfhm",
			"privilege": GUEST
		}
		self.order = {
			"site_name": "One Holds Three",
			"site_address": "www.oneholdsthree.com",
			"billing_method": 1,
			"network_demand": ["Guest", "Management", "Test"],
			"flow_threshold": 998244353
		}
		self.ssid = {
			"name": "1holds3",
			"enable": 1,
			"connection_mode": "bridge",
			"hid_enable": 1,
			"relative_radios": 1,
			"max_user_number": 114,
			"user_separation": 1,
			"auth_mode": "open"
		}
		self.long_str = "0" * 1000
		self.uuid = "6ae03865-cbf8-43fc-94e8-a74647c7dc53"
		self.c = Client()

	def post_check(self, url: str, data: dict, code: int):
		"""
			Using POST method to send a json request to `url`, with json data `data`, then check
			if the returned status code equals to `code`.
		"""
		self.assertEqual(self.c.post(url, data, content_type=self.json_content).status_code, code)

	def get_check(self, url: str, data: dict, code: int):
		"""
			Using GET method to send a json request to `url`, with json data `data`, then check
			if the returned status code equals to `code`.
		"""
		self.assertEqual(self.c.get(url, data).status_code, code)

	def login(self, admin=False):
		"""
			Login with `self.c`.

			Args:
				:param bool admin: If `True`, then login with admin, or else register with `self.profile` and login.
		"""
		if admin:
			self.c.post(
				"/api/login",
				{"data": {"username": "admin", "password": MAGIC_NUMBER}},
				content_type=self.json_content
			)
		else:
			self.c.post("/api/register", {"data": self.profile}, content_type=self.json_content)  # register first
			self.c.post(
				"/api/login",
				{"data": {"username": self.username, "password": self.password}},
				content_type=self.json_content
			)  # then login

	def logout(self):
		self.c.post("/api/logout")

	def get_order_information(self):
		response = self.c.get("/api/get_order_information")
		self.assertEqual(response.status_code, 200)
		orders = json.loads(response.content)["data"]["orders"]
		return orders

	def get_latest_order(self):
		"""
			ATTENTION: A user and an order must login and be submitted first.
		"""
		orders = self.get_order_information()
		self.assertEqual(type(orders), list)
		return orders[-1]

	def get_order_information(self):
		url = "/api/get_order_information"
		self.login()
		response = self.c.get(url)
		self.assertEqual(response.status_code, 200)
		orders = json.loads(response.content)["data"]["orders"]
		return orders

	def get_latest_order(self):
		"""
			First login, then submit_order and get_latest_order.
		"""
		orders = self.get_order_information()
		self.assertEqual(type(orders), list)
		return orders[-1]

	def submit_order(self, site_name=""):
		"""
			Submit order with `self.order` and `site_name`.
			ATTENTION: A user must login first.
		"""
		if site_name == "":
			site_name = self.order["site_name"]
		self.c.post("/api/submit_order", {"data": modify(self.order, "site_name", site_name)}, content_type=self.json_content)

	def cancel_order(self, order_id):
		"""
			Cancel the order with uuid=order_id.
			ATTENTION: A user must login first, and submit an order.
		"""
		self.post_check("/api/cancel_order", {"data": {"id": order_id, "reason": ""}}, 201)

	def test_register(self):
		url = "/api/register"
		# invalid method
		self.get_check(url, {}, 405)
		# no data field
		self.post_check(url, {}, 400)
		# missing needed field
		self.post_check(url, {"data": {}}, 400)
		invalid_profile = self.profile.copy()
		invalid_profile["email"], invalid_profile["telephone"] = "", ""
		# email and telephone both empty
		self.post_check(url, {"data": invalid_profile}, 400)
		# invalid email address
		self.post_check(url, {"data": modify(self.profile, "email", "www.baidu.com")}, 400)
		# invalid telephone number
		self.post_check(url, {"data": modify(self.profile, "telephone", "www.baidu.com")}, 400)
		valid_profile = self.profile.copy()
		valid_profile["username"], valid_profile["telephone"] = "hall", "010-62782334"
		# strong telephone number: http://www.hall.tsinghua.edu.cn
		self.post_check(url, {"data": valid_profile}, 201)
		# empty username
		self.post_check(url, {"data": modify(self.profile, "username", "")}, 400)
		# register succeeded
		self.post_check(url, {"data": self.profile}, 201)
		# user existed
		self.post_check(url, {"data": self.profile}, 400)

	def test_login(self):
		url = "/api/login"
		# register first
		self.c.post("/api/register", {"data": self.profile}, content_type=self.json_content)
		# no password
		self.post_check(url, {"data": {"username": self.username}}, 400)
		# login failed
		self.post_check(url, {"data": {"username": self.username, "password": ""}}, 400)
		# login succeeded
		self.post_check(url, {"data": {"username": self.username, "password": self.password}}, 200)
		# login again
		self.post_check(url, {"data": {"username": self.username, "password": self.password}}, 403)

	def test_logout(self):
		url = "/api/logout"
		self.post_check(url, {}, 401)
		self.login()
		self.post_check(url, {}, 200)

	def test_get_csrf_token(self):
		self.post_check("/api/get_csrf_token", {}, 200)

	def test_submit_order(self):
		url = "/api/submit_order"
		self.login()
		# long site address
		self.post_check(url, {"data": modify(self.order, "site_address", self.long_str)}, 400)
		# invalid billing method
		self.post_check(url, {"data": modify(self.order, "billing_method", "1")}, 400)
		# invalid network demand, must be a list
		self.post_check(url, {"data": modify(self.order, "network_demand", "guohao")}, 400)
		# invalid network demand, must be Guest, Management or Test
		self.post_check(url, {"data": modify(self.order, "network_demand", ["guohao"])}, 400)
		# flow threshold too high
		self.post_check(url, {"data": modify(self.order, "flow_threshold", 2 ** 64)}, 400)

		self.post_check(url, {"data": self.order}, 201)

	def test_get_userprofile(self):
		url = "/api/get_userprofile"
		# not login
		self.get_check(url, {}, 401)
		# now login
		self.login()
		response = self.c.get(url)
		self.assertEqual(response.status_code, 200)
		userprofile = json.loads(response.content)["data"]["userprofile"]
		self.assertTrue(
			"username" in userprofile and "email" in userprofile and "name" in userprofile and
			"telephone" in userprofile and "address" in userprofile and "id" in userprofile
		)

	def test_get_order_information(self):
		url = "/api/get_order_information"
		# not login
		self.get_check(url, {}, 401)
		# now login
		self.login()
		self.submit_order()
		self.submit_order()
		# then login with admin
		self.logout()
		self.login(admin=True)
		self.submit_order()
		self.assertEqual(len(json.loads(self.c.get(url).content)["data"]["orders"]), 3)

	def test_cancel_order(self):
		url = "/api/cancel_order"
		self.login()
		# no such id
		self.post_check(url, {"data": {"id": self.uuid, "reason": ""}}, 400)
		# now submit an order
		self.submit_order()
		# check new id: TODO
		latest_order = self.get_latest_order()
		# the reason is too long
		self.post_check(url, {"data": {"id": latest_order["id"], "reason": self.long_str}}, 400)
		# cancel it
		self.cancel_order(latest_order["id"])
		# cancel again
		self.post_check(url, {"data": {"id": latest_order["id"], "reason": ""}}, 400)
		# close it
		self.c.post("/api/close_order", {"id": latest_order["id"]}, content_type=self.json_content)
		# cancel a closed order
		self.post_check(url, {"data": {"id": latest_order["id"], "reason": ""}}, 400)

	def test_restore_order(self):
		url = "/api/restore_order"
		self.login()
		# invalid method
		self.get_check(url, {}, 405)
		self.submit_order()
		latest_order = self.get_latest_order()

		# order has not been cancelled and cannot be restored
		self.post_check(url, {"data": {"id": latest_order["id"]}}, 400)
		# cancel the latest order
		self.cancel_order(latest_order["id"])
		# restore it
		self.post_check(url, {"data": {"id": latest_order["id"]}}, 201)

	def test_close_order(self):
		url = "/api/close_order"
		# user not login
		self.post_check(url, {}, 401)
		self.login()
		self.submit_order()
		latest_order = self.get_latest_order()
		# close the order
		self.post_check(url, {"data": {"id": latest_order["id"]}}, 201)
		# close again
		self.post_check(url, {"data": {"id": latest_order["id"]}}, 400)

	def test_get_single_order_information(self):
		url = "/api/get_single_order_information"
		# login as normal user and submit an order
		self.login()
		self.submit_order()
		# no id field
		self.get_check(url, {}, 400)
		normal_order = self.get_latest_order()
		self.get_check(url, {"id": normal_order["id"]}, 200)
		# login as admin and submit an order
		self.logout()
		self.login(admin=True)
		normal_order = self.get_latest_order()
		self.get_check(url, {"id": normal_order["id"]}, 200)
		self.submit_order()
		admin_order = self.get_latest_order()
		# check normal user permission
		self.logout()
		self.login()
		self.get_check(url, {"id": admin_order["id"]}, 401)

	def test_survey_order(self):
		url = "/api/survey_order"
		self.login()
		self.submit_order()
		order_id = self.get_latest_order()["id"]
		# no permission
		self.post_check(url, {"data": {"id": order_id, "network_list": [], "ssid_list": []}}, 400)
		self.logout()
		self.login(admin=True)
		# invalid data field
		self.post_check(url, {"data": {"id": order_id, "network_list": 1, "ssid_list": []}}, 400)
		self.post_check(url, {"data": {"id": order_id, "network_list": [""], "ssid_list": []}}, 400)
		self.post_check(url, {"data": {"id": order_id, "network_list": [], "ssid_list": [""]}}, 400)
		# network name too long
		self.post_check(
			url,
			{"data": {"id": order_id, "network_list": [{"name": self.long_str}], "ssid_list": []}},
			400
		)
		# empty network name
		self.post_check(
			url,
			{"data": {"id": order_id, "network_list": [{"name": ""}], "ssid_list": []}},
			400
		)
		# multiple same network name
		self.post_check(
			url,
			{"data": {"id": order_id, "network_list": [{"name": "1"}, {"name": "1"}], "ssid_list": []}},
			400
		)
		# ssid name too long
		self.post_check(
			url,
			{"data": {"id": order_id, "network_list": [], "ssid_list": [modify(self.ssid, "name", self.long_str)]}},
			400
		)
		# invalid connection mode
		self.post_check(
			url,
			{"data": {"id": order_id, "network_list": [], "ssid_list": [modify(self.ssid, "connection_mode", "")]}},
			400
		)
		# invalid relative radios
		self.post_check(
			url,
			{"data": {"id": order_id, "network_list": [], "ssid_list": [modify(self.ssid, "relative_radios", 8)]}},
			400
		)
		# invalid max user number
		self.post_check(
			url,
			{"data": {"id": order_id, "network_list": [], "ssid_list": [modify(self.ssid, "max_user_number", 0)]}},
			400
		)
		# invalid auth mode
		self.post_check(
			url,
			{"data": {"id": order_id, "network_list": [], "ssid_list": [modify(self.ssid, "auth_mode", "")]}},
			400
		)
		# psk encrypt check
		ppsk_ssid = modify(self.ssid, "auth_mode", "ppsk")
		ppsk_ssid["auth_psk_encrypt_type"] = "wpa2"
		ppsk_ssid["auth_security_key_type"] = "AES"
		self.post_check(url, {"data": {"id": order_id, "network_list": [], "ssid_list": [ppsk_ssid]}}, 400)
		ppsk_ssid["auth_mac_auto_binding"] = True
		psk_ssid = modify(modify(ppsk_ssid, "auth_mode", "psk"), "auth_security_key", "12345678")
		self.post_check(
			url,
			{
				"data": {
					"id": order_id,
					"network_list": [],
					"ssid_list": [modify(ppsk_ssid, "auth_psk_encrypt_type", "")]
				}
			},
			400
		)
		self.post_check(
			url,
			{
				"data": {
					"id": order_id,
					"network_list": [],
					"ssid_list": [modify(psk_ssid, "auth_security_key", "")]
				}
			},
			400
		)
		self.post_check(
			url,
			{
				"data": {
					"id": order_id,
					"network_list": [],
					"ssid_list": [modify(ppsk_ssid, "auth_security_key_type", "")]
				}
			},
			400
		)
		# dot1x encrypt check
		dot1x_ssid = modify(self.ssid, "auth_mode", "dot1x")
		dot1x_ssid["auth_dot1x_encrypt_type"] = "wpa2"
		self.post_check(
			url,
			{
				"data": {
					"id": order_id,
					"network_list": [],
					"ssid_list": [modify(dot1x_ssid, "auth_dot1x_encrypt_type", "")]
				}
			},
			400
		)
		# valid operation
		self.post_check(
			url,
			{
				"data": {
					"id": order_id,
					"network_list": [{"name": "gkk"}],
					"ssid_list": [self.ssid, ppsk_ssid, dot1x_ssid, psk_ssid]
				}
			},
			201
		)
		# survey again
		self.post_check(url, {"data": {"id": order_id, "network_list": [], "ssid_list": []}}, 400)

	def test_modify_password(self):
		url = "/api/modify_password"
		data = {
			"username": self.username,
			"original_password": self.password,
			"password": "asdasd",
			"check_password": "asdasd"
		}
		self.login()
		# json decode failed
		self.assertEqual(self.c.post(url).status_code, 400)
		# permission denied
		self.post_check(url, {"data": modify(data, "username", "admin")}, 400)
		# password incorrect
		self.post_check(url, {"data": modify(data, "original_password", "")}, 400)
		# different new passwords
		self.post_check(url, {"data": modify(data, "password", "1")}, 400)
		# modify successfully
		self.post_check(url, {"data": data}, 201)
		self.logout()
		# now login as admin and try to modify password
		self.login(admin=True)
		# no such user
		self.post_check(url, {"data": modify(data, "username", "")}, 400)
		self.post_check(url, {"data": data}, 201)

	def test_modify_userprofile(self):
		url = "/api/modify_userprofile"
		self.login()
		# invalid privilege
		self.post_check(url, {"data": modify(self.profile, "privilege", 4)}, 400)
		self.post_check(url, {"data": self.profile}, 201)
		# permission denied
		self.post_check(url, {"data": modify(self.profile, "username", "admin")}, 400)

	def test_get_user_list(self):
		url = "/api/get_user_list"
		# no permission
		self.login()
		self.get_check(url, {}, 400)
		self.logout()
		# now login as admin
		self.login(admin=True)
		self.get_check(url, {}, 200)

	@mock.patch("api.NCE_campus.create_site")
	@mock.patch("api.NCE_campus.create_device")
	def test_deploy_order(self, mock_create_site, mock_create_device):
		# mock
		mock_create_site.return_value = get_mock_create_site_return_value()
		mock_create_device.return_value = get_mock_create_device_return_value()

		url = "/api/deploy_order"
		# invalid method
		self.get_check(url, {}, 405)
		self.login()
		# guest submits an order
		# NOTICE: site_name must be random
		site_name = str(random.random())
		self.submit_order(site_name=site_name)
		order_id = self.get_latest_order()["id"]
		self.logout()
		self.login(admin=True)

		# not surveyed
		self.post_check(url, {"data": {"id": order_id}}, 400)

		# survey order
		self.post_check(
			"/api/survey_order",
			{
				"data": {
					"id": order_id,
					"network_list": [
						{"name": "network1"},
						{"name": "network2"}
					],
					"ssid_list": [self.ssid]
				}
			},
			201
		)

		# deploy order
		self.post_check(url, {"data": {"id": order_id}}, 201)

		""" 
		# Duplicate site name
		self.submit_order(site_name=site_name)
		order_id = self.get_latest_order()["id"]

		# survey order
		self.post_check(
			"/api/survey_order",
			{
				"data": {
					"id": order_id,
					"network_list": [
						{"name": "network3"},
						{"name": "network4"}
					],
					"ssid_list": [self.ssid]
				}
			},
			201
		)

		# deploy order, site_name is duplicate
		self.post_check(url, {"data": {"id": order_id}}, 400)"""

	@mock.patch("api.NCE_campus.get_sites")
	def test_get_sites(self, mock_get_sites):
		# mock
		mock_get_sites.return_value = get_mock_get_sites_return_value()

		url = "/api/get_sites"
		# user not login
		self.get_check(url, {}, 401)
		self.login()

		self.get_check(url, {}, 200)

	@mock.patch("api.NCE_campus.get_devices")
	def test_get_devices(self, mock_get_devices):
		# mock
		mock_get_devices.return_value = get_mock_get_devices_return_value()

		url = "/api/get_devices"
		# invalid method
		self.post_check(url, {}, 405)
		self.login()

		self.get_check(url, {"id": "1c44db61-aa01-4046-9ae0-32eb0214b4fd"}, 200)

	def test_get_single_site_information(self):
		url = "/api/get_single_site_information"
		self.login()
		# no such site id
		self.get_check(url, {"id": ""}, 400)
