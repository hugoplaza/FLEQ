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

from fleq.quizbowl.models import *
from fleq.quizbowl.views_language import *
from fleq.quizbowl.views_tournaments_api import *


def Questions(request):
	
    if request.mobile:
        return HttpResponseRedirect('/')
	
    preguntas = Preguntas_acertadas.objects.all().values('question', 'num_aciertos').distinct().order_by('-num_aciertos')[:10]
	
    data = []
    categories = []
	
    for p in preguntas:
        data.append(int(p['num_aciertos']))
        categories.append('Pregunta '+ str(p['question']))
    
    template = get_template('custom/analytics/questions.html')
    
    return HttpResponse(template.render(RequestContext(request, {'categories': categories, 'data': data})))


def Categories(request):
	
    if request.mobile:
        return HttpResponseRedirect('/')
    
    categories = Category.objects.all()
    
    data = []
    
    for c in categories:
        
        preguntas = Preguntas_acertadas.objects.filter(question__categories=c).values('question', 'num_aciertos').distinct()
        
        aciertos = 0
        for p in preguntas:
            aciertos += p['num_aciertos']
        
        data_category = {'name': c.name.encode('utf-8'), 'number': aciertos}
        data.append(data_category)

    print data
    
    template = get_template('custom/analytics/categories.html')

    return HttpResponse(template.render(RequestContext(request, {'data': data})))
   
   
   
def Questionsgid(request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)

	preguntas = Preguntas_acertadas.objects.filter(torneo=tournament.name).values('question', 'num_aciertos').distinct().order_by('-num_aciertos')[:10]
	
	data = []
	categories = []
	
	for p in preguntas:
		data.append(int(p['num_aciertos']))
		categories.append('Pregunta '+ str(p['question']))
    
	template = get_template('custom/analytics/questions.html')
    
	return HttpResponse(template.render(RequestContext(request, {'categories': categories, 'data': data, 'id': gid})))




def Categoriesgid(request, gid):
	
    if request.mobile:
        return HttpResponseRedirect('/')

    tournament = Tournament.objects.get(id=gid)

    data = []
    
    for c in tournament.categories.all():
        
        preguntas = Preguntas_acertadas.objects.filter(question__categories=c).values('question', 'num_aciertos').distinct()
        
        aciertos = 0
        for p in preguntas:
            aciertos += p['num_aciertos']
        
        data_category = {'name': c.name.encode('utf-8'), 'number': aciertos}
        data.append(data_category)

    
    template = get_template('custom/analytics/categories.html')

    return HttpResponse(template.render(RequestContext(request, {'data': data, 'id': gid})))
   
   
def Absences(request, gid):
	
 	tournament = Tournament.objects.get(id=gid)
 	
 	data = []
 	data2 = []
 	
 	absences = Juegos.objects.filter(torneo=tournament.name).order_by('partida')
 
 	ausencias = 0
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct()
 	for r in rondas:
 		data.append('Ronda ' + str(r['ronda']))
 	
 	for a in absences:
  		if a.ronda == 1:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	data2.append(ausencias)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 2:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	data2.append(ausencias)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 3:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	data2.append(ausencias)
  	ausencias = 0
  
  	for a in absences:
  		if a.ronda == 4:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
  	
  	data2.append(ausencias)
  	ausencias = 0
  	
  	for a in absences:
  		if a.ronda == 2:
  		    if a.player1 == "AUSENTE":
  		    	ausencias = ausencias + 1
  		    if a.player2 == "AUSENTE":
  		    	ausencias = ausencias + 1
 
  	data2.append(ausencias)
  	ausencias = 0

 	
	if request.mobile:
         return HttpResponseRedirect('/')
        

	template = get_template('custom/analytics/absences.html')        
	return HttpResponse(template.render(RequestContext(request, {'data': data, 'data2': data2, 'id': gid})))


def Questionsless(request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)

	preguntas = Preguntas_acertadas.objects.filter(torneo=tournament.name).values('question', 'num_aciertos').distinct().order_by('num_aciertos')[:10]
	
	data = []
	categories = []
	
	for p in preguntas:
		data.append(int(p['num_aciertos']))
		categories.append('Pregunta '+ str(p['question']))
    
	template = get_template('custom/analytics/questionsless.html')
    
	return HttpResponse(template.render(RequestContext(request, {'categories': categories, 'data': data, 'id': gid})))

