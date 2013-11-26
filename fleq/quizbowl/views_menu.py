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

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from fleq.quizbowl.views_tournaments_api import *
from fleq.quizbowl.views_language import strLang, setBox
from fleq.quizbowl.models import UserProfile

def home(request):

	if request.mobile:
		return HttpResponseRedirect('mobile')

	# Load strings language to template index.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR INFO
	if request.user.is_active:
		myTournaments = myActiveTournaments(request)
		myAdmnTournaments = myAdminTournaments(request)
		todayGames = myTodayGames(request)
		nextGames = myNextGames(request)
		# Info about user
		user_me = UserProfile.objects.get(user=request.user)
		pendingQR = myAdminPendingQuestionReviews(request.user)
	else:
		myTournaments = ""
		myAdmnTournaments = ""
		todayGames = ""
		nextGames = ""
		user_me = request.user
		pendingQR = 0
  
	return render_to_response('custom/index.html', {
		'user_me': user_me,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})
