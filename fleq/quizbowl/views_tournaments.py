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
#                    Félix Redondo <felix.redondo.sierra@gmail.com>	    #
#                                                                           #
#############################################################################

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from datetime import *
import datetime
from operator import itemgetter

from fleq.quizbowl.models import Date_time, Game, Preferred_start_time, Question_review, Round, Score, Tournament, Question, UserProfile
from fleq.quizbowl.views_notify import notify_user
from fleq.quizbowl.views_language import strLang, setBox
from fleq.quizbowl.views_tournaments_api import *

from fleq.quizbowl.views_connect import EditProfileForm, ChangePasswordForm

##################################
# MY TOURNAMENTS
##################################

# Shows active Tournaments of user (admin tournament or player tournament)
def myTournaments(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')
           
	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	myFinishedTournaments = myPastTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	pendingQR = myAdminPendingQuestionReviews(request.user)
	
	# Player hasn't got any Tournament, redirect to Tournaments
	if len(myAdmnTournaments) == 0 and len(myTournaments) == 0 and len(myFinishedTournaments) == 0 and not request.user.is_superuser:
		return HttpResponseRedirect('/tournaments?status=info_join_tournaments')
	elif len(myAdmnTournaments) == 0 and len(myTournaments) == 0 and len(myFinishedTournaments) == 0 and request.user.is_superuser:
		return HttpResponseRedirect('/admin/new-tournament?status=info_new_tournament')
	
	dateNow = datetime.datetime.now()
	  
	tournamentCategories = []
	for t in myTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)
		
	adminTournamentCategories = []
	for t in myAdmnTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		adminTournamentCategories.append(c)

	finishedTournamentCategories = []
	for t in myFinishedTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		finishedTournamentCategories.append(c)

	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	# Must we show a notification user?
	try:
		if request.GET['status']:
			box = setBox(request.GET['status'])
	except:
		box = ''
	
	# Info about user
	user_me = UserProfile.objects.get(user=request.user)
	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	return render_to_response('mytournaments.html', {
		'user_me': user_me,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'myFinishedTournaments': myFinishedTournaments,
		'tournamentCategories': tournamentCategories,
		'adminTournamentCategories': adminTournamentCategories,
		'finishedTournamentCategories': finishedTournamentCategories,
		'dateNow': dateNow,
		'lang': lang,
		'box': box,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})

##################################
# TOURNAMENTS
##################################

# Show information about active Tournaments and future Tournaments
def tournaments(request):

	# Load strings language to template tournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

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

	# Must we show a notification user?
	try:
 		if request.GET['status']:
 			box = setBox(request.GET['status'])
	except:
		box = ''
           
	# Select all next and active Tournaments
	nextTournaments = Tournament.objects.exclude(start_date__lte = datetime.date.today())
	activeTournaments =  Tournament.objects.filter(Q(finish_date__gte = datetime.datetime.now())).order_by('-start_date')
	finishedTournaments = Tournament.objects.filter(Q(finish_date__lte = datetime.datetime.now())).order_by('-start_date')[:10]
   
   # Select all categories from Tournaments
	tournamentCategories = []
	for t in nextTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c) 
	for t in activeTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)
	for t in finishedTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)

   # Select all players from Tournaments
	tournamentPlayers = []
		    
	return render_to_response('tournaments.html', {
		'user_me': user_me,
		'nextTournaments': nextTournaments,
		'activeTournaments': activeTournaments,
		'finishedTournaments': finishedTournaments,
		'tournamentCategories': tournamentCategories,
		'box': box,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})

##################################
# TOURNAMENTSINFO
##################################

