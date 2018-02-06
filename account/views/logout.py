from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms

@view_function
def process_request(request):

    context = {

    }
    return request.dmp_render('signup.html', context)
