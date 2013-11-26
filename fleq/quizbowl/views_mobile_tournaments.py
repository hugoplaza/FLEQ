from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from fleq.quizbowl.views_language import strLang, setBox
import datetime

from fleq.quizbowl.models import *



def MyTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/mobile')
           
	dateNow = datetime.datetime.now()
	myTournaments = Tournament.objects.filter(players = request.user).order_by('-start_date')
	  
	tournamentCategories = []

	for t in myTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


	return render_to_response('mobile/my-tournaments.html', {
		'myTournaments': myTournaments,
		'tournamentCategories': tournamentCategories,
		'lang': lang,
	})




def ActiveTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/mobile')

	#activeTournaments = Tournament.objects.filter(Q(finish_date__gte = datetime.datetime.now())).order_by('-start_date')
	activeTournaments = Tournament.objects.filter(start_date__lte = datetime.date.today(), finish_date__gte = datetime.date.today()).order_by('-start_date')
	tournamentCategories = []

	for t in activeTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


	return render_to_response('mobile/active-tournaments.html', {
		'activeTournaments': activeTournaments,
		'tournamentCategories': tournamentCategories,
		'lang': lang,
	})








def NextTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/mobile')
           
	nextTournaments = Tournament.objects.filter(start_date__gt = datetime.date.today())
	  
	tournamentCategories = []

	for t in nextTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


	return render_to_response('mobile/next-tournaments.html', {
		'nextTournaments': nextTournaments,
		'tournamentCategories': tournamentCategories,
		'lang': lang,
	})




def FinishedTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/mobile')

	finishedTournaments = Tournament.objects.filter(finish_date__lt = datetime.datetime.now()).order_by('-start_date')
	tournamentCategories = []

	for t in finishedTournaments:
		categories = t.categories.all()
		c = {}
		c['tid'] = t.pk
		c['categories'] = categories
		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


	return render_to_response('mobile/finished-tournaments.html', {
		'finishedTournaments': finishedTournaments,
		'tournamentCategories': tournamentCategories,
		'lang': lang,
	})













def TournamentStatistics(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/mobile')

	tournament = Tournament.objects.get(id=gid)
	rounds = Round.objects.filter(tournament = tournament).order_by('round_number')

	# Generate Score Table by this Tournament
	allscores = Score.objects.filter(tournament=tournament).order_by('-points', '-questions_won', 'questions_lost', 'player')
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
						if game[0].winner != userScore.player and game[0].winner.username != "jgonzalez":
							print "LOST"
							user['loser_games'] += 1
						elif game[0].winner.username == "FLEQBOT":
							user['loser_games'] += 1
						elif game[0].winner == userScore.player:
							user['winner_games'] += 1
					except:
						continue
			except:
				continue
		
		user['reflection_days'] = user['score'] - user['winner_games']
		user['total_games'] = user['loser_games'] + user['winner_games']
		
		# Save user stats and increment counter var
		scores.append(user)
		pos += 1

	rounds = Round.objects.filter(tournament=tournament)
	games = Game.objects.all()

	join = False
	disjoin = False

	if not (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		join = True
	elif (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		disjoin = True

	return render_to_response('mobile/tournament-statistics.html', {
			'tournament': tournament,
			'join': join,
			'disjoin': disjoin,
			'scores': scores,
			'rounds': rounds,
			'games': games
		})






def JoinTournament(request, gid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/mobile')

	try:
		tournament = Tournament.objects.get(pk=gid)
	except:
		return HttpResponseRedirect('/mobile')
	
	# players are added automatically to not started tournament the first time they visit tournament's site
	if (request.user != tournament.admin) and (not request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		tournament.players.add(request.user)
		tournament.save()
		s = Score(player = request.user, tournament = tournament)
		s.save()
		return HttpResponseRedirect('/mobile/tournament/'  + gid)

	else:
		return HttpResponseRedirect('/mobile/tournament/'  + gid)




def DisjoinTournament(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/mobile')

	try:
		tournament = Tournament.objects.get(pk=gid)
	except:
		return HttpResponseRedirect('/mobile')
	
	# players are added automatically to not started tournament the first time they visit tournament's site
	if (request.user != tournament.admin) and (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		tournament.players.remove(request.user)
		tournament.save()
		
		Score.objects.get(player=request.user, tournament=tournament).delete()

		return HttpResponseRedirect('/mobile/tournament/'  + gid)

	else:
		return HttpResponseRedirect('/mobile/tournament/'  + gid)




