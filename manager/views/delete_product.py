from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms

@view_function
def process_request(request):

    # process the form
    form = MyForm(request)
    if form.is_valid():
        d = form.commit()
        return HttpResponseRedirect('/app/successurl/')

    # render the template
    return request.dmp_render('mytemplate.html', {
        'form': form,
    })


class MyForm(Formless):   # extending formlib.Form, not Django's forms.Form
    '''An example form'''
    def init(self):
        '''Adds the fields for this form (called at end of __init__)'''
        self.fields['name'] = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data.get('name')
        # ...
        return name

    def commit(self, c):
        '''Process the form action'''
        # do something with c (optional)
        print('>>>>', c)
        # act on the form
        print('>>>> Name is', self.cleaned_data['name'])
        # return any data (optional)
        return 4
