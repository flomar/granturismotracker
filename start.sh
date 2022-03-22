#!/bin/bash

nginx -c nginx.ini && uwsgi wsgi.ini
