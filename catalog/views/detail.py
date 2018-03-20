from django.conf import settings
from django_mako_plus import view_function, jscontext
from datetime import datetime, timezone
from catalog import models as cmod
import math
from django import forms

@view_function
def process_request(request, product: cmod.Product = None):

    # # if this is a POST request we need to process the form data
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     quantity_form = QuantityForm(request.POST)
    #     # check whether it's valid:
    #     if quantity_form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         quantity_form.commit(request, product)
    #         # redirect to a new URL:
    #         return HttpResponseRedirect('/thanks/')
    #
    # # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = QuantityForm(initial={'quantity':product.quantity})

    context = {
        # sent to index.html:
        'product': product,
        # 'quantity_form': quantity_form,
        # sent to index.html and index.js:
        # jscontext(): ,
    }
    return request.dmp.render('detail.html', context)

# class QuantityForm(forms.Form):
#     '''An example form'''
#     def init(self):
#         quantity = forms.IntegerField(label='Quantity:', required=False)
#         self.fields['quantity'].widget.attrs['class'] = 'Bulk'
#
#     def clean(self):
#         if product.__class__.__name__ == 'BulkProduct':
#             if self.cleaned_data.get('quantity') == '':
#                 raise forms.ValidationError('Quantity is required')
#
#     def commit(self, request, product):
#         '''Process the form action'''
