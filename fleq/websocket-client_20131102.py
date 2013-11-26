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
from quizbowl.models import *
from django.contrib.auth.models import User
from django.utils.html import escape

import httplib
import websocket
import threading
import time
import json


NUM_CORRECT = 10
QUESTIONS = 20


game_id = sys.argv[1]


# Extract quiz questions and fix the start time
game = Game.objects.get(pk=game_id)
game.start_time_committed = True
game.save()
c = Category.objects.filter(tournament = game.round.tournament)
#q = list(Question.objects.filter(categories = c))

q = []
for category in c:
    questions = list(Question.objects.filter(categories = category))
    for question in questions:
        q.append(question)


# Set up codec
reload(sys)
sys.setdefaultencoding("utf-8")


break_thread = 0


class send_ping(threading.Thread):

    def __init__(self, ws):
        threading.Thread.__init__(self) # no need for extra args
        self.ws = ws
        
    def run(self):
        global break_thread
        
        while 1:
            time.sleep(5)
            self.ws.send("2::")
            
            if break_thread == 1:
                self.ws.send('0::')
                break



class Fleqbot():
    
    def __init__(self):
        self.ws = ""
        self.ping = ""
        return

    def connect(self, room):
    
        conn  = httplib.HTTPConnection("localhost:8004")
        conn.request('GET','/socket.io/1/')
        resp  = conn.getresponse() 
     
        hk = resp.read()
        hskey = ''.join(hk).split(':')[0]    
           
        self.ws = websocket.create_connection('ws://localhost:8004/socket.io/1/websocket/' + hskey)
            
        data = self.ws.recv()
        
        self.ws.send('3:::{"code": "1", "room": "' + room + '", "user": "FLEQBOT"}')
        
        if self.ws.recv() == '3:::{"code":"1"}':
            self.ping = send_ping(self.ws)
            self.ping.start()
            return 1
        
        return 0
    
    
    def send(self, message):
        self.ws.send('3:::{"code": "2", "room": "' + game_id + '", "user": "FLEQBOT", "message": "' + message + '"}')
        
        return
    

    def recv(self):
        data = self.ws.recv()[4:]
        return data


    def disconnect(self):
        global break_thread
        break_thread = 1
        return



if __name__ == "__main__":
    
    fb = Fleqbot()
    
    fb.connect(game_id)

    # Start countdown
    fb.send('La partida empieza en 3 min')
#     time.sleep(60)
#     fb.send('Quedan 2 minutos...')
#     time.sleep(30)
#     fb.send('Solo 1 min 30 seg...')
#     time.sleep(30)
#     fb.send('Un minuto para el comienzo!')
#     time.sleep(30)
#     fb.send('30 segundos')
#     time.sleep(20)
#     fb.send('La partida entre ' + game.player1.username + " y " + game.player2.username + ' correspondiente al torneo ' + str(game.round) + ' va a empezar')
#     time.sleep(5)
#     fb.send('Recordamos que es indiferente contestar en mayúsculas o en minúsculas')
#     time.sleep(5)
#     fb.send('Una vez lanzada la pregunta, se dispone de 90 segundos para contestar')
#     time.sleep(5)
#     fb.send('El primer jugador en conseguir ' + str(NUM_CORRECT) + ' respuestas correctas gana la partida')
#     time.sleep(5)
#     fb.send('Se dispone de un total de ' + str(QUESTIONS) + ' preguntas')
#     time.sleep(5)
#     fb.send('Si se consumen sin que ningún jugador alcance ' + str(NUM_CORRECT) + ' aciertos, ganará el que más haya acertado')
#     time.sleep(5)
#     fb.send('En caso de haber empate, se considerará que ambos jugadores pierden')
#     time.sleep(5)

    fb.send('SUERTE!!')
    time.sleep(3)
    
    # Create log file
    logfile = open('/pfc-jgonzalez-data/home/jgonzalez/virtualenvs/fleq/fleq/logs/' + str(game_id), 'w')
    
    # Set up auxiliar variables
    num_msg = 0
    score1 = 0
    score2 = 0
    game_finished = False
    winner = ''
    lap = 0
    

    # Start game
    # Select and send first question
    num_question = random.randrange(len(q))
    
    fb.send(escape(q[num_question].question))
    QUESTIONS = QUESTIONS - 1
    
    while 1:
        data = fb.recv()
        if data == "":
            continue
        
        jData = json.loads(data)
        
        message = jData['message'].encode('utf-8').lower().replace('"', "&quot;").replace("'", "&#39;").replace('\\', '&#92')
        username = jData['user'].encode('utf-8')
        
        
        print "-------------------------------"
        print username
        print message
        print "-------------------------------"

        print "CORRECT ANSWER"
        print q[num_question].answer
        
        if (message == str(escape(q[num_question].answer)).lower() or message == str(escape(q[num_question].alt_answer1)).lower() \
                or message == str(escape(q[num_question].alt_answer2)).lower() or message == str(escape(q[num_question].alt_answer3)).lower()) \
                and message != "":        

            time.sleep(1)

            fb.send("Respuesta correcta de " + username + "!")
            
            time.sleep(3)
            
            # Sumar resultados
            # Guardar en el log
            q.remove(q[num_question])
            num_question = random.randrange(len(q))
            fb.send(escape(q[num_question].question))
            
            # Comprobamos que no hayan llegado a 10

    fb.disconnect()
