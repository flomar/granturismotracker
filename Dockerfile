FROM ubuntu:latest

RUN DEBIAN_FRONTEND=noninteractive rm -rf /var/lib/apt/lists/*
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y --fix-missing
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx-full python3 python3-pip sqlite3 uwsgi uwsgi-plugin-python3 vim

WORKDIR .

RUN mkdir ./granturismotracker

COPY ./requirements.txt ./granturismotracker/requirements.txt

WORKDIR ./granturismotracker

RUN pip install -r requirements.txt

COPY ./granturismotracker/ ./granturismotracker/
COPY ./wsgi.ini ./wsgi.ini
COPY ./nginx.ini /usr/share/nginx/nginx.ini
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
