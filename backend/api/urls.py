from . import views
from django.urls import path
from .models import User, UserProfile
from .config import ADMIN, MAGIC_NUMBER

urlpatterns = [
	path("login", views.login, name="login"),
	path("register", views.register, name="register"),
	path("logout", views.logout, name="logout"),
	path("get_csrf_token", views.get_csrf_token, name="get_csrf_token"),
	path("submit_order", views.submit_order, name="submit_order"),
	path("get_userprofile", views.get_userprofile, name="get_userprofile"),
	path("get_order_information", views.get_order_information, name="get_order_information"),
	path("cancel_order", views.cancel_order, name="cancel_order"),
	path("restore_order", views.restore_order, name="restore_order"),
	path("close_order", views.close_order, name="close_order"),
	path("get_single_order_information", views.get_single_order_information, name="get_single_order_information"),
	path("survey_order", views.survey_order, name="survey_order"),
	path("modify_password", views.modify_password, name="modify_password"),
	path("modify_userprofile", views.modify_userprofile, name="modify_userprofile"),
	path("get_user_list", views.get_user_list, name="get_user_list"),
	path("deploy_order", views.deploy_order, name="deploy_order"),
	path("get_sites", views.get_sites, name="get_sites"),
	path("get_devices", views.get_devices, name="get_devices"),
	path("get_single_site_information", views.get_single_site_information, name="get_single_site_information"),
	path("get_bill", views.get_bill, name="get_bill"),
	path("get_ssid", views.get_ssid, name="get_ssid"),
	path("get_statistics", views.get_statistics, name="get_statistics"),
	path("pay", views.pay, name="pay"),
]

# Create admin at the beginning
try:
	UserProfile.objects.create(
		user=User.objects.create_user(
			username="admin",
			password=MAGIC_NUMBER,
		),
		email="cfhmgh@163.com",
		name="Hao Guo",
		telephone="1234567890",
		address="0987654321",
		privilege=ADMIN,
	)
except:
	pass
