#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings

setup_environ(settings)

from quizbowl.models import Game, Preferred_start_time, Round, Score
from quizbowl.views_notify import notify_user
from random import choice
import datetime
import sys


r = Round.objects.filter(start_date = datetime.date.today())


for round in r:
        
    s = Score.objects.filter(tournament = round.tournament.id).order_by('player_profile__timezone', 'points', '?') 
    # get'em ordered first by points, second randomly

    for r in s:
        print r.player.username
        print r.player_profile.timezone
    
    scores = list(s)

    if len(scores)%2:
        # if the number of players is odd, a random player is earned with 1 point and won't play this round  
        lucky_score = choice(scores)
        lucky_score.points += 1
        lucky_score.save()
        scores.remove(lucky_score)
        notify_user(lucky_score.player, 'meditation_round', round)

    while scores:
        player1 = scores.pop().player
        player2 = scores.pop().player
        default_date = round.finish_date 
        default_time = datetime.time(21,00)
        default_start_time = datetime.datetime.combine(default_date, default_time)
        
        game = Game(start_time = default_start_time, player1 = player1, player2 = player2, score_player1 = 0, score_player2 = 0, winner = round.tournament.admin, round = round)
        game.save()
        
        notify_user(player1, 'new_game', round)
        notify_user(player2, 'new_game', round)
        
        pst = Preferred_start_time(player = game.player1, game = game)
        pst.save()
        pst = Preferred_start_time(player = game.player2, game = game)
        pst.save()
