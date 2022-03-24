#!/bin/bash

nginx -c nginx.ini && uwsgi configuration/wsgi.ini
