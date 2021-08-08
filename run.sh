export DJANGO_SETTINGS_MODULE="backend.settings_deployment"
echo 'DJANGO_SETTINGS_MODULE="backend.settings_deployment"' >> /var/spool/cron/crontabs/root
service cron start
python3 /var/backend/manage.py makemigrations
python3 /var/backend/manage.py migrate
python3 /var/backend/manage.py crontab add .
python3 /var/backend/manage.py crontab add .
service nginx stop
uwsgi --ini /var/backend/script/uwsgi.ini
nginx -g "daemon off;"
while true; do sleep 1d; done
