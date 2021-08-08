FROM nginx

# change source to TUNA
RUN apt update
RUN apt install -y gpg
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 40976EAF437D05B5
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3B4FE6ACC0B21F32
COPY config/sources.list /etc/apt/sources.list

# install necessary libs
RUN apt update
RUN apt-get install -y curl
RUN apt-get install -y cron
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
COPY requirements.txt /var/requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /var/requirements.txt
RUN curl -fsSL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs

# copy and build frontend and backend files
COPY backend /var/backend
COPY frontend /var/frontend-src
RUN cd /var/frontend-src && npm ci && npm run build && cp -r /var/frontend-src/dist /var/frontend
RUN rm -rf /var/frontend-src

EXPOSE 80

# backend with uwsgi
RUN mkdir /var/backend/script
COPY config/uwsgi.ini /var/backend/script/uwsgi.ini

# nginx
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY run.sh /var/run.sh

CMD ["/bin/sh", "/var/run.sh"]
