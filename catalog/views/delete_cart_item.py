from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
import math
from django import forms
from django.contrib.auth.decorators import login_required

@login_required
@view_function
def process_request(request, item: cmod.OrderItem = None):

    item.status = 'deleted'    
    item.save()

    return HttpResponseRedirect('/catalog/cart/')
