from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod

@view_function
def process_request(request, product: cmod.Product):


    # not using this anymore
    # initial={'name':product.name, 'description':product.description, 'category': product.category.name}
    # process the form
    # if product.__class__.__name__ == 'BulkProduct':
    #     edit_form = EditForm(request, initial={'name':product.name, 'description':product.description, 'category': product.category, 'type': product.__class__.__name__, 'status':product.status, 'price':product.price, 'quantity': product.quantity, 'reorder_trigger': product.reorder_trigger, 'reorder_quantity': product.reorder_quantity})
    # if product.__class__.__name__ == 'IndividualProduct':
    #     edit_form = EditForm(request, initial={'name':product.name, 'description':product.description, 'category': product.category, 'type': product.__class__.__name__, 'status':product.status, 'price':product.price, 'pid': product.pid})
    # if product.__class__.__name__ == 'RentalProduct':
    #     edit_form = EditForm(request, initial={'name':product.name, 'description':product.description, 'category': product.category, 'type': product.__class__.__name__, 'status':product.status, 'price':product.price, 'pid': product.pid, 'max_rental_days': product.max_rental_days, 'retire_date': product.retire_date})

    # get the initial data
    initial_data=forms.model_to_dict(product)
    initial_data.update({'type': product.__class__.__name__})
    edit_form = EditForm(request, initial=initial_data)

    if edit_form.is_valid():
        edit_form.commit(request, product)
        return HttpResponseRedirect('/manager/product_list/')

    # render the template
    return request.dmp_render('edit_product.html', {
        'edit_form': edit_form,
    })


class EditForm(Formless):
    '''An example form'''
    def init(self):
        '''Adds the fields for product form'''
        self.fields['status'] = forms.ChoiceField(label='Status:', required=True, choices=cmod.Product.STATUS_CHOICES)
        # widget=forms.RadioSelect(),
        self.fields['type'] = forms.ChoiceField(label='Type', required=True, choices=cmod.Product.TYPE_CHOICES, help_text='Select Product Type')
        # self.fields['type'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'] = forms.CharField(label='Product Name:', required=True)
        self.fields['description'] = forms.CharField(label='Product Description:', required=True, widget=forms.Textarea)
        self.fields['price'] = forms.DecimalField(label='Price:', required=True, max_digits=7, decimal_places=2)
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
        # , widget=forms.TextInput(attrs={'type': 'date'})
        self.fields['retire_date'].widget.attrs['class'] = 'Rental'




    def clean(self):
        if self.cleaned_data.get('type') == 'BulkProduct':
            if self.cleaned_data.get('quantity') == '':
                raise forms.ValidationError('Quantity is required')
            if self.cleaned_data.get('reorder_trigger') == '':
                raise forms.ValidationError('Reorder Trigger is required')
            if self.cleaned_data.get('reorder_quantity') == '':
                raise forms.ValidationError('Reorder Quantity is required')

        if self.cleaned_data.get('type') == 'IndividualProduct':
            if self.cleaned_data.get('pid') == '':
                raise forms.ValidationError('Product ID is required')

        if self.cleaned_data.get('type') == 'RentalProduct':
            if self.cleaned_data.get('pid') == '':
                raise forms.ValidationError('Product ID is required')
            if self.cleaned_data.get('max_rental_days') == '':
                raise forms.ValidationError('Max Rental Days is required')

        return self.cleaned_data


    def commit(self, request, product):
        '''Process the form action'''
        # get specific product info
        if self.cleaned_data['type'] == 'BulkProduct':
            product.quantity = self.cleaned_data.get('quantity')
            product.reorder_trigger = self.cleaned_data.get('reorder_trigger')
            product.reorder_quantity = self.cleaned_data.get('reorder_quantity')

        if self.cleaned_data['type'] == 'IndividualProduct':
            product.pid = self.cleaned_data.get('pid')

        if self.cleaned_data['type'] == 'RentalProduct':
            product.pid = self.cleaned_data.get('pid')
            product.retire_date = self.cleaned_data.get('retire_date')
            product.max_rental_days = self.cleaned_data.get('max_rental_days')

        # get the common product info
        product.name = self.cleaned_data.get('name')
        product.description = self.cleaned_data.get('description')
        product.price = self.cleaned_data.get('price')
        product.category = self.cleaned_data.get('category')
        product.status = self.cleaned_data.get('status')

        # save to database
        product.save()
