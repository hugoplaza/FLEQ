from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from fleq.quizbowl.views_language import strLang, setBox
from django.template import RequestContext
from django.template.loader import get_template
from fleq.quizbowl.models import *

import datetime


def MyTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
           
	dateNow = datetime.datetime.now()
	myTournaments = Tournament.objects.filter(players = request.user).order_by('-start_date')
	
	myTournaments_format = []
	
	for t in myTournaments:
		myTournament = {'days_per_round': t.days_per_round, 'start_date': t.start_date, 'finish_date': t.finish_date, 
						'rounds': t.rounds, 'name': t.name, 'pk': t.pk}
		
		categories = " - "
		for c in t.categories.all():
			categories += c.name + " - "
			
		myTournament['categories'] = categories
		myTournaments_format.append(myTournament)
	
	
# 	tournamentCategories = []
# 
# 	for t in myTournaments:
# 		categories = t.categories.all()
# 		c = {}
# 		c['tid'] = int(t.pk)
# 		c['categories'] = categories
# 		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'custom/my-tournaments.html'

	if request.mobile:
		template = 'mobile/my-tournaments.html'


	return render_to_response(template, {
		'user_me': request.user,
		'myTournaments': myTournaments_format,
		#'tournamentCategories': tournamentCategories,
		'lang': lang,
	})




def ActiveTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	#activeTournaments = Tournament.objects.filter(Q(finish_date__gte = datetime.datetime.now())).order_by('-start_date')
	activeTournaments = Tournament.objects.filter(start_date__lte = datetime.date.today(), finish_date__gte = datetime.date.today()).order_by('-start_date')

	activeTournaments_format = []
	
	for t in activeTournaments:
		activeTournament = {'days_per_round': t.days_per_round, 'start_date': t.start_date, 'finish_date': t.finish_date, 
						'rounds': t.rounds, 'name': t.name, 'pk': t.pk}
		
		categories = " - "
		for c in t.categories.all():
			categories += c.name + " - "
			
		activeTournament['categories'] = categories
		activeTournaments_format.append(activeTournament)


#	tournamentCategories = []

# 	for t in activeTournaments:
# 		categories = t.categories.all()
# 		c = {}
# 		c['tid'] = t.pk
# 		c['categories'] = categories
# 		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'custom/active-tournaments.html'

	if request.mobile:
		template = 'mobile/active-tournaments.html'


	return render_to_response(template, {
		'user_me': request.user,
		'activeTournaments': activeTournaments_format,
		#'tournamentCategories': tournamentCategories,
		'lang': lang,
	})



def NextTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
           
	nextTournaments = Tournament.objects.filter(start_date__gt = datetime.date.today())

	nextTournaments_format = []
	
	for t in nextTournaments:
		nextTournament = {'days_per_round': t.days_per_round, 'start_date': t.start_date, 'finish_date': t.finish_date, 
						'rounds': t.rounds, 'name': t.name, 'pk': t.pk}
		
		categories = " - "
		for c in t.categories.all():
			categories += c.name + " - "
			
		nextTournament['categories'] = categories
		nextTournaments_format.append(nextTournament)

  
# 	tournamentCategories = []
#  
#  	for t in nextTournaments:
#  		categories = t.categories.all()
#  		c = {}
#  		c['tid'] = t.pk
#  		c['categories'] = categories
#  		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = get_template('custom/next-tournaments.html')

	if request.mobile:
		template = get_template('mobile/next-tournaments.html')


	return HttpResponse(template.render(RequestContext(request, {
		'user_me': request.user,
		'nextTournaments': nextTournaments_format,
		#'tournamentCategories': tournamentCategories,
		'lang': lang,
	})))





def FinishedTournaments(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	finishedTournaments = Tournament.objects.filter(finish_date__lt = datetime.datetime.now()).order_by('-start_date')

	finishedTournaments_format = []
	
	for t in finishedTournaments:
		finishedTournament = {'days_per_round': t.days_per_round, 'start_date': t.start_date, 'finish_date': t.finish_date, 
						'rounds': t.rounds, 'name': t.name, 'pk': t.pk}
		
		categories = " - "
		for c in t.categories.all():
			categories += c.name + " - "
			
		finishedTournament['categories'] = categories
		finishedTournaments_format.append(finishedTournament)


# 	tournamentCategories = []
# 
# 	for t in finishedTournaments:
# 		categories = t.categories.all()
# 		c = {}
# 		c['tid'] = t.pk
# 		c['categories'] = categories
# 		tournamentCategories.append(c)


	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''

	template = 'custom/finished-tournaments.html'

	if request.mobile:
		template = 'mobile/finished-tournaments.html'


	return render_to_response(template, {
		'user_me': request.user,
		'finishedTournaments': finishedTournaments_format,
		#'tournamentCategories': tournamentCategories,
		'lang': lang,
	})





def TournamentStatistics(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

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
			game = Game.objects.filter(Q(round = r), Q(player1 = userProfile.user) | Q(player2 = userProfile.user), Q(log=True))
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

	# Load strings language to template mytournaments.html
	try:
		lang = strLang()
	except:
		lang = ''


	template = 'custom/tournament-statistics.html'

	if request.mobile:
		template = 'mobile/tournament-statistics.html'

	userprofile = UserProfile.objects.get(user=request.user)
	timezone = int(userprofile.timezone)

	return render_to_response(template, {
			'user_me': request.user,
			'timezone': timezone,
			'tournament': tournament,
			'join': join,
			'disjoin': disjoin,
			'scores': scores,
			'rounds': rounds,
			'games': games,
			'lang': lang,
		})



def JoinTournament(request, gid):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	try:
		tournament = Tournament.objects.get(pk=gid)
	except:
		return HttpResponseRedirect('/')
	
	# players are added automatically to not started tournament the first time they visit tournament's site
	if (request.user != tournament.admin) and (not request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		tournament.players.add(request.user)
		tournament.save()
		player_profile = UserProfile.objects.get(user=request.user)
		s = Score(player = request.user, player_profile=player_profile, tournament = tournament)
		s.save()

		return HttpResponseRedirect('/tournament/'  + gid)

	else:
		return HttpResponseRedirect('/tournament/'  + gid)





def DisjoinTournament(request, gid):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	try:
		tournament = Tournament.objects.get(pk=gid)
	except:
		return HttpResponseRedirect('/')
	
	# players are added automatically to not started tournament the first time they visit tournament's site
	if (request.user != tournament.admin) and (request.user in tournament.players.all()) and (datetime.date.today() < tournament.start_date):
		tournament.players.remove(request.user)
		tournament.save()
		
		Score.objects.get(player=request.user, tournament=tournament).delete()

		return HttpResponseRedirect('/tournament/'  + gid)

	else:
		return HttpResponseRedirect('/tournament/'  + gid)




