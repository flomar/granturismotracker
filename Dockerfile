FROM ubuntu:latest

RUN DEBIAN_FRONTEND=noninteractive rm -rf /var/lib/apt/lists/*
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y --fix-missing
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx-full python3 python3-pip sqlite3 uwsgi uwsgi-plugin-python3 vim

WORKDIR .

RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime

RUN mkdir ./granturismotracker

WORKDIR ./granturismotracker

COPY ./granturismotracker.py ./granturismotracker.py
COPY ./granturismotracker/ ./granturismotracker/
COPY ./configuration/wsgi.ini ./configuration/wsgi.ini
COPY ./configuration/nginx.ini /usr/share/nginx/nginx.ini
COPY ./start.sh /start.sh

COPY ./requirements/requirements.txt ./requirements/requirements.txt
RUN pip install -r ./requirements/requirements.txt

RUN chmod +x /start.sh
CMD ["/start.sh"]
