#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings
setup_environ(settings)

import os
import sys
import time
import random
import datetime
from selenium import webdriver
#from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from quizbowl.models import Category, Game, Question, Score, UserProfile
from quizbowl.views import notify_user
from django.utils.html import escape
from django.contrib.auth.models import User


NUM_CORRECT = 10
QUESTIONS = 20

HOST = "http://pfc-clavado.libresoft.es"


# Set up codec
reload(sys)
sys.setdefaultencoding("utf-8")

os.environ['DISPLAY'] = ':6801'

#browser = webdriver.PhantomJS(executable_path='/pfc-jgonzalez-data/home/jgonzalez/virtualenvs/fleq/fleq/phantomjs/bin/phantomjs') 
browser = webdriver.Firefox()

# Log in FLEQ as FLEQBOT
print "Accediendo a la pantalla incial para hacer login..."
browser.get(HOST)

elem = browser.find_element_by_name("username")
elem.send_keys("FLEQBOT")
elem = browser.find_element_by_name("password")
elem.send_keys("F13B0t")

print "Logueando..."
elem = browser.find_element_by_class_name("button").send_keys(Keys.RETURN)
time.sleep(5)

print "Donde esta el robot ahora (deberia estar en /next-games)" 
print browser.current_url

# Go to Game window
print "Accediendo a la ventana de juego 2 (por defecto)..."
browser.get(HOST + "/game-room/2")
time.sleep(5)

print "Donde esta el robot ahora (deberia estar en /game-room/2)"
print browser.current_url
print "Si no esta en /game-room/2 va a petar porque no encuentra el elemento con name igual a message"

time.sleep(5)

elem = browser.find_element_by_name("message")

time.sleep(10)
elem.send_keys('Quedan 2 minutos...' +  Keys.RETURN)

time.sleep(2)
browser.close()
