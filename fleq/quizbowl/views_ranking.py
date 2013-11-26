# -*- coding: utf-8 -*-

#############################################################################
#                                                                           #
#  FLEQ (Free LibreSoft Educational Quizbowl)                               #
#  A synchronous on-line competition software to improve and                #
#  motivate learning.                                                       #
#                                                                           #
#  Copyright (C) 2012  Arturo Moral, Gregorio Robles & Félix Redondo        #
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
#                    Félix Redondo <felix.redondo.sierra@gmail.com>			 #
#                                                                           #
#############################################################################

from __future__ import division

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from datetime import *
import datetime

from fleq.quizbowl.models import Date_time, Game, Preferred_start_time, Question_review, Round, Score, Tournament, Question, UserProfile
from fleq.quizbowl.views_notify import notify_user
from fleq.quizbowl.views_language import strLang, setBox
from fleq.quizbowl.views_tournaments_api import *

##################################
# RANKING
##################################

def ranking(request):

	# SIDEBAR INFO
	if request.user.is_authenticated():
		myTournaments = myActiveTournaments(request)
		myAdmnTournaments = myAdminTournaments(request)
		todayGames = myTodayGames(request)
		nextGames = myNextGames(request)
		user_me = UserProfile.objects.get(user=request.user)
		pendingQR = myAdminPendingQuestionReviews(request.user)
	else:
		myTournaments = ''
		myAdmnTournaments = ''
		todayGames = ''
		nextGames = ''
		user_me = request.user
		pendingQR = 0

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# Load strings language to template newquestionreview.html
	try:
		lang = strLang()
	except:
		lang = ''
		
	# Select all stats by users
	users = UserProfile.objects.all().order_by('-winner_games')
	
	ranking = []
	for user in users:
		u = {}
		u['user'] = user
		u['total_games'] = user.winner_games + user.loser_games
		u['winner_games'] = user.winner_games
		u['loser_games'] = user.loser_games
		if user.winner_games + user.loser_games == 0:
			u['winner_total_ratio'] = 0
		else:
			u['winner_total_ratio'] = (user.winner_games/(user.winner_games + user.loser_games))
		ranking.append(u)	
	
	return render_to_response('ranking.html', {
		'user_me': user_me,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,		
		'lang': lang,
		'ranking': ranking,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})	
