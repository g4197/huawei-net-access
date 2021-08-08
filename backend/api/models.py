from django.db import models
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	name = models.CharField(max_length=50)
	telephone = models.CharField(max_length=50, blank=True)
	email = models.CharField(max_length=50, blank=True)  # use this email, not the one in User
	address = models.CharField(max_length=100)
	privilege = models.IntegerField(default=0)
	# 0 means guest, 1 means network engineer, 2 means operations engineer, 3 means admin

	def __str__(self):
		return self.user.__str__()


class Order(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  # An order belongs to only one user
	billing_method = models.BooleanField(default=0)  # 0 means annually and 1 means monthly
	network_demand_guest = models.BooleanField(default=0)
	network_demand_management = models.BooleanField(default=0)
	network_demand_test = models.BooleanField(default=0)
	state = models.IntegerField(default=0)
	"""
	state: int
	0 means the order has been submitted, 1 means the order has been surveyed,
	2 means the order has been deployed, 3 means the order has been closed,
	4 means the order has been cancelled
	"""
	last_state = models.IntegerField(default=0)
	# the last_state represents the state before the order was cancelled
	reason = models.CharField(default="", max_length=500)
	# the reason of cancellation


class Network(models.Model):
	name = models.CharField(max_length=100)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)


class SSID(models.Model):
	name = models.CharField(max_length=32)
	enable = models.BooleanField(default=True)
	connection_mode = models.CharField(max_length=10, default="nat")  # "bridge" or "nat"
	hid_enable = models.BooleanField(default=False)
	relative_radios = models.IntegerField(default=3)  # 1~7
	max_user_number = models.IntegerField(default=10)  # 1~512
	user_separation = models.BooleanField(default=False)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)


class SSIDAuth(models.Model):
	mode = models.CharField(max_length=10, default="ppsk")  # "open", "psk", "ppsk", "dot1x" or "mac"
	psk_encrypt_type = models.CharField(max_length=20, default="wpa2")  # "wep", "wpa1AndWpa2" or "wpa2"
	security_key = models.CharField(max_length=63)
	security_key_type = models.CharField(max_length=10, default="AES")  # "AES", "AES-TKIP" or "TKIP"
	dot1x_encrypt_type = models.CharField(max_length=20)  # "wpa1AndWpa2" or "wpa2"
	mac_auto_binding = models.BooleanField()
	ssid = models.OneToOneField(SSID, on_delete=models.CASCADE, related_name="auth")


class Site(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100)
	uuid = models.CharField(max_length=100)
	order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="site")
	upload_speed = models.IntegerField(default=0)
	download_speed = models.IntegerField(default=0)
	flow = models.BigIntegerField(default=0)  # KB
	flow_threshold = models.BigIntegerField()
	online_user_cnt = models.IntegerField(default=0)
	max_user_number_cnt = models.IntegerField(default=0)
	flow_limit_exceeded = models.BooleanField(default=False)


class Device(models.Model):
	esn = models.CharField(max_length=50)
	uuid = models.CharField(max_length=100)
	# name is the same as device.network.name
	# siteId is the same as device.network.order.site.uuid
	device_model = models.CharField(max_length=20)
	network = models.OneToOneField(Network, on_delete=models.CASCADE, related_name="device")


class SiteRecord(models.Model):
	online_user_cnt = models.IntegerField(default=0)
	upload_speed = models.IntegerField(default=0)
	download_speed = models.IntegerField(default=0)
	flow = models.BigIntegerField(default=0)
	time = models.DateTimeField(auto_now_add=True)
	site = models.ForeignKey(Site, on_delete=models.CASCADE)
