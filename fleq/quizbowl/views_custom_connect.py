# -*- coding: utf-8 -*-

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

from fleq.quizbowl.models import UserProfile, RecoverUser, Mensajes, Preguntas_acertadas, Juegos
from fleq.quizbowl.views_language import strLang, setBox
from fleq.quizbowl.views_tournaments_api import *
from fleq.quizbowl.views_notify import notify_user



def Welcome(request):
	if request.mobile:
		return render_to_response('mobile/welcome.html', {})

	return render_to_response('custom/welcome.html', {})


def StepbyStep(request):
	if request.mobile:
		return render_to_response('mobile/stepbystep.html', {})
	
	return render_to_response('custom/stepbystep.html')


def CargarLogs(request):
	
    f = open('/pfc-jgonzalez-data/home/jgonzalez/virtualenvs/fleq/fleq/mislogs/69')  
    lines = f.readlines()
      
    for line in lines:
        if line != "":
            parser = line.split(';')         
             
            fecha = parser[0].split(':')
            usuario = parser[1]
            texto = parser[2]
            tipo = parser[3]
            acierto = parser[4]
            tiempo_respuesta = parser[5]
            num_question = parser[6]  
              
            hora = int(fecha[0])
            minutos = int(fecha[1])
            segundos = int(fecha[2].split('.')[0])
              
            fecha = datetime.datetime(2013,1,1,hora,minutos,segundos)
              
            mensaje = Mensajes(partida=69, torneo = "Tournament_PTAVI", ronda = 5, hora=fecha, usuario=usuario, texto=texto, tipo = tipo, acierto = acierto,  num_question = num_question, tiempo_respuesta = tiempo_respuesta)
            mensaje.save()
      
    f.close()
    return HttpResponse("Datos almacenados correctamente")
   
  
   
def Analytics(request):
	
# 	usuario1 = "AUSENTE"
# 	usuario2 = "AUSENTE"
# 	todos = Mensajes.objects.order_by('id')
# 	for one in todos:
# 		if one.partida == 20:
# 			if one.tipo == 1 or one.tipo == 2:
# 				if (one.usuario != 'FLEQBOT' and one.tipo == 1):
# 					usuario1 = one.usuario
# 				elif (one.usuario != 'FLEQBOT' and one.tipo == 2):
# 					usuario2 = one.usuario
# 	
# 				
# 	nuevojuego = Juegos(partida = 20, torneo = "Tournament PTAVI", ronda = 1, player1 = usuario1, player2 = usuario2)
# 	nuevojuego.save()
	
	if request.mobile:
		return render_to_response('mobile/welcome.html', {})
	
	
	preguntas = Preguntas_acertadas.objects.all().values('pregunta', 'num_aciertos').distinct().order_by('-num_aciertos')[:10]
	
	data = []
	categories = []
	
	for p in preguntas:
		data.append(int(p['num_aciertos']))
		categories.append('Pregunta '+ str(p['pregunta']))
	
	print data
	print categories

	return render_to_response('custom/analytics.html', {'categories': categories, 'data': data})


    
#		preguntas que han sido acertadas (YA ESTAN CARGADAS)
#   	todos = Mensajes.objects.order_by('id')
#   	for one in todos:
#   		if one.acierto == 1:
# 	 	 	aciertos = 1
# 	  		preguntas = Preguntas_acertadas.objects.order_by('id')
# 	  		for p in preguntas:
# 	  		 	if p.pregunta == one.num_question :
# 	  			 	p.num_aciertos = p.num_aciertos +1
# 	  				p.save()
# 	  			    aciertos = p.num_aciertos
# 	  				
# 	  		nuevoacierto = Preguntas_acertadas(pregunta=one.num_question, num_aciertos = aciertos, torneo = one.torneo, intentos = 1, usuario= one.usuario, tiempo = one.tiempo_respuesta)
# 	  		nuevoacierto.save()