# Show information about a Tournament
def tournamentInfo(request, sid):
	try:
		tournament = Tournament.objects.get(sid = sid)
	except:
		return HttpResponseRedirect('/tournaments?status=error_tournament_no_exists')

	# Load strings language to template tournamentinfo.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# Must we show a notification user?
	try:
		if request.GET['status']:
			box = setBox(request.GET['status'])
	except:
		box = ''

	# SIDEBAR INFO
	if request.user.is_authenticated():
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
		user_me = ""
		pendingQR = 0
	
	# Info about Tournaments
	dateNow = datetime.datetime.now()
	name = tournament.name
	startDate = tournament.start_date
	finishDate = tournament.finish_date
	numberRounds = tournament.rounds
	rounds = Round.objects.filter(tournament = tournament).order_by('round_number')
	
	# Check if a user can join to this tournament now
	if startDate >= dateNow.date() and request.user != tournament.admin:
		for player in tournament.players.all():
			if player == request.user:
				userJoined = True
				break
		else:
			userJoined = False
	else:
		userJoined = True
		
	# Generate Score Table by this Tournament
	allscores = Score.objects.filter(tournament = tournament).order_by('-points', '-questions_won', 'questions_lost', 'player') # Extract all info about scores and players in a Tournament
	scores = []
	pos = 0
	for userScore in allscores:
		userProfile = UserProfile.objects.get(user=userScore.player)
		user = {}
		user['profile'] = userProfile
		user['score'] = userScore.points
		
		# Create tournament positions
		if pos == 0:
			user['pos'] = pos+1
		else:
			if scores[pos-1]['score'] == userScore.points:
				user['pos'] = scores[pos-1]['pos']
			else:
				user['pos'] = pos+1
		
		# Initializing vars for question stats
		user['winner_questions'] = userScore.questions_won
		user['loser_questions'] = userScore.questions_lost
		user['winner_games'] = 0
		user['loser_games'] = 0
		
		# For each user, calculate how many games did he play
		gamesUser = []
		for r in rounds:
			game = Game.objects.filter(Q(round = r), Q(player1 = userProfile.user) | Q(player2 = userProfile.user))
			try:
				#if game[0] and game[0].log:
				if game[0]:
					gamesUser.append(game)
					# Total points won and lost
					try:
						if game[0].winner != userScore.player:
							user['loser_games'] += 1
						else:
							user['winner_games'] += 1
					except:
						continue
			except:
				continue
		
		user['reflection_days'] = user['score'] - user['winner_games']
		user['total_games'] = len(gamesUser)
		
		# Save user stats and increment counter var
		scores.append(user)
		pos += 1
	
	# Select all games if you are admin and only user games if you aren't a superuser	
	allGames = []
	myGames = []
	if tournament.admin == request.user or request.user.is_superuser:
		for r in rounds:
			games = Game.objects.filter(round = r, round__tournament = tournament)
			for game in games:
				g = {}
				g['rid'] = r.pk
				g['game'] = game
				allGames.append(g)			
	else:
		if request.user.is_authenticated():
			myGames = Game.objects.filter(Q(player1 = request.user) | Q(player2 = request.user))
		else:
			myGames = ""
	
	return render_to_response('tournamentinfo.html', {
		'user_me': user_me,
		'tournament': tournament,
		'name': name,
		'startDate': startDate,
		'finishDate': finishDate,
		'dateNow': dateNow,
		'numberRounds': numberRounds,
		'scores': scores,
		'rounds': rounds,
		'myGames': myGames,
		'allGames': allGames,
		'lang': lang,
		'box': box,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'userJoined': userJoined, # Boolean variable. Shows if a user is the admin tournament or if he/she has joined to this Tournament	
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})

def tournamentJoin(request, sid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register?status=error_register_before_join_tournament')

	try:
		tournament = Tournament.objects.get(sid = sid)
	except:
		return HttpResponseRedirect('/tournaments?status=error_tournament_no_exists')
	
	# players are added automatically to not started tournament the first time they visit tournament's site
	if (request.user != tournament.admin) and (not request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		tournament.players.add(request.user)
		tournament.save()
		s = Score(player = request.user, tournament = tournament)
		s.save()
		return HttpResponseRedirect('/tournaments/{{ tournament.sid }}?status=success_join_tournament')
	else:
		if datetime.date.today() >= tournament.start_date:
			return HttpResponseRedirect('/tournaments/' + tournament.sid + '?status=error_join_tournament_expired')
		elif request.user == tournament.admin:
			return HttpResponseRedirect('/tournaments/' + tournament.sid + '?status=error_join_tournament_admin')
		elif request.user in tournament.players.all():
			return HttpResponseRedirect('/tournaments/' + tournament.sid + '?status=error_join_tournament_joined')
		else:
			return HttpResponseRedirect('/tournaments/' + tournament.sid + '?status=error_join_tournament')
