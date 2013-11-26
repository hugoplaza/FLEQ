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
from selenium import webdriver
#from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from quizbowl.models import Category, Game, Question, Score, UserProfile
from quizbowl.views import notify_user
from django.utils.html import escape
from django.contrib.auth.models import User


NUM_CORRECT = 10
QUESTIONS = 20

#HOST = "http://pfc-jgonzalez.libresoft.es"
HOST = "http://pfc-clavado.libresoft.es"

game_id = sys.argv[1]


# Synchronization
now = datetime.datetime.now()
seconds_init = int(time.mktime(now.timetuple()))
seconds_start = seconds_init + 180


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


# Hide Firefox 
os.environ['DISPLAY'] = ':1008'
#display = Display(visible=0, size=(800, 600))
#display.start()


# Launch Firefox
browser = webdriver.Firefox()
#browser = webdriver.PhantomJS(executable_path='/pfc-jgonzalez-data/home/jgonzalez/virtualenvs/fleq/fleq/phantomjs/bin/phantomjs') 


# Log in FLEQ as FLEQBOT
browser.get(HOST + "/game-room/" + game_id)
#elem = browser.find_element_by_id("loginForm").find_element_by_name("username")
elem = browser.find_element_by_name("username")
elem.send_keys("FLEQBOT")
#elem = browser.find_element_by_id("loginForm").find_element_by_name("password")
elem = browser.find_element_by_name("password")
elem.send_keys("F13B0t")
#elem = browser.find_element_by_id("loginForm").find_element_by_class_name("button").send_keys(Keys.RETURN)
elem = browser.find_element_by_class_name("button").send_keys(Keys.RETURN)

# Go to Game window
browser.get(HOST + "/game-room/" + game_id)
time.sleep(5)
elem = browser.find_element_by_name("message")

# Start countdown
now = datetime.datetime.now()
seconds_now = int(time.mktime(now.timetuple()))

time.sleep(30 - (seconds_now - seconds_init))
elem.send_keys('La partida empieza en 2 min 30 seg' + Keys.RETURN)
time.sleep(30)
elem.send_keys('Quedan 2 minutos...' +  Keys.RETURN)
time.sleep(30)
elem.send_keys('Solo 1 min 30 seg...' + Keys.RETURN)
time.sleep(30)
elem.send_keys('Un minuto para el comienzo!' + Keys.RETURN)
time.sleep(30)
elem.send_keys('30 segundos' + Keys.RETURN)
time.sleep(20)
elem.send_keys('La partida entre ' + game.player1.username + " y " + game.player2.username + ' correspondiente al torneo ' + str(game.round) + ' va a empezar' + Keys.RETURN)
time.sleep(5)
elem.send_keys('Recordamos que es indiferente contestar en mayúsculas o en minúsculas' + Keys.RETURN)
time.sleep(5)
elem.send_keys('Una vez lanzada la pregunta, se dispone de 90 segundos para contestar' + Keys.RETURN)
time.sleep(5)
elem.send_keys('El primer jugador en conseguir ' + str(NUM_CORRECT) + ' respuestas correctas gana la partida' + Keys.RETURN)
time.sleep(5)
elem.send_keys('Se dispone de un total de ' + str(QUESTIONS) + ' preguntas' + Keys.RETURN)
time.sleep(5)
elem.send_keys('Si se consumen sin que ningún jugador alcance ' + str(NUM_CORRECT) + ' aciertos, ganará el que más haya acertado' + Keys.RETURN)
time.sleep(5)
elem.send_keys('En caso de haber empate, se considerará que ambos jugadores pierden' + Keys.RETURN)
time.sleep(5)
elem.send_keys('SUERTE!!' + Keys.RETURN)
time.sleep(3)

# Select and send first question
num_question = random.randrange(len(q))
elem.send_keys(escape(q[num_question].question) + Keys.RETURN)
QUESTIONS = QUESTIONS - 1


# Create log file
logfile = open('/pfc-jgonzalez-data/home/jgonzalez/virtualenvs/fleq/fleq/logs/' + str(game_id), 'w')
#logfile = open(os.getcwd() + '/logs/' + str(game_id), 'w')
#logfile.write(str(datetime.datetime.now().time()) + ";FLEQBOT;" + q[num_question].question + ";\n")

# Set up auxiliar variables
num_msg = 0
score1 = 0
score2 = 0
game_finished = False
winner = ''
lap = 0


############################
##        GAME LOOP
############################


