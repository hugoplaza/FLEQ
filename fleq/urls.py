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
#                    Félix Redondo <felix.redondo.sierra@gmail.com>         #
#                                                                           #
#############################################################################

#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url, include
from django.views.generic import *
import settings

from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
					

	(r'^admin/', include(admin.site.urls)),
	(r'^admin/new-tournament/', 'fleq.quizbowl.views_admin.newTournament'),
	(r'^admin/load-questions/', 'fleq.quizbowl.views_admin.loadQuestions'),
	

  
    # Media
	(r'css/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': 'template/css'}),
	(r'images/(?P<path>.*)$', 'django.views.static.serve', 
	{'document_root': 'template/images'}),
	(r'js/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': 'template/js'}),



	# New website
    url('^$', 'fleq.quizbowl.views_custom_connect.Home'),
	url('^signin$', 'fleq.quizbowl.views_custom_connect.Signin'),
	url('^logout$', 'fleq.quizbowl.views_custom_connect.Logout'),
	#url('^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),	
	
	url('^welcome$', 'fleq.quizbowl.views_custom_connect.Welcome'),
	url('^stepbystep$', 'fleq.quizbowl.views_custom_connect.StepbyStep'),
	url('^cargarlogs$', 'fleq.quizbowl.views_custom_connect.CargarLogs'),
	url('^FAQ$', 'fleq.quizbowl.views_custom_connect.FAQ'),

	url('^my-tournaments$', 'fleq.quizbowl.views_custom_tournaments.MyTournaments'),
	url('^active-tournaments$', 'fleq.quizbowl.views_custom_tournaments.ActiveTournaments'),
	url('^next-tournaments$', 'fleq.quizbowl.views_custom_tournaments.NextTournaments'),
	url('^finished-tournaments$', 'fleq.quizbowl.views_custom_tournaments.FinishedTournaments'),

	url('^new-tournament$', 'fleq.quizbowl.views_custom_admin.NewTournament'),
	url('^load-questions$', 'fleq.quizbowl.views_custom_admin.LoadQuestions'),

	url('^tournament/(?P<gid>\d+)$', 'fleq.quizbowl.views_custom_tournaments.TournamentStatistics'),
	url('^tournament/(?P<gid>\d+)/join$', 'fleq.quizbowl.views_custom_tournaments.JoinTournament'),
	url('^tournament/(?P<gid>\d+)/disjoin$', 'fleq.quizbowl.views_custom_tournaments.DisjoinTournament'),

	url('^next-games$', 'fleq.quizbowl.views_custom_games.NextGames'),
	url('^won-games$', 'fleq.quizbowl.views_custom_games.WonGames'),
	url('^lost-games$', 'fleq.quizbowl.views_custom_games.LostGames'),


	url('^game-room/(?P<gid>\d+)$', 'fleq.quizbowl.views_custom_games.GameRoom'),
   	url('^game-room/(?P<gid>\d+)/select-time$', 'fleq.quizbowl.views_custom_games.SelectStartTime'),   
   	url('^game-room/(?P<gid>\d+)/delete-time$', 'fleq.quizbowl.views_custom_games.DeleteStartTime'),


   	# Analytics
	#url('^analytics/categories$', 'fleq.quizbowl.views_custom_analytics.Categories'),
	#url('^analytics/questions$', 'fleq.quizbowl.views_custom_analytics.Questions'),
	url('^analytics/questions/(?P<gid>\d+)$', 'fleq.quizbowl.views_custom_analytics.Questionsgid'),
	url('^analytics/categories/(?P<gid>\d+)$', 'fleq.quizbowl.views_custom_analytics.Categoriesgid'),
   	url('^analytics/absences/(?P<gid>\d+)$', 'fleq.quizbowl.views_custom_analytics.Absences'),
   	url('^analytics/questionsless/(?P<gid>\d+)$', 'fleq.quizbowl.views_custom_analytics.Questionsless'),
   	url('^analytics/successtime/(?P<gid>\d+)$', 'fleq.quizbowl.views_custom_analytics.Successtime'),
   	url('^analytics/general/(?P<gid>\d+)$', 'fleq.quizbowl.views_custom_analytics.General'),
   	
   	



	# Mobile
    #url('^mobile$', 'fleq.quizbowl.views_mobile_connect.Login'),
	#url('^mobile/signin$', 'fleq.quizbowl.views_mobile_connect.Signin'),
	#url('^mobile/logout$', 'fleq.quizbowl.views_mobile_connect.Logout'),
	#url('^mobile/welcome$', 'fleq.quizbowl.views_mobile_connect.Welcome'),

	#url('^mobile/my-tournaments$', 'fleq.quizbowl.views_mobile_tournaments.MyTournaments'),
	#url('^mobile/active-tournaments$', 'fleq.quizbowl.views_mobile_tournaments.ActiveTournaments'),
	#url('^mobile/next-tournaments$', 'fleq.quizbowl.views_mobile_tournaments.NextTournaments'),
	#url('^mobile/finished-tournaments$', 'fleq.quizbowl.views_mobile_tournaments.FinishedTournaments'),

	#url('^mobile/tournament/(?P<gid>\d+)$', 'fleq.quizbowl.views_mobile_tournaments.TournamentStatistics'),
	#url('^mobile/tournament/(?P<gid>\d+)/join$', 'fleq.quizbowl.views_mobile_tournaments.JoinTournament'),
	#url('^mobile/tournament/(?P<gid>\d+)/disjoin$', 'fleq.quizbowl.views_mobile_tournaments.DisjoinTournament'),

	#url('^mobile/next-games$', 'fleq.quizbowl.views_mobile_games.NextGames'),
	#url('^mobile/won-games$', 'fleq.quizbowl.views_mobile_games.WonGames'),
	#url('^mobile/lost-games$', 'fleq.quizbowl.views_mobile_games.LostGames'),


	#url('^mobile/game-room/(?P<gid>\d+)$', 'fleq.quizbowl.views_mobile_games.GameRoom'),
   	#url('^mobile/game-room/(?P<gid>\d+)/select-time$', 'fleq.quizbowl.views_mobile_games.SelectStartTime'),   
   	#url('^mobile/game-room/(?P<gid>\d+)/delete-time$', 'fleq.quizbowl.views_mobile_games.DeleteStartTime'),

	#url('^(.*)$', 'fleq.quizbowl.views_custom_connect.PageNotFound'),

)


