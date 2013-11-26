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
from quizbowl.views import notify_user
from django.contrib.auth.models import User
from django.utils.html import escape

import httplib
import websocket
import threading
import time
import json


NUM_CORRECT = 10
QUESTIONS = 20

# NUM_CORRECT = 10
# QUESTIONS = 20


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
        try:
            data = self.ws.recv()[4:]
        except:
            return ""
        
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
    time.sleep(60)
    fb.send('Quedan 2 minutos...')
    time.sleep(30)
    fb.send('Solo 1 min 30 seg...')
    time.sleep(30)
    fb.send('Un minuto para el comienzo!')
    time.sleep(30)
    fb.send('30 segundos')
    time.sleep(20)
    fb.send('La partida entre ' + game.player1.username + " y " + game.player2.username + ' correspondiente al torneo ' + str(game.round) + ' va a empezar')
    time.sleep(5)
    fb.send('Recordamos que es indiferente contestar en mayúsculas o en minúsculas')
    time.sleep(5)
    fb.send('Una vez lanzada la pregunta, se dispone de 90 segundos para contestar')
    time.sleep(5)
    fb.send('El primer jugador en conseguir ' + str(NUM_CORRECT) + ' respuestas correctas gana la partida')
    time.sleep(5)
    fb.send('Se dispone de un total de ' + str(QUESTIONS) + ' preguntas')
    time.sleep(5)
    fb.send('Si se consumen sin que ningún jugador alcance ' + str(NUM_CORRECT) + ' aciertos, ganará el que más haya acertado')
    time.sleep(5)
    fb.send('En caso de haber empate, se considerará que ambos jugadores pierden')
    time.sleep(5)

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
   

    
    what = '4'
    while 1:
        
        fb.ws.settimeout(1)

        data = fb.recv()            
        
        if data == "":
            lap = lap + 1
            #print lap
            #cCMBIAR LOS "= SEGUNDOS A 90 SEGUNDOSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
            if lap == 90:
                fb.send("Los 90 segundos se han cumplido sin que se haya acertado la respuesta")
                time.sleep(3)
                fb.send("La respuesta correcta era: " + q[num_question].answer)
                time.sleep(3)
                 
                if QUESTIONS == 1:
                    fb.send("Última pregunta disponible...")
                    time.sleep(3)
     
                if QUESTIONS != 0:
                    q.remove(q[num_question])
                    num_question = random.randrange(len(q))
                    fb.send(escape(q[num_question].question))
                else:
                    game_finished = True
                    fb.send("Se han acabado las preguntas dispobibles y la partida ha terminado")
                    time.sleep(1)
                    fb.send ('El resultado final ha sido: ' + str(score1) + ' - ' + str(score2))
                    time.sleep(1)
                    fb.send("Podéis consultar la tabla del torneo para conocer la clasificación. Hasta la próxima!")
                    break
     
                QUESTIONS = QUESTIONS - 1
     
                lap = 0
            continue
        
        jData = json.loads(data)
        
        message = jData['message'].encode('utf-8').lower().replace('"', "&quot;").replace("'", "&#39;").replace('\\', '&#92')
        username = jData['user'].encode('utf-8')
        
        #OJO GUARDAR TB EN LOS LOGS ESTO:
        #tournament = game.round.tournament
        #game.round.round_number
        
        if (username == 'FLEQBOT') and (message == (q[num_question].question).lower()): 
            what = '0'   #pregunta lanzada por fleqbot 
            success = '2' #ni acierta ni falla
            datequestion = time.time()
            tiempo = "0"
            numquestion = str(q[num_question].id)
    
        elif ((username == game.player1.username) and (what !='4') and (what !='3')):
            what ='1' # mensaje del usuario1
            if (message == str(escape(q[num_question].answer)).lower() or message == str(escape(q[num_question].alt_answer1)).lower() \
                    or message == str(escape(q[num_question].alt_answer2)).lower() or message == str(escape(q[num_question].alt_answer3)).lower()) \
                    and message != "":
                success = '1' #acierta
                restatiempo = time.time()- datequestion
                tiempo = str(restatiempo)
                numquestion = str(q[num_question].id)
                        
            else: 
                success = '0' #ha fallado
                tiempo = "0"
                numquestion = str(q[num_question].id)
                       
        elif ((username == game.player1.username) and (what =='4')):
            what = '4'
            success = '2'
            tiempo =  "0"
                   
        elif ((username == game.player2.username)and (what !='4') and (what !='3')):
            what = '2' #mensaje del usuario2
            if (message == str(escape(q[num_question].answer)).lower() or message == str(escape(q[num_question].alt_answer1)).lower() \
                    or message == str(escape(q[num_question].alt_answer2)).lower() or message == str(escape(q[num_question].alt_answer3)).lower()) \
                    and message != "":
                success = '1' #acierta
                restatiempo = time.time()- datequestion
                tiempo = str(restatiempo)
                numquestion = str(q[num_question].id)
                              
            else: 
                success = '0' #ha fallado
                tiempo =  "0"
                numquestion = str(q[num_question].id)
                        
        elif ((username == game.player2.username) and (what =='4')):
            what = '4'
            success = '2'
            tiempo =  "0"
            numquestion = "0"
                         
        elif (username == 'FLEQBOT') and not (message == (q[num_question].question).lower()): 
            what = '3'   #mensajes de instrucciones de fleqbot 
            success = '2' #ni acierta ni falla
            tiempo =  "0"
            numquestion = "0"
        
        logfile.write(str(datetime.datetime.now().time()) + ";" + username + ";" + message + ";" + what + ";" + success + ";" + tiempo + ";" + numquestion + ";\n") 
        
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
            
            if username == game.player1.username:
                fb.send(game.player1.username + ' ha acertado!')
                score1 = score1 + 1
            elif username == game.player2.username:
                fb.send(game.player2.username + ' ha acertado!')
                score2 = score2 + 1
            
            time.sleep(3)
            
            fb.send(game.player1.username + " " + str(score1) + ':' + str(score2) + " " + game.player2.username)
            
            time.sleep(2)
            
            if score1 == NUM_CORRECT or score2 == NUM_CORRECT:
                game_finished = True
                fb.send('La partida ha terminado')
                time.sleep(3)
                fb.send ('El resultado final ha sido: ' + str(score1) + ' - ' + str(score2))
                time.sleep(3)
                if score1 > score2:
                    winner = game.player1
                    loser = game.player2
                    print "PLAYER1"
                elif score2 > score1:
                    winner = game.player2
                    loser = game.player1
                    print "PLAYER2"    
                
                if score1 != score2:
                    game.winner = winner
                    fb.send(winner.username + " ha sido el vencedor")
                    time.sleep(2)
                    fb.send("ENHORABUENA!!")
                else:
                    fleqbot = User.objects.get(username="FLEQBOT")
                    game.winner = fleqbot
                    elem.send_keys("Habéis empatado tras agotar el lote de preguntas disponibles para la partida")
                    time.sleep(3)
                    elem.send_keys("El sistema de puntuación aún no contempla empates, por lo que ambos habéis perdido esta partida...")
                    time.sleep(3)
                    elem.send_keys("Al empatar por lo menos habéis evitado que vuestro oponente sume una victoria, no está mal!")
                
                time.sleep(3)
                fb.send("Podéis consultar la tabla del torneo para conocer la clasificación. Hasta la próxima!")

                scorepl1 = Score.objects.get(player=game.player1, tournament=game.round.tournament)
                scorepl2 = Score.objects.get(player=game.player2, tournament=game.round.tournament)            

                game.score_player1 = score1
                game.score_player2 = score2

                scorepl1.questions_won += score1
                scorepl1.questions_lost += score2
                scorepl2.questions_lost += score1
                scorepl2.questions_won += score2            
            
                game.save()
                scorepl1.save()
                scorepl2.save()
    
                print "SAVE GAME"

                if score2 != score1:
                    winnerProfile = UserProfile.objects.get(user=winner)
                    loserProfile = UserProfile.objects.get(user=loser)
        
                    winnerProfile.winner_games = winnerProfile.winner_games + 1
                    loserProfile.loser_games = loserProfile.loser_games + 1
        
                    winnerProfile.save()
                    loserProfile.save()
        
                    if score1 > score2:
                        scorepl1.points = scorepl1.points + 1
                        scorepl1.save()
                    elif score2 > score1:
                        scorepl2.points = scorepl2.points + 1
                        scorepl2.save()

                else:
                    player1pf = UserProfile.objects.get(user=game.player1)
                    player2pf = UserProfile.objects.get(user=game.player2)
        
                    player1pf.loser_games = player1pf.loser_games + 1
                    player2pf.loser_games = player2pf.loser_games + 1
        
                    player1pf.save()
                    player2pf.save()


                if game.round.round_number == game.round.tournament.rounds:
                    if not Game.objects.filter(round = game.round):
                        for score in Score.objects.filter(tournament = game.round.tournament):
                            notify_user(score.player, 'tournament_over', game.round.tournament)
                        notify_user(game.round.tournament.admin, 'tournament_over', game.round.tournament)
        
                break
                
            
            
            #Comprobamos si es la última pregunta disponible
            if QUESTIONS == 1:
                fb.send("Última pregunta disponible...")
                time.sleep(3)
      
            q.remove(q[num_question])
            num_question = random.randrange(len(q))
            fb.send(escape(q[num_question].question))
            QUESTIONS = QUESTIONS - 1
            print "Preguntas que quedan por hacer...."
            print QUESTIONS
            lap = 0
      
            # Sumar resultados
            # Guardar en el log
        
        
logfile.close()
game.log = True
game.save()
time.sleep(2)
fb.disconnect()
