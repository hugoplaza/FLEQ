# -*- coding: utf-8 -*-

from django import db, forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import CheckboxSelectMultiple
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.template.loader import get_template

from fleq.quizbowl.models import Category, Question, Tournament, UserProfile
from fleq.quizbowl.views_language import strLang, setBox
from fleq.quizbowl.views_tournaments_api import *

# Create sid of new Tournament
import re
import unicodedata
import datetime



##################################
# NEW TOURNAMENT
##################################

class TournamentForm(ModelForm):
	class Meta:
		model = Tournament
		fields = ('name', 'categories', 'start_date', 'only_mobile_devices', 'days_per_round', 'rounds', 'optional_info')
		widgets = {
			'start_date': SelectDateWidget(),
			'categories': CheckboxSelectMultiple,
		}
	
	def clean_name(self):
		name = self.cleaned_data.get('name')
		try:
			tournament = Tournament.objects.get(name=name)
		except Tournament.DoesNotExist:
			return name
		raise	forms.ValidationError(strLang()['error_new_tournament_name_exists'])




def NewTournament(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/register')

	elif not request.user.is_superuser and not request.user.has_perm('fleq.quizbowl.add_tournament'):
		return HttpResponseRedirect('/my-tournaments')


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
			return HttpResponseRedirect('/next-tournaments')

		else:
			
# 			return render_to_response('custom/new-tournament.html', {
# 				'user_me': request.user,
# 				'form': form,
# 				'lang': lang,
# 			})

			return HttpResponse(get_template('custom/new-tournament.html').render(RequestContext(request, {
				'user_me': request.user,
				'form': form,
				'lang': lang,
			})))


	else:

 		form = TournamentForm(initial={'start_date': (datetime.date.today() + datetime.timedelta(days=1))})
 
# 		return render_to_response('custom/new-tournament.html', {
# 			'user_me': request.user,
# 			'form': form,
# 			'lang': lang,
# 		})

		return HttpResponse(get_template('custom/new-tournament.html').render(RequestContext(request, {
			'user_me': request.user,
			'form': form,
			'lang': lang,
		})))





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
		
		q = Question(use_phonetic = 0,question = fields[1], answer = fields[2])
#		q = Question(use_phonetic = 0, question = fields[1], answer = fields[2])


        try: 
            q.alt_answer1 = fields[3]
            q.alt_answer2 = fields[4]
            q.alt_answer3 = fields[5]
        except IndexError:  # none or not all alt_answers were provided 
            pass
            
        try:
            q.save()
            count = count + 1
            print str(count) + " " + line
        except db.utils.IntegrityError: # question already exists
            q = Question.objects.get(question = fields[1])

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
#@csrf_exempt
def LoadQuestions(request):

	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if not request.user.is_superuser:
		return HttpResponseRedirect('/')

	# Load strings language to template loadquestions.html
	try:
		lang = strLang()
	except:
		lang = ''


	if request.method == 'POST':
		print "POST"
		form = LoadQuestionsForm(request.POST, request.FILES)
		# Load strings language to template loadquestions.html

		if form.is_valid():
			loadQuestionsFile(request.FILES['questions_file'])
			return HttpResponseRedirect('/load-questions?status=success_load_questions')

		else:
# 			return render_to_response('custom/load-questions.html', {
# 				'user_me': request.user,
# 				'form': form,
# 				'lang': lang,
# 			})
			return HttpResponse(get_template('custom/load-questions.html').render(RequestContext(request, {
			    'user_me': request.user,
 				'form': form,
 				'lang': lang,
 			})))																					
       
        
	else:

		# Must we show a notification user?
		try:
	 		if request.GET['status']:
	 			box = setBox(request.GET['status'])

				return HttpResponse(get_template('custom/load-questions.html').render(RequestContext(request, {
					'box': box,
					'user_me': request.user,
					'lang': lang,
				})))
		except:
			box = ''
	
		form = LoadQuestionsForm()
		
		#return render_to_response('custom/load-questions.html', {
		#	'form': form,
		#	'box': box,
		#	'user_me': request.user,
		#	'lang': lang,
		#})
				
		return HttpResponse(get_template('custom/load-questions.html').render(RequestContext(request, {
			'form': form,
			'box': box,
			'user_me': request.user,
			'lang': lang,
		})))