def Successtime (request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
 	tournament = Tournament.objects.get(id=gid)
 	mensajes = Mensajes.objects.filter(torneo=tournament.name)
 	
 	data = []
 	categories = []
 	count = 0
 	count2 = 0
 	count3 = 0
 	count4 = 0
 	count5 = 0
 	tiempo = 0
 	tiempo2 = 0
 	tiempo3 = 0
 	tiempo4 = 0
 	tiempo5 = 0
 	
 	
 	for m in mensajes:
 		if m.acierto == 1:
 		    if m.ronda == 1:
 		    	tiempo = tiempo + m.tiempo_respuesta
 		    	count = count + 1
  		    elif m.ronda == 2:
  		    	tiempo2 = tiempo2 + m.tiempo_respuesta
 		    	count2 = count2 + 1
  		    elif m.ronda == 3:
  		    	tiempo3 = tiempo3 + m.tiempo_respuesta
 		    	count3 = count3 + 1
  		    elif m.ronda == 4:
  		    	tiempo4 = tiempo4 + m.tiempo_respuesta
 		    	count4 = count4 + 1
 		    elif m.ronda ==5:
 		    	tiempo5 = tiempo5 + m.tiempo_respuesta
 		    	count5 = count5 + 1
 		    	
 	data.append(tiempo/count)
 	data.append(tiempo2/count2)
 	data.append(tiempo3/count3)
 	data.append(tiempo4/count4)
 	data.append(tiempo5/count5)
 	
 	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct()
	for r in rondas:
		categories.append('Ronda ' + str(r['ronda']))
   
	template = get_template('custom/analytics/successtime.html')
    
	return HttpResponse(template.render(RequestContext(request, {'data': data, 'categories':categories, 'id': gid})))


	
# 	if request.mobile:
# 		return HttpResponseRedirect('/')
# 	
#  	tournament = Tournament.objects.get(id=gid)
#  
#  	mensajes = Mensajes.objects.filter(torneo=tournament.name)
#  	
#  	data = []
#  	data2 = []
#  	data3 = []
#  	data4 = []
#  	data5 = []
#  	
#  	
#  	for m in mensajes:
#  		if m.acierto == 1:
#  		    if m.ronda == 1:
#  		    	tiempo = m.tiempo_respuesta
#  		    	count = count + 1
#   		    elif m.ronda == 2:
#   		    	data2.append(m.tiempo_respuesta)
#   		    elif m.ronda == 3:
#   		    	data3.append(m.tiempo_respuesta)
#   		    elif m.ronda == 4:
#   		    	data4.append(m.tiempo_respuesta)
#  		    elif m.ronda ==5:
#  		    	data5.append(m.tiempo_respuesta)
# 	
#    
# 	template = get_template('custom/analytics/successtime.html')
#     
# 	return HttpResponse(template.render(RequestContext(request, {'data': data,  'data2': data2, 'data3': data3, 'data4':data4, 'data5':data5, 'id': gid})))


def General(request, gid):
	
	if request.mobile:
		return HttpResponseRedirect('/')
	
	tournament = Tournament.objects.get(id=gid)
	mensajes = Mensajes.objects.filter(torneo=tournament.name)
	
	categories = []
	
	rondas = Juegos.objects.filter(torneo=tournament.name).values('ronda').distinct()
	for r in rondas:
		categories.append('Ronda ' + str(r['ronda']))
	
# 	acierto1 = 0
# 	fallo1 = 0
# 	preguntas1 = 0
# 	ronda1 = Mensajes.objects.filter(ronda=1)
# 	for r in ronda1:
#  		if r.acierto == 1:
#  			acierto1 = acierto1 + 1
#  			print "aciertos" + str(acierto1)
#  		if r.acierto == 0:
#  			fallo1 = fallo1 + 1
#  			print "fallos" + str(fallo1)
#  		if r.acierto == 2:
#  			if r.tipo == 0:
#  			    preguntas1 = preguntas1 + 1
#  			    print preguntas1
#  			
	
	
 	acierto1 = 0
 	acierto2 = 0
  	acierto3 = 0
  	acierto4 = 0
  	acierto5 = 0
  	fallo1 = 0
 	fallo2 = 0
 	fallo3 = 0
 	fallo4 = 0
 	fallo5 = 0
 	preguntas1 = 0
 	preguntas2 = 0
 	preguntas3 = 0
 	preguntas4 = 0
 	preguntas5 = 0
 	
 	
 	
 	for m in mensajes:
 		if m.acierto == 1:
 		    if m.ronda == 1:
 		    	acierto1 = acierto1 + 1
  		    if m.ronda == 2:
  		    	acierto2 = acierto2 + 1
  		    elif m.ronda == 3:
  		    	acierto3 = acierto3 + 1
  		    elif m.ronda == 4:
  		    	acierto4 = acierto4 + 1
 		    elif m.ronda ==5:
 		    	acierto5 = acierto5 + 1    	
 		elif m.acierto == 0:
 		    if m.ronda == 1:
 		    	fallo1 = fallo1 + 1
  		    elif m.ronda == 2:
  		    	fallo2 = fallo2 + 1
  		    elif m.ronda == 3:
  		    	fallo3 = fallo3 + 1
  		    elif m.ronda == 4:
  		    	fallo4 = fallo4 + 1
 		    elif m.ronda ==5:
 		    	fallo5 = fallo5 + 1
 		elif m.acierto == 2:
  		    if m.tipo == 0:
  		 	  	if m.ronda == 1:
  		 	  		preguntas1 = preguntas1 + 1
  		 	  	elif m.ronda == 2:
  		 	  		preguntas2 = preguntas2 + 1
  		 	  	elif m.ronda == 3:
  		 	  		preguntas3 = preguntas3 + 1
  		 	  	elif m.ronda == 4:
  		 	  		preguntas4 = preguntas4 + 1
  		 	  	elif m.ronda ==5:
  		 	  		preguntas5 = preguntas5 + 1	 		    	
 	 		    	
 	template = get_template('custom/analytics/general.html')
    
	return HttpResponse(template.render(RequestContext(request, {'acierto1': acierto1, 'acierto2': acierto2, 'acierto3': acierto3, 'acierto4': acierto4, 'acierto5': acierto5, 'fallo1': fallo1, 'fallo2': fallo2, 'fallo3': fallo3, 'fallo4': fallo4, 'fallo5': fallo5, 'preguntas1': preguntas1, 'preguntas2': preguntas2, 'preguntas3': preguntas3, 'preguntas4': preguntas4, 'preguntas5': preguntas5, 'categories': categories, 'id': gid})))



