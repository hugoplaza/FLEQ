from django.http import HttpResponse
from django.shortcuts import render_to_response


def Home(request):
	print request.META['HTTP_USER_AGENT']
	#if request.mobile:
	return render_to_response('mobile/home.html', {})
	#else:
	#	return HttpResponse("pc")


def Panel(request):
	print request.META['HTTP_USER_AGENT']
	#if request.mobile:
	return render_to_response('mobile/panel.html', {})
	#else:
	#	return HttpResponse("pc")
