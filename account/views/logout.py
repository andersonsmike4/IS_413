from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from django.contrib.auth import logout

@view_function
def process_request(request):
    logout(request)
    return HttpResponseRedirect('/account/index/')
