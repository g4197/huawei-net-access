from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.middleware.csrf import get_token
from .config import GUEST, NETWORK_ENGINEER, ADMIN, OPERATIONS_ENGINEER, USER_NOT_LOGIN, USER_PERMISSION_DENIED, \
	JSON_DATA_FIELD_INVALID, ORDER_SUBMITTED, ORDER_SURVEYED, ORDER_CLOSED, ORDER_CANCELLED, ORDER_DEPLOYED,\
	FEE_PER_KB
from .models import UserProfile, Order, Network, Site, SSID, SSIDAuth, Device
from .utils import gen_response, userprofile_to_dict, ssid_to_dict, order_to_dict, check_and_parse,\
	create_site_by_order, create_devices_by_order, modify, get_bill_list
from . import NCE_campus


def register(request):
	ret = check_and_parse(
		"POST", request,
		info_list=["username", "password", "email", "name", "telephone", "address"],
		stringify_list=["username", "password", "email", "name", "telephone", "address"],
		empty_check_list=["name", "username", "address"],
		length_limit_list=["email", "telephone", "name", "username", "address", "password"],
		check_contact=True
	)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	if User.objects.filter(username=ret["username"]):  # the username is existed
		return gen_response(400, "用户名已存在")

	UserProfile.objects.create(
		user=User.objects.create_user(
			username=ret["username"],
			password=ret["password"],
		),
		email=ret["email"],
		name=ret["name"],
		telephone=ret["telephone"],
		address=ret["address"],
		privilege=GUEST,
	)
	return gen_response(201, "注册成功")


def login(request):
	ret = check_and_parse(
		"POST", request,
		info_list=["username", "password"],
		stringify_list=["username", "password"],
		check_username_existence=True
	)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	if request.user.is_authenticated:
		return gen_response(403, "用户已登录")
	user = auth.authenticate(username=ret["username"], password=ret["password"])
	if not user:
		return gen_response(400, "用户名错误或密码错误")
	auth.login(request, user)
	return gen_response(200, "成功登录")


def logout(request):
	if not request.user.is_authenticated:
		return gen_response(401, USER_NOT_LOGIN)
	auth.logout(request)
	return gen_response(200, "成功注销")


def get_csrf_token(request):
	get_token(request)
	return JsonResponse({})


def submit_order(request):
	ret = check_and_parse(
		"POST", request,
		info_list=[
			"site_name",
			"site_address",
			"billing_method",
			"network_demand",
			"flow_threshold"
		],
		stringify_list=["site_name", "site_address"],
		empty_check_list=["site_name", "site_address"],
		length_limit_list=["site_name", "site_address"],
		user_auth=True
	)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	if ret["billing_method"] not in range(2):
		return gen_response(400, "计费方式有误")
	if type(ret["network_demand"]) != list:
		return gen_response(400, "基础网络需求类型有误")

	network_demand_guest = ("Guest" in ret["network_demand"])
	network_demand_management = ("Management" in ret["network_demand"])
	network_demand_test = ("Test" in ret["network_demand"])
	if network_demand_guest == 0 and network_demand_management == 0 and network_demand_test == 0:
		return gen_response(400, "基础网络需求中缺少指定的类型")
	if int(ret["flow_threshold"]) not in range(0, 2 ** 63):
		return gen_response(400, "流量限制范围异常")

	order = Order.objects.create(
		owner=request.user.profile,
		billing_method=ret["billing_method"],
		network_demand_guest=network_demand_guest,
		network_demand_management=network_demand_management,
		network_demand_test=network_demand_test,
		state=ORDER_SUBMITTED
	)
	Site.objects.create(
		name=ret["site_name"],
		address=ret["site_address"],
		flow_threshold=int(ret["flow_threshold"]),
		order=order
	)
	return gen_response(201, "成功创建订单")


