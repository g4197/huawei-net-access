from django.http import JsonResponse
import re
import json
from .config import USER_NOT_LOGIN, JSON_DATA_FIELD_INVALID, FIELD_META, USER_PERMISSION_DENIED, FEE_PER_KB,\
	ORDER_CLOSED, OPERATIONS_ENGINEER, ADMIN
from .models import Order, Device, Site, UserProfile
from django.contrib.auth.models import User
from . import NCE_campus
from django.core.mail import send_mail
import time
from random import randint


def gen_response(code: int, message: str, data=None):
	return JsonResponse({"code": code, "message": message, "data": data}, status=code)


def verify_email(email):
	pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
	if re.match(pattern, email) is None:
		return False
	else:
		return True


def verify_telephone(telephone):
	pattern = r'0?(13|14|15|17|18|19)[0-9]{9}|[0-9-()（）]{7,18}'  # cell phone number or phone number
	if re.match(pattern, telephone) is None:
		return False
	else:
		return True


def check_info(elements, info):
	"""
		Check if `info` contains `elements`.
	"""
	for element in elements:
		if element not in info:
			return False
	return True


def userprofile_to_dict(user_profile):
	return {
		"username": user_profile.user.username,
		"email": user_profile.email,
		"name": user_profile.name,
		"telephone": user_profile.telephone,
		"address": user_profile.address,
		"id": user_profile.id,
		"privilege": user_profile.privilege
	}


def ssid_to_dict(ssid):
	return {
		"name": ssid.name,
		"enable": ssid.enable,
		"connection_mode": ssid.connection_mode,
		"hid_enable": ssid.hid_enable,
		"relative_radios": ssid.relative_radios,
		"max_user_number": ssid.max_user_number,
		"user_separation": ssid.user_separation,
		"auth_mode": ssid.auth.mode,
		"auth_psk_encrypt_type": ssid.auth.psk_encrypt_type,
		"auth_security_key": ssid.auth.security_key,
		"auth_security_key_type": ssid.auth.security_key_type,
		"auth_dot1x_encrypt_type": ssid.auth.dot1x_encrypt_type,
		"auth_mac_auto_binding": ssid.auth.mac_auto_binding
	}


def order_to_dict(order, need_network_list=False, need_ssid_list=False):
	network_demand = []
	if order.network_demand_guest:
		network_demand.append("Guest")
	if order.network_demand_management:
		network_demand.append("Management")
	if order.network_demand_test:
		network_demand.append("Test")

	ret = {
		"owner": order.owner.name,
		"site_name": order.site.name,
		"site_address": order.site.address,
		"billing_method": order.billing_method,
		"network_demand": network_demand,
		"state": order.state,
		"id": order.uuid,
		"flow_threshold": order.site.flow_threshold,
		"reason": order.reason
	}
	if need_network_list:
		ret["network_list"] = [{"name": network.name} for network in order.network_set.all()]
	if need_ssid_list:
		ret["ssid_list"] = [ssid_to_dict(ssid) for ssid in order.ssid_set.all()]
	return ret


def check_and_parse(
		method: str, request,
		info_list=None,	privilege_list=None, stringify_list=[], empty_check_list=[], length_limit_list=[],
		user_auth=False, check_username_existence=False, check_contact=False, check_order_id=False, site_check=False
	):
	"""
		Check if `request` is valid. Return the parsed data or an error response.

		Args:
			:param str method: A string indicated the method type.
			:param request: The request.
			:param list info_list: A List of strings, for checking whether JSON data includes all the keys
				in `info_list`.
			:param list privilege_list: A list of integers, for checking whether the privilege of the user
				belongs to privilege_list. If it is not `None`, `user_auth` should always be `True`.
			:param list stringify_list: A list of strings, must be a sublist of `info_list`. All the data
				with key in `stringify_list` will be converted to a string.
			:param list empty_check_list: A list of strings, must be a sublist of `info_list`. It is for
				checking whether the length of all data	with keys in `empty_check_list` are empty.
				This will be done after stringification.
			:param list length_limit_list: A list of strings, must be a sublist of `info_list` and a subset
				in `FIELD_META`. It is for checking whether the length of all data with keys in
				`length_limit_list` exceeds the max length. This will be done after stringification.
			:param bool user_auth: If `True`, the function will check whether the user in `request` is
				authenticated.
			:param bool check_username_existence: If `True`, the function will check whether the given
				username exists. Note that "username" must be an element of `info_list`.
			:param bool check_contact: If `True`, the function will check whether the email and telephone both
				are empty, and check the validity of them. Note that "email" and "telephone" must be
				elements of `info_list`.
			:param bool check_order_id: If `True`, the function will check whether an order	with given UUID
				exists. Note that "id" must be an element of `info_list`.
			:param bool site_check: If `True`, the function will check whether a site with given UUID exists, and check
				user permission according to site management logic. Note that "id" must be an element of `info_list`.

		Returns:
			Return a parsed dict if all the tests are passed, or else return an error response.
	"""
	if request.method != method:
		return gen_response(405, "非法请求")

	if user_auth and not request.user.is_authenticated:
		return gen_response(401, USER_NOT_LOGIN)

	if privilege_list is not None and request.user.profile.privilege not in privilege_list:
		return gen_response(400, USER_PERMISSION_DENIED)

	if info_list is None:
		return None
	if method == "POST":
		try:
			message = json.loads(request.body)
		except json.JSONDecodeError:
			return gen_response(400, "json解析失败")
		try:
			info = message["data"]
		except KeyError:
			return gen_response(400, JSON_DATA_FIELD_INVALID)
	else:
		info = request.GET

	if not check_info(info_list, info):
		return gen_response(400, "data中缺少必要的元素")

	if "email" in info and info["email"] != "" and not verify_email(info["email"]):
		return gen_response(400, "邮箱不合法")
	if "telephone" in info and info["telephone"] != "" and not verify_telephone(info["telephone"]):
		return gen_response(400, "电话号码不合法")
	if "privilege" in info and info["privilege"] not in range(4):
		return gen_response(400, "用户权限类型不合法")

	for value in stringify_list:
		info[value] = str(info[value])
	for value in empty_check_list:
		if info[value] == "":
			return gen_response(400, "%s不能为空" % FIELD_META[value][0])
	for value in length_limit_list:
		if len(info[value]) > FIELD_META[value][1]:
			return gen_response(400, "%s过长" % FIELD_META[value][0])

	if check_username_existence and not User.objects.filter(username=info["username"]):
		return gen_response(400, "用户名不存在")

	if check_contact and info["email"] == "" and info["telephone"] == "":
		return gen_response(400, "邮箱和电话必须留其一")

	if check_order_id and not Order.objects.filter(uuid=info["id"]):
		return gen_response(400, "不存在指定id的订单")

	if site_check:
		if not Site.objects.filter(uuid=info["id"]):
			return gen_response(400, "不存在指定id的网站")
		site = Site.objects.get(uuid=info["id"])
		if site.order.owner.user != request.user and request.user.profile.privilege not in [ADMIN, OPERATIONS_ENGINEER]:
			return gen_response(400, USER_PERMISSION_DENIED)

	return info


