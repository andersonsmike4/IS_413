from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod

@view_function
def process_request(request, product:cmod.Product):
    # initial=forms.model_to_dict(product)
# initial={'name':product.name, 'description':product.description, 'category': product.category.name}
    # process the form

    product_form = ProductForm(request, initial=forms.model_to_dict(product))
    if product_form.is_valid():
        product_form.commit()
        return HttpResponseRedirect('/manager/product_list/')

    # render the template
    return request.dmp_render('modify_product.html', {
        'product_form': product_form,
    })


class ProductForm(Formless):
    '''An example form'''
    def init(self):
        '''Adds the fields for product form'''
        self.fields['name'] = forms.CharField(label='Product Name:', required=True)
        self.fields['description'] = forms.CharField(label='Product Description:', required=True, widget=forms.Textarea)

        # I don't know how to implement these
        # self.fields['category'] = forms.ModelChoiceField(label='Category:', required=True, queryset=cmod.Category.objects.all())
        # self.fields['TYPE_CHOICES'] = forms.ChoiceField(label='Type', required=True, choices=cmod.Product.STATUS_CHOICES)

        self.fields['price'] = forms.CharField(label='Price:', required=True)
        self.fields['status'] = forms.ChoiceField(label='Status:', required=True, choices=cmod.Product.STATUS_CHOICES, widget=forms.RadioSelect)

    def clean(self):

        return name

    def commit(self):
        '''Process the form action'''
