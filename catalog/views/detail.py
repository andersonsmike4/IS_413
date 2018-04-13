from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
from account import models as amod
from formlib import Formless
import math
from django import forms

@view_function
def process_request(request, product: cmod.Product = None):
    # determine if the current product is already in last five viewed
    if product in request.last_five:
        del request.last_five[request.last_five.index(product)]
    # add current product to last five
    request.last_five.insert(0, product)

    # set inital data
    initial={'quantity': 1, 'id':product.id}

    # get quantiy available and set initial to Out of Stock if there is none avialable
    cart = request.user.get_shopping_cart().items.all()
    if product.__class__.__name__ == 'BulkProduct':
        quant_avail = product.quantity
        for c in cart:
            if product.name == c.description:
                quant_avail = product.quantity - c.quantity
                if quant_avail == 0:
                    initial={'quantity': 'Out of Stock', 'id':product.id}

    # add to cart form
    add_to_cart_form = AddToCartForm(request, prod=product, initial=initial)

    # overwrite the submit button text
    add_to_cart_form.submit_text = None

    # check whether it's valid:
    if add_to_cart_form.is_valid():
        # process the data in form.cleaned_data as required
        add_to_cart_form.commit(request, product)
        # redirect to cart:
        return HttpResponseRedirect('/catalog/cart/')
    price = product.price
    context = {
        # sent to index.html:
        'product': product,
        'add_to_cart_form': add_to_cart_form,
        # sent to index.html and index.js:
        jscontext('price'): price,
    }
    return request.dmp.render('detail.html', context)

class AddToCartForm(Formless):
    '''An example form'''
    def init(self):
        self.fields['id'] = forms.CharField(widget=forms.HiddenInput)
        cart = self.request.user.get_shopping_cart().active_items()
        min = 1
        if self.prod.__class__.__name__ == 'BulkProduct':
            quant_avail = self.prod.quantity

            for c in cart:
                if self.prod.name == c.description:
                    quant_avail = self.prod.quantity - c.quantity
                    if quant_avail == 0:
                        min = 0
        if min == 0:
            self.fields['quantity'] = forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}), label='Quantity:', required=True)
        else:
            if self.prod.__class__.__name__ == 'BulkProduct':
                self.fields['quantity'] = forms.IntegerField(label='Quantity:', required=True, min_value=min, max_value=quant_avail)
            else:
                self.fields['quantity'] = forms.IntegerField(widget=forms.HiddenInput)

    def clean_quantity(self):
        # make sure quantity field is not empty
        if self.prod.__class__.__name__ == 'BulkProduct':
            if self.cleaned_data.get('quantity') == '':
                raise forms.ValidationError('Quantity is required')
            if self.cleaned_data.get('quantity') == 'Out of Stock':
                raise forms.ValidationError('This Item is Out of Stock')

        # check availability



        return self.cleaned_data.get('quantity')
    # def clean(self):
    #
    #
    def commit(self, request, product):
        '''Process the form action'''
        order = request.user.get_shopping_cart()
        item = order.get_item(product=product, create=True)
        if product.__class__.__name__ == 'BulkProduct':
            item.quantity += self.cleaned_data.get('quantity')
        else:
            item.quantity = self.cleaned_data.get('quantity')
        item.description = product.name
        item.recalculate()
        order.recalculate()
        item.save()
        order.save()
