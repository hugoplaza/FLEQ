#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
#  FLEQ (Free LibreSoft Educational Quizbowl)                               #
#  A synchronous on-line competition software to improve and                #
#  motivate learning.                                                       #
#                                                                           #
#  Copyright (C) 2012  Arturo Moral, Gregorio Robles & Felix Redondo        #
#                                                                           #
#  This program is free software: you can redistribute it and/or modify     #
#  it under the terms of the GNU Affero General Public License as           #
#  published by the Free Software Foundation, either version 3 of the       #
#  License, or (at your option) any later version.                          #
#                                                                           #
#  This program is distributed in the hope that it will be useful,          #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #       
#  GNU Affero General Public License for more details.                      #
#                                                                           #
#  You should have received a copy of the GNU Affero General Public License #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                           #
#  Contact authors : Arturo Moral <amoral@gmail.com>                        #
#                    Gregorio Robles <grex@gsyc.urjc.es>                    #
#                    Felix Redondo <felix.redondo.sierra@gmail.com>	    #
#                                                                           #
#############################################################################

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                     #
#  - El script se lanza a las *:30				      #
#                                                                     #
#         ####                             ####                       #
#                                                                     #
#                       @@@@@@@@@@                                    #
#                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

from django.core.management import setup_environ
import settings

setup_environ(settings)

from quizbowl.models import Game
from quizbowl.views_notify import notify_user
import datetime

###
#import os
#from django.core.mail import send_mail
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#send_mail("Bienvenido a FLEQ", "Eres un nuevo usuario de FLEQ", 'fleq.libresoft@gmail.com', ['j.gonzalezna@gmail.com'])
###

print datetime.datetime.now()

thirty_minutes_ahead = datetime.datetime.now() + datetime.timedelta(minutes=30)  # datetime X minutes ahead from now
g = Game.objects.filter(start_time__lte = thirty_minutes_ahead, start_time__gte = datetime.datetime.now())


for game in g:
	if not game.log:
		notify_user(game.player1, 'hurry_up', game)
		notify_user(game.player2, 'hurry_up', game)