#urlpatterns += patterns('django.views.generic.simple',
#	(r'^login/$', 'direct_to_template', {'template': 'login.html'}),
#)


"""

   #(r'^$', 'fleq.quizbowl.views_menu.home'),
	(r'^$', 'fleq.quizbowl.views_custom_connect.Login'), 

	(r'^my-question-reviews/', 'fleq.quizbowl.views_games.myQuestionReviews'),
   (r'^question-review/(?P<gid>\d+)/add/', 'fleq.quizbowl.views_games.newQuestionReview'),   
   (r'^question-review/(?P<qrid>\d+)/$', 'fleq.quizbowl.views_games.questionReview'),
   
   (r'^register/$', 'fleq.quizbowl.views_connect.register'),
   (r'^recover-account/(?P<ruid>[a-z0-9A-Z]+)', 'fleq.quizbowl.views_connect.recoverAccountNewPassword'),
   (r'^recover-account/', 'fleq.quizbowl.views_connect.recoverAccount'),   
   (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),   
  	(r'^login/$', 'fleq.quizbowl.views_connect.mylogin'),
  	
	#(r'^logout/$', 'fleq.quizbowl.views_connect.mylogout'),
	(r'^logout/$', 'fleq.quizbowl.views_custom_connect.Logout'),
  	
	(r'^edit-profile/', 'fleq.quizbowl.views_connect.editProfile'),
	(r'^change-password/', 'fleq.quizbowl.views_connect.changePassword'),	
  	
   (r'^my-tournaments/', 'fleq.quizbowl.views_tournaments.myTournaments'),
   (r'^tournaments/(?P<sid>[a-z0-9A-Z]+)/join', 'fleq.quizbowl.views_tournaments.tournamentJoin'),   
   (r'^tournaments/(?P<sid>[a-z0-9A-Z]+)', 'fleq.quizbowl.views_tournaments.tournamentInfo'),
   (r'^tourna ments/(?P<sid>[a-z0-9A-Z]+)', 'fleq.quizbowl.views_tournaments.tournamentInfo'),
   (r'^tournaments/', 'fleq.quizbowl.views_tournaments.tournaments'),
   
   (r'^won-games$', 'fleq.quizbowl.views_games.wonGames'),
   (r'^lost-games$', 'fleq.quizbowl.views_games.lostGames'),

   (r'^my-next-games/', 'fleq.quizbowl.views_games.myNextGamesView'),   
   (r'^games/(?P<gid>\d+)/select-time', 'fleq.quizbowl.views_games.selectStartTime'),   
   (r'^games/(?P<gid>\d+)/delete-time', 'fleq.quizbowl.views_games.deleteStartTime'),   
   (r'^games/(?P<gid>\d+)', 'fleq.quizbowl.views_games.gameInfo'),
   
   (r'^ranking/', 'fleq.quizbowl.views_ranking.ranking'),   
   
   (r'^play/', 'fleq.quizbowl.views_play.webplay'),

   (r'^what-is-fleq/', 'fleq.quizbowl.views_faqinfo.whatIsFleq'),
   (r'^rules/', 'fleq.quizbowl.views_faqinfo.rules'),
   (r'^faq/', 'fleq.quizbowl.views_faqinfo.faq'),
   (r'^how-to-play/', 'fleq.quizbowl.views_faqinfo.howToPlay'),
   (r'^contact/', 'fleq.quizbowl.views_faqinfo.contact'),


"""