def get_userprofile(request):
	ret = check_and_parse("GET", request, user_auth=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	user_profile = request.user.profile
	return gen_response(
		code=200,
		message="成功返回用户信息",
		data={"userprofile": userprofile_to_dict(user_profile)}
	)


def get_order_information(request):
	ret = check_and_parse("GET", request, user_auth=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	user_profile = request.user.profile

	if user_profile.privilege in [NETWORK_ENGINEER, ADMIN]:
		order_list = [order_to_dict(order) for order in Order.objects.all()]
	else:
		order_list = [order_to_dict(order) for order in user_profile.order_set.all()]

	return gen_response(
		code=200,
		message="成功返回订单信息",
		data={"orders": order_list}
	)


def cancel_order(request):
	ret = check_and_parse(
		"POST", request,
		info_list=["id", "reason"],
		length_limit_list=["reason"],
		user_auth=True,
		check_order_id=True
	)
	# reason may be ""
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	order = Order.objects.get(uuid=ret["id"])
	if order.state == ORDER_CLOSED:
		return gen_response(400, "订单已为关闭状态，无法取消")
	if order.state == ORDER_CANCELLED:
		return gen_response(400, "订单已为取消状态")

	# order has been deployed
	user_profile = request.user.profile
	if user_profile.privilege == GUEST and order.state in [ORDER_SURVEYED, ORDER_DEPLOYED]:
		return gen_response(400, "订单已被工勘，您无法取消该订单了")

	# delete the sites and devices
	# TODO: if user restore order after deleting ?
	if user_profile.privilege == NETWORK_ENGINEER and order.state == ORDER_DEPLOYED:
		devices = []
		for network in order.network_set.all():
			devices.append(network.device.uuid)
		NCE_campus.delete_devices(devices)

		NCE_campus.delete_sites([order.site.uuid])

		for uuid in devices:
			device = Device.objects.filter(uuid=uuid)
			if device:
				device[0].delete()

	order.last_state = order.state
	order.state = ORDER_CANCELLED
	order.reason = ret["reason"]
	# reason of cancellation
	order.save()
	return gen_response(201, "成功取消订单")


def restore_order(request):
	ret = check_and_parse("POST", request, info_list=["id"], user_auth=True, check_order_id=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	order = Order.objects.get(uuid=ret["id"])
	if order.state != ORDER_CANCELLED:
		return gen_response(400, "订单暂未取消, 无法恢复")

	# I haven't figured it out yet
	if order.last_state == ORDER_DEPLOYED:
		# restore to ORDER_SURVEYED
		order.last_state = ORDER_SURVEYED

	order.state = order.last_state
	order.save()
	return gen_response(201, "成功恢复订单")


def close_order(request):
	ret = check_and_parse("POST", request, info_list=["id"], user_auth=True, check_order_id=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	order = Order.objects.get(uuid=ret["id"])
	if order.state == ORDER_CLOSED:
		return gen_response(400, "订单已为关闭状态")
	order.state = ORDER_CLOSED
	order.save()
	return gen_response(201, "操作成功")


def get_single_order_information(request):
	ret = check_and_parse("GET", request, info_list=["id"], user_auth=True, check_order_id=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	order = Order.objects.get(uuid=ret["id"])
	if order.owner.user != request.user and request.user.profile.privilege == GUEST:
		return gen_response(401, USER_PERMISSION_DENIED)
	return gen_response(
		code=200,
		message="成功返回单个订单信息",
		data=order_to_dict(order, need_network_list=True, need_ssid_list=True)
	)


def survey_order(request):
	ret = check_and_parse(
		"POST", request,
		info_list=["id", "network_list", "ssid_list"],
		privilege_list=[NETWORK_ENGINEER, ADMIN],
		user_auth=True, check_order_id=True
	)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	order = Order.objects.get(uuid=ret["id"])
	if order.state != ORDER_SUBMITTED:
		return gen_response(400, "订单状态不合法")
	if type(ret["network_list"]) != list or type(ret["ssid_list"]) != list:
		return gen_response(400, JSON_DATA_FIELD_INVALID)

	name_set = set()
	for network in ret["network_list"]:
		try:
			if len(str(network["name"])) > Network._meta.get_field("name").max_length:
				return gen_response(400, "网络名称过长")
			if len(str(network["name"])) == 0:
				return gen_response(400, "网络名称不能为空")
			if network["name"] in name_set or Network.objects.filter(name=network["name"]):
				return gen_response(400, "网络名称重复")
			name_set.add(network["name"])
		except (KeyError, TypeError):
			return gen_response(400, JSON_DATA_FIELD_INVALID)

	for ssid in ret["ssid_list"]:
		try:
			# TODO: stringify
			# TODO: name check
			if len(ssid["name"]) > SSID._meta.get_field("name").max_length:
				return gen_response(400, "SSID名称过长")
			if ssid["connection_mode"] not in ["bridge", "nat"]:
				return gen_response(400, "网络连接方式不合法")
			if ssid["relative_radios"] not in range(1, 8):
				return gen_response(400, "射频类型不合法")
			if ssid["max_user_number"] not in range(1, 513):
				return gen_response(400, "最大用户数不合法")
			auth_mode = ssid["auth_mode"]
			if auth_mode not in ["open", "psk", "ppsk", "dot1x", "mac"]:
				return gen_response(400, "SSID认证模式不合法")
			if auth_mode in ["psk", "ppsk"]:
				encrypt_type = ssid["auth_psk_encrypt_type"]
				if encrypt_type not in ["wep", "wpa1AndWpa2", "wpa2"] or auth_mode == "ppsk" and encrypt_type == "wep":
					return gen_response(400, "psk认证方式下的加密模式不合法")
				# TODO: security key check
				if auth_mode == "psk":
					security_key = ssid["auth_security_key"]
					if encrypt_type == "wep" and len(security_key) != 5 or\
						encrypt_type != "wep" and len(security_key) not in range(8, 64):
						return gen_response(400, "psk密钥不合法")
				elif "auth_mac_auto_binding" not in ssid:
					return gen_response(400, "缺少MAC自动绑定选项")
				if encrypt_type == "wpa2" and ssid["auth_security_key_type"] not in ["AES", "AES-TKIP", "TKIP"]:
					return gen_response(400, "加密方法不合法")
			elif auth_mode == "dot1x" and ssid["auth_dot1x_encrypt_type"] not in ["wpa1AndWpa2", "wpa2"]:
				return gen_response(400, "dot1x加密模式不合法")
		except (KeyError, TypeError):
			return gen_response(400, JSON_DATA_FIELD_INVALID)

	for network_name in name_set:
		Network.objects.create(
			order=order,
			name=str(network_name)
		)
	order.state = ORDER_SURVEYED
	order.save()
	for info in ret["ssid_list"]:
		ssid = SSID.objects.create(
			name=info["name"],
			enable=info["enable"],
			connection_mode=info["connection_mode"],
			hid_enable=info["hid_enable"],
			relative_radios=info["relative_radios"],
			max_user_number=info["max_user_number"],
			user_separation=info["user_separation"],
			order=order
		)
		auth_mode = info["auth_mode"]
		psk_encrypt_type, security_key, security_key_type, dot1x_encrypt_type = "", "", "", ""
		mac_auto_binding = False
		if auth_mode == "psk":
			psk_encrypt_type = info["auth_psk_encrypt_type"]
		elif auth_mode == "dot1x":
			dot1x_encrypt_type = info["auth_dot1x_encrypt_type"]
		if "auth_mac_auto_binding" in info:
			mac_auto_binding = info["auth_mac_auto_binding"]
		if "auth_security_key" in info:
			security_key = info["auth_security_key"]
		if "auth_security_key_type" in info:
			security_key_type = info["auth_security_key_type"]
		SSIDAuth.objects.create(
			mode=auth_mode,
			psk_encrypt_type=psk_encrypt_type,
			security_key=security_key,
			security_key_type=security_key_type,
			dot1x_encrypt_type=dot1x_encrypt_type,
			mac_auto_binding=mac_auto_binding,
			ssid=ssid
		)

	return gen_response(201, "工勘成功")


def modify_password(request):
	ret = check_and_parse(
		"POST", request,
		info_list=["username", "original_password", "password", "check_password"],
		length_limit_list=["password"],
		empty_check_list=["password"],
		user_auth=True,
		check_username_existence=True
	)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	if request.user.profile.privilege == ADMIN:
		user = User.objects.get(username=ret["username"])
	else:
		if request.user.username != ret["username"]:
			return gen_response(400, USER_PERMISSION_DENIED)
		user = auth.authenticate(username=ret["username"], password=ret["original_password"])
		if not user:
			return gen_response(400, "用户名错误或密码错误")
	if ret["password"] != ret["check_password"]:
		return gen_response(400, "两次输入的密码不一致")
	user.set_password(ret["password"])
	user.save()
	return gen_response(201, "密码修改成功")


def modify_userprofile(request):
	ret = check_and_parse(
		"POST", request,
		info_list=["username", "email", "name", "telephone", "address", "privilege"],
		stringify_list=["username", "email", "name", "telephone", "address"],
		empty_check_list=["name", "username", "address"],
		length_limit_list=["email", "telephone", "name", "username", "address"],
		user_auth=True,
		check_username_existence=True,
		check_contact=True
	)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	if request.user.profile.privilege != ADMIN and request.user.username != ret["username"] or\
		request.user.profile.privilege != ADMIN and request.user.profile.privilege != ret["privilege"]:
		return gen_response(400, USER_PERMISSION_DENIED)
	profile = User.objects.get(username=ret["username"]).profile
	profile.email, profile.telephone = ret["email"], ret["telephone"]
	profile.name, profile.address = ret["name"], ret["address"]
	profile.privilege = ret["privilege"]
	profile.save()
	return gen_response(201, "用户信息修改成功")


def get_user_list(request):
	ret = check_and_parse("GET", request, privilege_list=[ADMIN], user_auth=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	return gen_response(
		code=200,
		message="成功返回用户列表",
		data={"userprofile": [userprofile_to_dict(profile) for profile in UserProfile.objects.all()]}
	)


def deploy_order(request):
	"""
	Creating sites and devices. User can view site and device information by function get_sites and get_devices
	"id" is the uuid of order that need to be deployed

	:param request:
	:return:
	"""
	ret = check_and_parse(
		"POST", request,
		info_list=["id"],
		privilege_list=[NETWORK_ENGINEER, ADMIN],
		user_auth=True, check_order_id=True
	)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	order = Order.objects.get(uuid=ret["id"])
	if order.state != ORDER_SURVEYED:
		return gen_response(400, "已工勘的订单才能部署")

	site_message = create_site_by_order(order)
	if not site_message["result"]:
		return gen_response(400, site_message["errmsg"])  # The site name is already in use
	order.site.uuid = site_message["id"]
	order.site.max_user_number_cnt = sum([x.max_user_number for x in order.ssid_set.all()])
	order.site.save()

	create_devices_by_order(order, site_message["id"])
	# device_message
	# Since the network name has been deduplicated and the device is distinguished by name,
	# the creation of devices will be successful.
	# device_message[index]["result"] == False is impossible

	order.state = ORDER_DEPLOYED
	order.save()
	return gen_response(201, "部署成功")


def get_sites(request):
	ret = check_and_parse("GET", request, user_auth=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	user_profile = request.user.profile

	if user_profile.privilege != OPERATIONS_ENGINEER:
		order_set = user_profile.order_set.all()
	else:
		order_set = Order.objects.all()
	site_list = []

	for order in order_set:
		if order.state == ORDER_CLOSED:
			return_sites = NCE_campus.get_sites(uuid=order.site.uuid)
			if return_sites:
				site_list.append(modify(return_sites[0], "flowLimitExceeded", order.site.flow_limit_exceeded))

	return gen_response(
		code=200,
		message="成功返回站点信息",
		data={"sites": site_list}
	)


def get_devices(request):
	"""
	Get devices by id of site
	:param request:
	:return:
	"""
	ret = check_and_parse("GET", request, info_list=["id"], user_auth=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	device_list = NCE_campus.get_devices(site_id=ret["id"])

	return gen_response(
		code=200,
		message="成功返回设备信息",
		data={"devices": device_list}
	)


def get_single_site_information(request):
	ret = check_and_parse("GET", request, info_list=["id"], user_auth=True, site_check=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	site = Site.objects.get(uuid=ret["id"])
	site_info = NCE_campus.get_sites(uuid=ret["id"])[0]
	site_info["upSpeed"], site_info["downSpeed"] = site.upload_speed, site.download_speed
	site_info["flow"], site_info["flowThreshold"] = site.flow, site.flow_threshold
	site_info["onlineUserCnt"], site_info["maxUserNumberCnt"] = site.online_user_cnt, site.max_user_number_cnt
	site_info["flowLimitExceeded"] = site.flow_limit_exceeded

	return gen_response(
		code=200,
		message="成功返回单个网站信息",
		data=site_info
	)


def get_bill(request):
	ret = check_and_parse("GET", request, user_auth=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	user_profile = request.user.profile
	bill_list = get_bill_list(user_profile)
	# get_bill_list will judge user_profile's privilege

	return gen_response(
		code=200,
		message="成功返回账单",
		data={
			"Bill": bill_list
		}
	)


def get_ssid(request):
	ret = check_and_parse("GET", request, info_list=["id"], user_auth=True, site_check=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	site = Site.objects.get(uuid=ret["id"])
	return gen_response(
		code=200,
		message="成功返回SSID信息",
		data={"ssid_list": [ssid_to_dict(ssid) for ssid in site.order.ssid_set.all()]}
	)


def get_statistics(request):
	ret = check_and_parse("GET", request, info_list=["id"], user_auth=True, site_check=True)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	site = Site.objects.get(uuid=ret["id"])
	return gen_response(
		code=200,
		message="成功返回统计信息",
		data={
			"online": [
				{"time": record.time.timestamp(), "value": record.online_user_cnt}
				for record in site.siterecord_set.all()
			],
			"upSpeed": [
				{"time": record.time.timestamp(), "value": record.upload_speed}
				for record in site.siterecord_set.all()
			],
			"downSpeed": [
				{"time": record.time.timestamp(), "value": record.download_speed}
				for record in site.siterecord_set.all()
			],
			"flow": [
				{"time": record.time.timestamp(), "value": record.flow / 1024}
				for record in site.siterecord_set.all()
			],
		}
	)


def pay(request):
	"""
	Given an id of site, only operations engineer could pay it.
	:param request:
	:return:
	"""
	ret = check_and_parse(
		"POST", request,
		info_list=["id"],
		user_auth=True
	)
	if ret.__class__.__name__ == "JsonResponse":
		return ret

	user_profile = request.user.profile
	if user_profile.privilege != OPERATIONS_ENGINEER:
		return gen_response(400, "请联系运营工程师进行缴费")

	site = Site.objects.get(uuid=ret["id"])
	site.flow_threshold *= 2
	site.flow_limit_exceeded = False
	site.save()

	return gen_response(
		code=200,
		message="缴费成功"
	)
