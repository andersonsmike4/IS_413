from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
import math
from django import forms
import traceback
from django.http import HttpResponseRedirect


@view_function
def process_request(request):
    cart = request.user.get_shopping_cart()
    cart.recalculate()
    checkout_form = CheckoutForm(request)
    checkout_form.submit_text=None

    if checkout_form.is_valid():
        checkout_form.commit(request, cart)
        return HttpResponseRedirect('/catalog/thanks/')

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
        self.fields['ship_fname'] = forms.CharField(label='First Name', required=True)
        self.fields['ship_lname'] = forms.CharField(label='Last Name', required=True)
        self.fields['ship_address'] = forms.CharField(label='Street Address', required=True)
        self.fields['ship_city'] = forms.CharField(label='City', required=True)
        self.fields['ship_state'] = forms.CharField(label='State', required=True)
        self.fields['ship_zip_code'] = forms.CharField(label='Zip Code', required=True)
        self.fields['stripeToken'] = forms.CharField(widget=forms.HiddenInput)


    def clean(self):

        cart = self.request.user.get_shopping_cart()
        stripeToken = self.cleaned_data.get('stripeToken')
        try:
            cart.finalize(stripeToken)
            print('>>>>>>>>>>>>>>>>>>> We got this far')

        except:
            print('>>>>>>>>>>>', traceback.print_exc)
            raise forms.ValidationError("Transaction was not recorded. Please Try again.")

        return self.cleaned_data




    def commit(self, request, cart):
        '''Process the form action'''
        cart.ship_name = (str(self.cleaned_data.get('lname')) + ', ' + str(self.cleaned_data.get('fname')))
        cart.ship_address = self.cleaned_data.get('ship_address')
        cart.ship_city = self.cleaned_data.get('ship_city')
        cart.ship_state = self.cleaned_data.get('ship_state')
        cart.ship_zip_code = self.cleaned_data.get('ship_zip_code')
        cart.ship_date = datetime.now()
        cart.save()