what = '4'
while 1:
    
    if game_finished == False:
        #elem.send_keys(str(lap*3) + ' segundos' + Keys.RETURN)
        messages = browser.find_elements_by_class_name('message')
        new_msg = len(messages) - num_msg
        num_msg = len(messages) 
      
        for i in range(0, new_msg):
            try:
                line = messages[num_msg - new_msg + i].get_attribute("innerHTML")
                (user, message) = line.split(': ', 1)    
                message = str(message).lower().replace('"', "&quot;").replace("'", "&#39;").replace('\\', '&#92')
                
                if (user == 'FLEQBOT') and (message == (q[num_question].question).lower()) : 
                    what = '0'   #pregunta lanzada por fleqbot 
                    success = '2' #ni acierta ni falla
                    datequestion = time.time()
                    tiempo = "0"
                    numquestion = str(q[num_question].id)
    
                elif ((user == game.player1.username) and (what !='4') and (what !='3')):
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
                       
                elif ((user == game.player1.username) and (what =='4')):
                    what = '4'
                    success = '2'
                    tiempo =  "0"
                   
                elif ((user == game.player2.username)and (what !='4') and (what !='3')):
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
                        
                elif ((user == game.player2.username) and (what =='4')):
                    what = '4'
                    success = '2'
                    tiempo =  "0"
                    numquestion = "0"
                         
                elif (user == 'FLEQBOT') and not (message == (q[num_question].question).lower()): 
                    what = '3'   #mensajes de instrucciones de fleqbot 
                    success = '2' #ni acierta ni falla
                    tiempo =  "0"
                    numquestion = "0"
                 
                     
                 #escribir en el fichero de log                        
                logfile.write(str(datetime.datetime.now().time()) + ";" + user + ";" + message + ";" + what + ";" + success + ";" + tiempo + ";" + numquestion + ";\n")                       
                #logfile.write(str(datetime.datetime.now().time()) + ";" + user + ";" + message + ";\n")


                print message + " - " + q[num_question].answer + " - " + q[num_question].alt_answer1
                if (message == str(escape(q[num_question].answer)).lower() or message == str(escape(q[num_question].alt_answer1)).lower() \
                        or message == str(escape(q[num_question].alt_answer2)).lower() or message == str(escape(q[num_question].alt_answer3)).lower()) \
                        and message != "":

                    # Delete last question
                    q.remove(q[num_question])
                    ##print len(q)
                    num_question = random.randrange(len(q))

                    elem.send_keys('Respuesta correcta!' + Keys.RETURN)
                    time.sleep(2)
                    
                    #acierto = Analytics_Message(user ="cris", time = 1, success = True, attempts = 1, question = 14, game = 1, tournament = 1, number_attemps = 2, ranking = 1)
                    #acierto.save()
                    if user == game.player1.username:
                        elem.send_keys(game.player1.username + ' ha acertado!' + Keys.RETURN)
                        score1 = score1 + 1
                    elif user == game.player2.username:
                        elem.send_keys(game.player2.username + ' ha acertado!' + Keys.RETURN)
                        score2 = score2 + 1
        
                    time.sleep(3)

                    elem.send_keys(game.player1.username + " " + str(score1) + ':' + str(score2) + " " + game.player2.username + Keys.RETURN)
                    time.sleep(2)

                    if score1 == NUM_CORRECT or score2 == NUM_CORRECT:
                        game_finished = True
                        break

                    if QUESTIONS == 1:
                        elem.send_keys("Última pregunta disponible..." + Keys.RETURN)
                        time.sleep(3)

                    if QUESTIONS != 0:
                        num_question = random.randrange(len(q))
                        elem.send_keys(escape(q[num_question].question) + Keys.RETURN)
                        #logfile.write(str(datetime.datetime.now().time()) + ";FLEQBOT;" + q[num_question].question + ";\n")

                    else:
                        game_finished = True

                    QUESTIONS = QUESTIONS - 1

                    lap = 0

                    break

            except:
                pass


        if lap == 90:
            elem.send_keys("Los 90 segundos se han cumplido sin que se haya acertado la respuesta" + Keys.RETURN)
            time.sleep(3)
            elem.send_keys("La respuesta correcta era: " + q[num_question].answer + Keys.RETURN)
            time.sleep(3)

            if QUESTIONS == 1:
                elem.send_keys("Última pregunta disponible..." + Keys.RETURN)
                time.sleep(3)

            if QUESTIONS != 0:
                q.remove(q[num_question])
                ##print len(q)
                num_question = random.randrange(len(q))
                elem.send_keys(escape(q[num_question].question) + Keys.RETURN)

            else:
                game_finished = True

            QUESTIONS = QUESTIONS - 1

            lap = 0


        time.sleep(1)
        lap = lap + 1


    else:
        elem.send_keys('La partida ha terminado' + Keys.RETURN)
        time.sleep(3)
        elem.send_keys('El resultado final ha sido: ' + str(score1) + ' - ' + str(score2) + Keys.RETURN)
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
            elem.send_keys(winner.username + " ha sido el vencedor" + Keys.RETURN)
            time.sleep(2)
            elem.send_keys("ENHORABUENA!!" + Keys.RETURN)

        else:
            fleqbot = User.objects.get(username="FLEQBOT")
            game.winner = fleqbot
            elem.send_keys("Habéis empatado tras agotar el lote de preguntas disponibles para la partida" + Keys.RETURN)
            time.sleep(3)
            elem.send_keys("El sistema de puntuación aún no contempla empates, por lo que ambos habéis perdido esta partida..." + Keys.RETURN)
            time.sleep(3)
            elem.send_keys("Al empatar por lo menos habéis evitado que vuestro oponente sume una victoria, no está mal!" + Keys.RETURN)


        time.sleep(3)
        elem.send_keys("Podéis consultar la tabla del torneo para conocer la clasificación. Hasta la próxima!" + Keys.RETURN)

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


#logfile = open('/home/jorge/Escritorio/fleq_server_30oct/fleq/logs/' + str(game_id), 'r')
#logfile.seek(0)
#game.log = logfile.read().replace("\n", "<br/>")
#game.save()

logfile.close()

game.log = True
game.save()


time.sleep(2)
browser.close()
#display.stop()

