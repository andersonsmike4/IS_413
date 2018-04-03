from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from formlib import Formless
import math
from django import forms

@view_function
def process_request(request, product: cmod.Product = None):

    # overwrite the submit button text
    Formless.submit_text = None

    # determine if the current product is already in last five viewed
    if product in request.last_five:
        del request.last_five[request.last_five.index(product)]
    # add current product to last five
    request.last_five.insert(0, product)

    # add to cart form
    add_to_cart_form = AddToCartForm(request, prod=product, initial={'quantity': 1, 'id':product.id})
    # check whether it's valid:
    if add_to_cart_form.is_valid():
        # process the data in form.cleaned_data as required
        add_to_cart_form.commit()
        # redirect to cart:
        return HttpResponseRedirect('/catalog/cart/')

    context = {
        # sent to index.html:
        'product': product,
        'add_to_cart_form': add_to_cart_form,
        # sent to index.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('detail.html', context)

class AddToCartForm(Formless):
    '''An example form'''
    def init(self):
        self.fields['id'] = forms.CharField(widget=forms.HiddenInput)
        if self.prod.__class__.__name__ == 'BulkProduct':
            self.fields['quantity'] = forms.IntegerField(label='Quantity:', required=False, min_value=1, max_value=self.prod.quantity)
        else:
            self.fields['quantity'] = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def clean_quantity(self):
        if self.prod.__class__.__name__ == 'BulkProduct':
            if self.cleaned_data.get('quantity') == '':
                raise forms.ValidationError('Quantity is required')


        return self.cleaned_data.get('quantity')
    # def clean(self):
    #
    #
    def commit(self, request, product):
        '''Process the form action'''
        item.quantity = self.cleaned_data.get('quantity')
