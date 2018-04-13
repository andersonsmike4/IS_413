from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
import math
from django import forms

from django.http import HttpResponseRedirect


@view_function
def process_request(request):
    cart = request.user.get_shopping_cart()
    cart.recalculate()
    checkout_form = CheckoutForm(request)
    checkout_form.submit_text=None
    if checkout_form.is_valid():
        checkout_form.commit(request)
        return HttpResponseRedirect('/catalog/thanks')

    context = {
        # sent to index.html:
        'checkout_form': checkout_form,
        'cart': cart,
        # sent to index.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('checkout.html', context)

class CheckoutForm(Formless):
    def init(self):
        self.fields['ship_fname'] = forms.CharField(label='First Name')
        self.fields['ship_lname'] = forms.CharField(label='Last Name')
        self.fields['ship_address'] = forms.CharField(label='Street Address')
        self.fields['ship_city'] = forms.CharField(label='City')
        self.fields['ship_state'] = forms.CharField(label='State')
        self.fields['ship_zip_code'] = forms.CharField(label='Zip Code')
        self.fields['stripetToken'] = forms.CharField(widget=forms.HiddenInput)


    def clean(self):
        pass

    def commit(self, request):
        '''Process the form action'''
        pass
