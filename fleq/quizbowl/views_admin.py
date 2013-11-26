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
#                    Félix Redondo <felix.redondo.sierra@gmail.com>			 #
#                                                                           #
#############################################################################

from django import db, forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import datetime

from fleq.quizbowl.models import Category, Question, Tournament, UserProfile
from fleq.quizbowl.views_language import strLang, setBox
from fleq.quizbowl.views_tournaments_api import *

# Create sid of new Tournament
import re
import unicodedata

##################################
# NEW TOURNAMENT
##################################

class TournamentForm(ModelForm):
	class Meta:
		model = Tournament
		fields = ('name', 'categories', 'start_date', 'days_per_round', 'rounds', 'optional_info')
		widgets = {
			'start_date': SelectDateWidget(),
		}
	
	def clean_name(self):
		name = self.cleaned_data.get('name')
		try:
			tournament = Tournament.objects.get(name=name)
		except Tournament.DoesNotExist:
			return name
		raise	forms.ValidationError(strLang()['error_new_tournament_name_exists'])

def newTournament(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')
	elif not request.user.is_superuser and not request.user.has_perm('fleq.quizbowl.add_tournament'):
		return HttpResponseRedirect('/my-tournaments')

	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	pendingQR = myAdminPendingQuestionReviews(request.user)

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# Load strings language to template newtournament.html
	try:
		lang = strLang()
	except:
		lang = ''

	# Info about user
	user_me = UserProfile.objects.get(user=request.user)

	if request.method == 'POST': # If the form has been submitted...
		form = TournamentForm(request.POST) # A form bound to the POST data
		if form.is_valid():
			
			t = form.save()
			t.admin = request.user
			
			# Generate sid name
			sid = t.name.lower()
			sid = sid.replace(" ", "")
			# Remove accents
			sid = ''.join((c for c in unicodedata.normalize('NFD', sid) if unicodedata.category(c) != 'Mn'))
			# Remove special chars
			sid = re.sub(r"\W+", "", sid)
			# Check if this sid exists or similars
			ts = Tournament.objects.filter(sid__startswith=sid)
			if len(ts) > 0:
				sid = sid + '-' + str(len(ts))			
			
			t.sid = sid
			
			t.finish_date = t.start_date + datetime.timedelta((t.rounds * t.days_per_round) -1)
			t.save()
			return HttpResponseRedirect('/admin/new-tournament?status=success_create_new_tournament')
		else:
			return render_to_response('newtournament.html', {
				'user_me': user_me,
				'form': form,
				'lang': lang,
				'myTournaments': myTournaments,
				'myAdminTournaments': myAdmnTournaments,
				'todayGames': todayGames,
				'nextGames': nextGames,
				'admin_user': admin_user,
				'pendingQR': pendingQR,
			})
	else: # If get request, generate a new form
 		form = TournamentForm(initial={'start_date': datetime.date.today()})

		# Must we show a notification user?
		try:
	 		if request.GET['status']:
	 			box = setBox(request.GET['status'])
		except:
			box = ''
 
		return render_to_response('newtournament.html', {
			'user_me': user_me,
			'form': form,
			'lang': lang,
			'box': box,
			'myTournaments': myTournaments,
			'myAdminTournaments': myAdmnTournaments,
			'todayGames': todayGames,
			'nextGames': nextGames,		
			'admin_user': admin_user,	
			'pendingQR': pendingQR,
		})

##################################
# LOAD QUESTIONS
##################################

class LoadQuestionsForm(forms.Form):
    questions_file  = forms.FileField()

# Function called by loadQuestions(request) that extracts and saves all questions received in a file
def loadQuestionsFile(questionsFile):
    count = 0
    for line in questionsFile:
        fields = line.rstrip('\n').split(';')
        fields = fields[:-1]  # ommits the last empty string 

        print fields[2]
        print fields[3]
        q = Question(use_phonetic = 0, question = fields[2], answer = fields[3])

        try: 
            q.alt_answer1 = fields[4]
            q.alt_answer2 = fields[5]
            q.alt_answer3 = fields[6]
        except IndexError:  # none or not all alt_answers were provided 
            pass
            
        try:
            q.save()
            count = count + 1
            print str(count) + " " + line
        except db.utils.IntegrityError: # question already exists
            q = Question.objects.get(question = fields[2])

        for category in fields[0].split(','):
            category = category.lower()
            try:
                c = Category.objects.get(name = category)
            except Category.DoesNotExist:
                c = Category(name = category)
                c.save()
            q.categories.add(c)
            q.save()

# Handle files loaded in admin panel to save them in the system
@csrf_exempt
def loadQuestions(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')

	if not request.user.is_superuser and not request.user.has_perm('fleq.quizbowl.add_tournament'):
		return HttpResponseRedirect('/my-tournaments')

	# SIDEBAR INFO
	myTournaments = myActiveTournaments(request)
	myAdmnTournaments = myAdminTournaments(request)
	todayGames = myTodayGames(request)
	nextGames = myNextGames(request)
	pendingQR = myAdminPendingQuestionReviews(request.user)

	# Info about user
	user_me = UserProfile.objects.get(user=request.user)

	# Load strings language to template loadquestions.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	if request.method == 'POST':
		form = LoadQuestionsForm(request.POST, request.FILES)
		# Load strings language to template loadquestions.html
		if form.is_valid():
			loadQuestionsFile(request.FILES['questions_file'])
			return HttpResponseRedirect('/admin/load-questions?status=success_load_questions')
		else:
			return render_to_response('loadquestions.html', {
				'user_me': user_me,
				'form': form,
				'lang': lang,
				'myTournaments': myTournaments,
				'myAdminTournaments': myAdmnTournaments,
				'todayGames': todayGames,
				'nextGames': nextGames,
				'admin_user': admin_user,
				'pendingQR': pendingQR,
			})            
	else:
	
		# Must we show a notification user?
		try:
	 		if request.GET['status']:
	 			box = setBox(request.GET['status'])
		except:
			box = ''
	
		form = LoadQuestionsForm()
		return render_to_response('loadquestions.html', {
			'form': form,
			'user_me': user_me,
			'lang': lang,
			'box': box,
			'myTournaments': myTournaments,
			'myAdminTournaments': myAdmnTournaments,
			'todayGames': todayGames,
			'nextGames': nextGames,	
			'admin_user': admin_user,
			'pendingQR': pendingQR,	
		})