def modify(data: dict, key: str, value):
	"""
		Create a modified copy of a dict by "data[key] = value".

		Args:
			:param dict data: The dict.
			:param str key: Data field which needs to be modified.
			:param value: New assigned value.

		Returns:
			The modified dict.
	"""
	ret = data.copy()
	ret[key] = value
	return ret


def create_site_by_order(order: Order):
	site_message = NCE_campus.create_site({
		"name": order.site.name,
		"description": order.site.name,
		"latitude": "40.0",  # fake
		"longtitude": "116.33",  # fake
		"contact": order.owner.name,
		"email": order.owner.email,
		"phone": order.owner.telephone,
		"postcode": "100084",  # fake
		"address": order.site.address
	})
	# sites_message["result"] = True / False
	# sites_message["id"] is the site_id
	return site_message


def create_devices_by_order(order: Order, site_id):
	"""
	The device name is the same as the network name
	"""
	devices_message = []
	for network in order.network_set.all():
		esn = ""
		device_model = "AP4050DN"
		devices_message.append(NCE_campus.create_device({
			"esn": esn,
			"siteId": site_id,
			"name": network.name,
			"deviceModel": device_model
		}))
		if devices_message[-1]["result"]:
			Device.objects.create(
				esn=esn,
				uuid=devices_message[-1]["id"],
				device_model=device_model,
				network=network
			)

	# devices_message[]["result"] = True / False
	# devices_message[]["id"] is the device_id
	return devices_message


def get_bill_list(user_profile: UserProfile):
	bill_list = []
	if user_profile.privilege != OPERATIONS_ENGINEER:
		order_set = user_profile.order_set.all()
	else:
		order_set = Order.objects.all()

	for order in order_set:
		if order.state == ORDER_CLOSED:
			flow_overused = order.site.flow - order.site.flow_threshold
			fee = flow_overused * FEE_PER_KB
			if flow_overused > 0:
				bill_list.append({
					"siteName": order.site.name,
					"siteId": order.site.uuid,
					"billingMethod": order.billing_method,
					"fee": fee,
					"flowOverused": flow_overused
				})
	return bill_list


def get_fee_by_user(user_profile: UserProfile):
	bill_list = get_bill_list(user_profile)

	fee_sum = 0
	for bill in bill_list:
		fee_sum += bill["fee"]
	return fee_sum


def send_email_to_user(user_profile: UserProfile):
	if not user_profile.email:
		return False

	bill_list = get_bill_list(user_profile)

	fee_sum = 0
	flow_overused_sum = 0
	for bill in bill_list:
		fee_sum += bill["fee"]
		flow_overused_sum += bill["flowOverused"]

	localtime = time.asctime(time.localtime(time.time()))

	title = "您的账单"
	message = """
		亲爱的 {0} ({1}),
		您好！截止至 {2}，您创建的站点共计超额流量 {3}MB，欠费 {4} 元。
		查询详情请登录https://huawei-net-access-oneholdsthree.app.secoder.net，感谢您的使用。
		OneHoldsThree
	""".format(user_profile.user.username, user_profile.name, localtime, flow_overused_sum/1000, fee_sum)

	send_mail(title, message, "OneHoldsThree@163.com", [user_profile.email], fail_silently=False)


def random_load(upper_bound: int):
	if time.localtime().tm_hour not in range(8, 24):
		upper_bound //= 10
	return randint(0, upper_bound)
