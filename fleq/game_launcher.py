#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings

setup_environ(settings)

from quizbowl.models import Category, Game, Question
import codecs
import datetime
import os
import random
import subprocess


three_minutes_ahead = datetime.datetime.now() + datetime.timedelta(minutes=3)  # datetime X minutes ahead from now
g = Game.objects.filter(start_time__lte = three_minutes_ahead, start_time__gte = datetime.datetime.now())


for game in g:
    
    if not game.is_over():
	#subprocess.Popen(['python', '/home/jgonzalez/virtualenvs/fleq/fleq/fleqbot.py', str(game.id)])
        subprocess.Popen(['python', '/pfc-jgonzalez-data/home/jgonzalez/virtualenvs/fleq/fleq/websocket-client.py', str(game.id)])
        
