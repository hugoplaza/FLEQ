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

from django.shortcuts import render_to_response

from fleq.quizbowl.views_language import strLang
from fleq.quizbowl.views_notify import contactEmail
from fleq.quizbowl.views_tournaments_api import *
from fleq.quizbowl.models import UserProfile

def whatIsFleq(request):   

	# Load strings language to template admin.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR INFO
	if request.user.is_active:
		myTournaments = myActiveTournaments(request)
		myAdmnTournaments = myAdminTournaments(request)
		todayGames = myTodayGames(request)
		nextGames = myNextGames(request)
		# Info about user
		user_me = UserProfile.objects.get(user=request.user)
		pendingQR = myAdminPendingQuestionReviews(request.user)
	else:
		myTournaments = ""
		myAdmnTournaments = ""
		todayGames = ""
		nextGames = ""
		user_me = request.user
		pendingQR = 0

	return render_to_response('whatisfleq.html', {
		'user_me': user_me,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,	
	})

def rules(request):   

	# Load strings language to template rules.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR INFO
	if request.user.is_active:
		myTournaments = myActiveTournaments(request)
		myAdmnTournaments = myAdminTournaments(request)
		todayGames = myTodayGames(request)
		nextGames = myNextGames(request)
		# Info about user
		user_me = UserProfile.objects.get(user=request.user)
		pendingQR = myAdminPendingQuestionReviews(request.user)
	else:
		myTournaments = ""
		myAdmnTournaments = ""
		todayGames = ""
		nextGames = ""
		user_me = request.user
		pendingQR = 0

	return render_to_response('rules.html', {
		'user_me': user_me,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,		
	})

def faq(request):   

	# Load strings language to template faq.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR INFO
	if request.user.is_active:
		myTournaments = myActiveTournaments(request)
		myAdmnTournaments = myAdminTournaments(request)
		todayGames = myTodayGames(request)
		nextGames = myNextGames(request)
		# Info about user
		user_me = UserProfile.objects.get(user=request.user)
		pendingQR = myAdminPendingQuestionReviews(request.user)
	else:
		myTournaments = ""
		myAdmnTournaments = ""
		todayGames = ""
		nextGames = ""
		user_me = request.user
		pendingQR = 0

	return render_to_response('faq.html', {
		'user_me': user_me,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})

def howToPlay(request):   

	# Load strings language to template howtoplay.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR INFO
	if request.user.is_active:
		myTournaments = myActiveTournaments(request)
		myAdmnTournaments = myAdminTournaments(request)
		todayGames = myTodayGames(request)
		nextGames = myNextGames(request)
		# Info about user
		user_me = UserProfile.objects.get(user=request.user)
		pendingQR = myAdminPendingQuestionReviews(request.user)		
	else:
		myTournaments = ""
		myAdmnTournaments = ""
		todayGames = ""
		nextGames = ""
		user_me = request.user
		pendingQR = 0

	return render_to_response('howtoplay.html', {
		'user_me': user_me,
		'lang': lang,
		'myTournaments': myTournaments,
		'myAdminTournaments': myAdmnTournaments,
		'todayGames': todayGames,
		'nextGames': nextGames,
		'admin_user': admin_user,
		'pendingQR': pendingQR,
	})

class ContactForm(forms.Form):

	SUBJECT_CHOICES = (
		('Problem with a game', 'Problem with a game'),
		('Problem with a Tournament', 'Problem with a Tournament'),
		('Problem with Stats', 'Problem with Stats'),		
		('Want information about FLEQ', 'Want information about FLEQ'),		
		('Permissions to create tournaments', 'Permissions to create tournaments'),
		('Problem described in the message (other)', 'Problem described in the message (other)'),
	)

	email = forms.EmailField(max_length=100)
	subject = forms.CharField(widget=forms.Select(choices=SUBJECT_CHOICES))
	message = forms.CharField(widget=forms.Textarea)

	def clean_subject(self):
		subject = self.cleaned_data.get('subject')
		if not subject:
			raise forms.ValidationError(strLang()['error_contact_empty_subject'])
		return subject

	def clean_message(self):
		message = self.cleaned_data.get('message')
		if not message:
			raise forms.ValidationError(strLang()['error_contact_empty_message'])
		return message

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not email:
			raise forms.ValidationError(strLang()['error_contact_empty_email'])
		return email

def contact(request):
	# Load strings language to template howtoplay.html
	try:
		lang = strLang()
	except:
		lang = ''

	if request.user.has_perm('fleq.quizbowl.add_tournament'):
		admin_user = True
	else:
		admin_user = False

	# SIDEBAR INFO
	if request.user.is_active:
		myTournaments = myActiveTournaments(request)
		myAdmnTournaments = myAdminTournaments(request)
		todayGames = myTodayGames(request)
		nextGames = myNextGames(request)
		# Info about user
		user_me = UserProfile.objects.get(user=request.user)		
		pendingQR = myAdminPendingQuestionReviews(request.user)
	else:
		myTournaments = ""
		myAdmnTournaments = ""
		todayGames = ""
		nextGames = ""
		user_me = request.user
		pendingQR = 0

	if request.method == 'POST':
		contactForm = ContactForm(request.POST) # A form bound to the POST data
		if contactForm.is_valid():
			info = {}
			info['subject'] = request.POST['subject']
			info['message'] = request.POST['message']
			info['userEmail'] = request.POST['email']

			contactEmail(info)

			# We show a notification user
			try:
	 			box = setBox('success_contact_sent')
			except:
				box = ''

			contactForm = ContactForm()

			return render_to_response('contact.html', {
				'user_me': user_me,
				'contactForm': contactForm,
				'box': box,
				'myTournaments': myTournaments,
				'myAdminTournaments': myAdmnTournaments,
				'todayGames': todayGames,
				'nextGames': nextGames,
				'contactForm': contactForm,
				'admin_user': admin_user,
				'pendingQR': pendingQR,
			})
		else:
			return render_to_response('contact.html', {
				'user_me': user_me,
				'contactForm': contactForm,
				'myTournaments': myTournaments,
				'myAdminTournaments': myAdmnTournaments,
				'todayGames': todayGames,
				'nextGames': nextGames,
				'contactForm': contactForm,
				'admin_user': admin_user,
				'pendingQR': pendingQR,
			})
	else: # If get request, generate a new form
		contactForm = ContactForm()

		# Must we show a notification user?
		try:
	 		if request.GET['status']:
	 			box = setBox(request.GET['status'])
		except:
			box = ''

		return render_to_response('contact.html', {
			'user_me': user_me,
			'lang': lang,
			'myTournaments': myTournaments,
			'myAdminTournaments': myAdmnTournaments,
			'todayGames': todayGames,
			'nextGames': nextGames,
			'contactForm': contactForm,
			'admin_user': admin_user,
			'pendingQR': pendingQR,
		})
