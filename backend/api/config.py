from .models import UserProfile, Site, Order

# constant parameters
USERNAME_MAX_LENGTH = 150
PASSWORD_MAX_LENGTH = 150

# message constant strings
USER_NOT_LOGIN = "用户未登录"
JSON_DATA_FIELD_INVALID = "json键值不合法"
USER_PERMISSION_DENIED = "用户权限不足"

# "English name": ("Chinese name": max_length)
FIELD_META = {
	"username": ("用户名", USERNAME_MAX_LENGTH),
	"password": ("密码", PASSWORD_MAX_LENGTH),
	"email": ("邮箱", UserProfile._meta.get_field("email").max_length),
	"telephone": ("电话", UserProfile._meta.get_field("telephone").max_length),
	"name": ("公司名称", UserProfile._meta.get_field("name").max_length),
	"address": ("地址", UserProfile._meta.get_field("address").max_length),
	"site_name": ("站点名称", Site._meta.get_field("name").max_length),
	"site_address": ("站点地址", Site._meta.get_field("address").max_length),
	"reason": ("取消原因", Order._meta.get_field("reason").max_length)
}

# state constant integers
ORDER_SUBMITTED = 0
ORDER_SURVEYED = 1
ORDER_DEPLOYED = 2
ORDER_CLOSED = 3
ORDER_CANCELLED = 4
GUEST = 0
NETWORK_ENGINEER = 1
OPERATIONS_ENGINEER = 2
ADMIN = 3

# guess what?
MAGIC_NUMBER = "a7ab43256baafb202b2b11f3418aae4d"

# network speed simulation
FEE_PER_KB = 0.06 / 1024
# 1MB: 0.06 yuan

SECONDS_PER_SIMULATE = 60
MAXIMUM_SPEED = 1024  # in KB