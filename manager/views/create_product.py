from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from catalog import models as cmod

@view_function
def process_request(request):
    # try:
    #     product = cmod.Product.objects.get(pk=request.urlparams[0])
    # except:
    #     pass

    # initial=forms.model_to_dict(product)
    # initial={'name':product.name, 'description':product.description, 'category': product.category.name}
    # process the form

        create_form = CreateForm(request)
# , 'pid': product.pid, 'max_rental_days': product.max_rental_days, 'retire_date': product.retire_date, 'quantity': product.quantity, 'reorder_trigger': product.reorder_trigger, 'reorder_quantity': product.reorder_quantity

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
        self.fields['name'] = forms.CharField(label='Product Name:', required=True)
        self.fields['description'] = forms.CharField(label='Product Description:', required=True, widget=forms.Textarea)
        self.fields['price'] = forms.CharField(label='Price:', required=True)
        self.fields['TYPE_CHOICES'] = forms.ChoiceField(label='Type', required=True, choices=cmod.Product.TYPE_CHOICES)
        # I don't know how to implement these
        self.fields['category'] = forms.ModelChoiceField(label='Category:', required=True, queryset=cmod.Category.objects.all(), to_field_name='name')
        # .values_list('name', flat=True)



        # if isinstance(cmod.BulkProduct):
        #     self.fields['quantity'] = forms.CharField(label='Quantity:', required=False)
        #     self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger:', required=False)
        #     self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity:', required=False)
        # self.fields['pid'] = forms.CharField(label='Product ID::', required=False)
        # self.fields['max_rental_days'] = forms.CharField(label='Max Rental Days:', required=False)
        # self.fields['retire_date'] = forms.DateTimeField(label='Retire Date:', required=False)
        # self.fields['quantity'] = forms.CharField(label='Quantity:', required=False)
        # self.fields['reorder_trigger'] = forms.CharField(label='Reorder Trigger:', required=False)
        # self.fields['reorder_quantity'] = forms.CharField(label='Reorder Quantity:', required=False)



    # def clean(self):
    #
    #
    #
    # def commit(self):
    #     '''Process the form action'''