# Login to the app
def Home(request):

	if request.user.is_authenticated():

		nextGames = len(Game.objects.filter(Q(log = False), Q(start_time__gte = datetime.datetime.now()),
										 Q(player1 = request.user) | Q(player2 = request.user)))
		wonGames = len(Game.objects.filter(Q(winner = request.user), Q(log=True)))
		lostGames = len(Game.objects.filter(Q(player1 = request.user) | Q(player2 = request.user), ~Q(winner = request.user), Q(log=True)))

		#myTournaments = len(Tournament.objects.filter(players = request.user).filter(Q(finish_date__gte = datetime.datetime.now())))
		myTournaments = len(Tournament.objects.filter(players = request.user))
		activeTournaments = len(Tournament.objects.filter(start_date__lte = datetime.date.today(), finish_date__gte = datetime.date.today()))
		nextTournaments = len(Tournament.objects.filter(start_date__gt = datetime.date.today()))
		finishedTournaments = len(Tournament.objects.filter(finish_date__lt = datetime.datetime.now()))

		if request.mobile:
			return render_to_response('mobile/home.html', {
				'nextGames': nextGames,
				'wonGames': wonGames,
				'lostGames': lostGames,
				'myTournaments': myTournaments,
				'activeTournaments': activeTournaments,
				'nextTournaments': nextTournaments,
				'finishedTournaments': finishedTournaments,	
			})
		
		
		return HttpResponseRedirect("/next-games")


	else:

		if request.method == 'POST': # If the form has been submitted...
			loginForm = LoginForm(request.POST) # A form bound to the POST data
			if loginForm.is_valid(): # All validation rules pass
				user = authenticate(username=request.POST['username'], password=request.POST['password'])
				login(request, user)
		
				if request.mobile:
					return render_to_response('mobile/home.html', {})
				
				else:
					#return HttpResponseRedirect('/next-games')
					myFutureGames = Game.objects.filter(Q(log = False), Q(player1 = request.user) | Q(player2 = request.user)).order_by('start_time')
				
					dates = []
				
					for game in myFutureGames:
						if not game.start_time_committed and (datetime.datetime.now() + datetime.timedelta(minutes=120)) > game.start_time:
							game.start_time_committed = True
							game.save()
				
						if not game.start_time.date() in dates:
							dates.append(game.start_time.date())
				
					template ='custom/next-games.html'
				
					if request.mobile:
						template = 'mobile/next-games.html'
				
					up = UserProfile.objects.get(user=request.user)
					timezone = up.timezone
				
				 	return render_to_response(template, {
				 		'user_me': request.user,
				 		'timezone': timezone,
				 		'myNextGames': myFutureGames,
				 		'dates': dates
				 	})


			else:
				registerForm = RegisterForm()
				template = get_template('custom/splash.html')

				if request.mobile:
					template = get_template('mobile/login.html')


				return HttpResponse(template.render(RequestContext(request, {'loginForm': loginForm})))
			
		else:
			if request.mobile:
				return HttpResponse(get_template('mobile/login.html').render(RequestContext(request, {})))


			return HttpResponse(get_template('custom/splash.html').render(RequestContext(request, {})))




def Logout(request):
	logout(request)
	return HttpResponseRedirect("/")
	


def Signin(request):


	if request.method == 'POST':
		print request.POST
		registerForm = RegisterForm(request.POST)
		
		timezone = request.POST['timezone']

		if registerForm.is_valid(): 
			user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
			user.is_staff = False
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			userProfile = UserProfile(user=user, timezone=timezone)
			user.save()
			userProfile.save()

			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, user)

			#return HttpResponseRedirect("/next-games")

			if request.mobile:
				return HttpResponse(get_template('mobile/welcome.html').render(RequestContext(request, {})))

				#return render_to_response('mobile/welcome.html', {})

# 			return HttpResponse(get_template('custom/welcome.html').render(RequestContext(request, {
# 				'user': request.user
# 			})))
			return HttpResponseRedirect("/active-tournaments")

			#return render_to_response('custom/welcome.html', {
			#	'user': request.user
			#})
			

		else:
			template = get_template('custom/signin.html')

			if request.mobile:
				template = get_template('mobile/signin.html')

			return HttpResponse(template.render(RequestContext(request, {
				'user_me': request.user,
				'registerForm': registerForm
			})))


	else: # If get request, generate a new form
		registerForm = RegisterForm() # An unbound form

		template = get_template('custom/signin.html')

		if request.mobile:
			template = get_template('mobile/signin.html')

		return HttpResponse(template.render(RequestContext(request, {
			'user_me': request.user,
			'registerForm': registerForm
		})))			



def FAQ(request):

	if request.mobile:
		return render_to_response('custom/FAQ.html', {})
	
	return render_to_response('custom/FAQ.html')


