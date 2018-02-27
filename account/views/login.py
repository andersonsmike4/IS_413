from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account import models as amod
from django.contrib.auth import authenticate, login

@view_function
def process_request(request):
    '''call constructor and assign to form'''
    login_form = LoginForm(request)

    if login_form.is_valid():
        login_form.commit()
        return HttpResponseRedirect('/account/index/')
    context = {
        'login_form': login_form,
    }
    return request.dmp.render('login.html', context)

class LoginForm(Formless):
    def init(self):
        '''create fields'''
        self.fields['email'] = forms.EmailField(label='Enter Email', required=True)
        self.fields['password'] = forms.CharField(label='Enter Password', widget=forms.PasswordInput(), required=True)
        self.user = None

    def clean(self):
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))
        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')

        # return cleaned_data dictionary
        return self.cleaned_data

    def commit(self):
        '''Process the form action'''
        login(self.request, self.user)
