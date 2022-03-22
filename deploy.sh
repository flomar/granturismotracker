#!/bin/bash

mkdir -p /home/$(whoami)/.granturismotracker
touch /home/$(whoami)/.granturismotracker/granturismotracker.sqlite
docker-compose -f docker-compose.yml build && HOME=/home/$(whoami) docker-compose -f docker-compose.yml up &
