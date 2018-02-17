from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod

@view_function
def process_request(request, product: cmod.Product):

    product.status = 'I'
    product.save()
    return HttpResponseRedirect('/manager/product_list/')
