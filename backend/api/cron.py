from .models import Site, UserProfile, SiteRecord
from . import config
from .utils import get_fee_by_user, send_email_to_user, random_load


def update_flow():
	for site in Site.objects.all():
		if site.order.state == config.ORDER_CLOSED:
			if site.flow_limit_exceeded:
				site.upload_speed, site.download_speed, site.online_user_cnt = 0, 0, 0
			else:
				site.upload_speed = random_load(config.MAXIMUM_SPEED)
				site.download_speed = random_load(config.MAXIMUM_SPEED)
				site.flow += (site.upload_speed + site.download_speed) * config.SECONDS_PER_SIMULATE
				site.flow_limit_exceeded = (site.flow > site.flow_threshold)
				site.online_user_cnt = random_load(site.max_user_number_cnt)
			site.save()
			SiteRecord(
				online_user_cnt=site.online_user_cnt,
				upload_speed=site.upload_speed,
				download_speed=site.download_speed,
				flow=site.flow,
				site=site
			).save()


def send_email():
	for user_profile in UserProfile.objects.all():
		send_email_to_user(user_profile)
