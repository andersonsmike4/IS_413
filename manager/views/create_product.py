from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod
import re

@view_function
def process_request(request):
    # try:
    #     product = cmod.Product.objects.get(pk=request.urlparams[0])
    # except:
    #     pass

    create_form = CreateForm(request)

    if create_form.is_valid():
        create_form.commit()
        return HttpResponseRedirect('/manager/product_list/')

    # render the template
    return request.dmp_render('create_product.html', {
        'create_form': create_form,
    })


class CreateForm(Formless):
    '''An example form'''
    def init(self):
        '''Adds the fields for product form'''
        self.fields['status'] = forms.ChoiceField(label='Status:', required=True, choices=cmod.Product.STATUS_CHOICES)
        # widget=forms.RadioSelect(),
        self.fields['type'] = forms.ChoiceField(label='Type', required=True, choices=cmod.Product.TYPE_CHOICES, help_text='Select Product Type')
        self.fields['name'] = forms.CharField(label='Product Name:', required=True)
        self.fields['description'] = forms.CharField(label='Product Description:', required=True, widget=forms.Textarea)
        self.fields['price'] = forms.CharField(label='Price:', required=True)
        self.fields['category'] = forms.ModelChoiceField(label='Category:', required=True, queryset=cmod.Category.objects.all())
        # .values_list('name', flat=True)

        # class specific fields
        # Bulk
        self.fields['quantity'] = forms.CharField(label='Quantity:', required=False)
        self.fields['quantity'].widget.attrs['class'] = 'Bulk'
        self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger:', required=False)
        self.fields['reorder_trigger'].widget.attrs['class'] = 'Bulk'
        self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity:', required=False)
        self.fields['reorder_quantity'].widget.attrs['class'] = 'Bulk'
        # Individual Rental
        self.fields['pid'] = forms.CharField(label='Product ID:', required=False)

        # Just Rental
        self.fields['max_rental_days'] = forms.CharField(label='Max Rental Days:', required=False)
        self.fields['max_rental_days'].widget.attrs['class'] = 'Rental'
        self.fields['retire_date'] = forms.DateTimeField(label='Retire Date:', required=False)
        self.fields['retire_date'].widget.attrs['class'] = 'Rental'




    def clean(self):
        if self.cleaned_data.get('type') == 'BulkProduct':
            if self.cleaned_data.get('quantity') is None:
                raise forms.ValidationError('Quantity is required')
            if self.cleaned_data.get('reorder_trigger') is None:
                raise forms.ValidationError('Reorder Trigger is required')
            if self.cleaned_data.get('reorder_quantity') is None:
                raise forms.ValidationError('Reorder Quantity is required')
        elif self.cleaned_data.get('type') == 'IndividualProduct':
            if self.cleaned_data.get('pid') == '':
                raise forms.ValidationError('Product ID is required')
        elif self.cleaned_data.get('type') == 'RentalProduct':
            if self.cleaned_data.get('pid') == '':
                raise forms.ValidationError('Product ID is required')
            if self.cleaned_data.get('retire_date') is None:
                raise forms.ValidationError('Retire Date is required')
            if self.cleaned_data.get('max_rental_days') is None:
                raise forms.ValidationError('Max Rental Days is required')
        else:
            pass

        return self.cleaned_data


    def commit(self):
        '''Process the form action'''
        p1 = cmod.Product()
        # get the common product info
        p1.__class__.__name__ = self.cleaned_data.get('type')
        p1.price = self.cleaned_data.get('price')
        p1.name = self.cleaned_data.get('name')
        p1.description = self.cleaned_data.get('description')
        p1.category = self.cleaned_data.get('category')
        # save common info
        p1.save()

        # get specific product info
        if p1.__class__.__name__ == 'BulkProduct':
            p = cmod.BulkProduct()
            p.TITLE = 'Bulk'
            p.quantity = self.cleaned_data.get('quantity')
            p.reorder_trigger = self.cleaned_data.get('reorder_trigger')
            p.reorder_quantity = self.cleaned_data.get('reorder_quantity')

        elif p1.__class__.__name__ == 'IndividualProduct':
            p = cmod.IndividualProduct()
            p.TITLE = 'Individual'
            p.pid = self.cleaned_data.get('pid')

        elif p1.__class__.__name__ == 'RentalProduct':
            p = cmod.RentalProduct()
            p.TITLE = 'Rental'
            p.pid = self.cleaned_data.get('pid')
            p.retire_date = self.cleaned_data.get('retire_date')
            p.max_rental_days = self.cleaned_data.get('max_rental_days')
        else:
            pass

        # save specifics to the database
        p.save()
