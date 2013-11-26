from django.http import HttpResponse
from django.shortcuts import render_to_response
from views_connect import LoginForm, RegisterForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings

from django.template import RequestContext
from django.template.loader import get_template

from fleq.quizbowl.models import UserProfile, RecoverUser
from fleq.quizbowl.views_language import strLang, setBox
from fleq.quizbowl.views_tournaments_api import *
from fleq.quizbowl.views_notify import notify_user



def Home2(request):
	print request.META['HTTP_USER_AGENT']
	if not request.mobile:
		return render_to_response('mobile/home.html', {})
	else:
		return HttpResponse("pc")


def Welcome(request):

	return render_to_response('mobile/welcome.html', {})



# Login to the app
def Login(request):

	if not request.mobile:
		return HttpResponseRedirect("/")


	if request.user.is_authenticated():

		nextGames = len(Game.objects.filter(Q(log__isnull = False), Q(start_time__gte = datetime.datetime.now()),
										 Q(player1 = request.user) | Q(player2 = request.user)))
		wonGames = len(Game.objects.filter(winner = request.user))
		lostGames = len(Game.objects.filter(Q(player1 = request.user) | Q(player2 = request.user), ~Q(winner = request.user), Q(log=True)))

		#myTournaments = len(Tournament.objects.filter(players = request.user).filter(Q(finish_date__gte = datetime.datetime.now())))
		myTournaments = len(Tournament.objects.filter(players = request.user))
		activeTournaments = len(Tournament.objects.filter(start_date__lte = datetime.date.today(), finish_date__gte = datetime.date.today()))
		nextTournaments = len(Tournament.objects.filter(start_date__gt = datetime.date.today()))
		finishedTournaments = len(Tournament.objects.filter(finish_date__lt = datetime.datetime.now()))

		return render_to_response('mobile/home.html', {
			'nextGames': nextGames,
			'wonGames': wonGames,
			'lostGames': lostGames,
			'myTournaments': myTournaments,
			'activeTournaments': activeTournaments,
			'nextTournaments': nextTournaments,
			'finishedTournaments': finishedTournaments,	
		})



	# Load strings language to template login.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.method == 'POST': # If the form has been submitted...
		loginForm = LoginForm(request.POST) # A form bound to the POST data
		if loginForm.is_valid(): # All validation rules pass
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, user)
			return render_to_response('mobile/home.html', {})
		else:
			registerForm = RegisterForm()
			return render_to_response('mobile/login.html', {
				'loginForm': loginForm,
				'lang': lang,
			})			
	else:
		loginForm = LoginForm() # An unbound form
		registerForm = RegisterForm()
		
# 		return render_to_response('mobile/login.html', {
# 			'loginForm': loginForm,
# 			'lang': lang,
# 		})


		return HttpResponse(get_template('mobile/login.html').render(RequestContext(request, {
			'loginForm': loginForm,
			'lang': lang,																								
		})))






def Logout(request):
  logout(request)
  return render_to_response('mobile/login.html', {})





def Signin(request):

	# Load strings language to template login.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.method == 'POST':
		registerForm = RegisterForm(request.POST)

		if registerForm.is_valid(): 
			user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
			user.is_staff = False
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			userProfile = UserProfile(user=user)
			user.save()
			userProfile.save()

			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, user)

			

			return render_to_response('mobile/welcome.html', {})

		else:
			return render_to_response('mobile/signin.html', {
				'user_me': request.user,
				'registerForm': registerForm,
				'lang': lang,
			})

	else: # If get request, generate a new form
		registerForm = RegisterForm() # An unbound form

		return render_to_response('mobile/signin.html', {
			'user_me': request.user,
			'registerForm': registerForm,
			'lang': lang,
		})



