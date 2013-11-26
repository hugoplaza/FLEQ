#!/bin/bash
cd /pfc-jgonzalez-data/home/jgonzalez/virtualenvs/fleq/fleq
#source ../bin/activate
exec gunicorn_django
