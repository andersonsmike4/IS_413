from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account import models as amod
import re

@view_function
def process_request(request):
    # call constructor and assign to form
    signup_form = SignupForm(request)

    if signup_form.is_valid():
        return HttpResponseRedirect('/account/index/')
    context = {
        'signup_form': signup_form,
    }
    return request.dmp_render('signup.html', context)

class SignupForm(Formless):
    def init(self):
        # create fields
        self.fields['email'] = forms.EmailField(label='Enter Email', required=True)
        self.fields['password'] = forms.CharField(label='Enter Password', widget=forms.PasswordInput(), required=True)
        self.fields['password2'] = forms.CharField(label='Verify Password', widget=forms.PasswordInput(), required=True)

    def clean_password(self):
        p1 = self.cleaned_data.get('password')

        not_eight = False
        no_number = False

        # determine if the passwords are valid
        if len(p1) < 8:
            not_eight = True

        if re.search('[0-9]', p1) is None:
            no_number = True

        # throw exceptions for a password that does not have 8 or more characters and a number
        if not_eight == True & no_number == True:
            raise forms.ValidationError('Password must have 8 or more characters and contian a number.')
        if not_eight == True:
            raise forms.ValidationError('Password must contain 8 or more characters.')
        elif no_number == True:
            raise forms.ValidationError('Password must contain a number.')

        # return password if it is correct
        return p1

    def clean_email(self):
        new_user = self.cleaned_data.get('email')

        # check to see if email exists in the database
        u1 = amod.User.objects.get(email=new_user)
        if new_user == u1.email:
            raise forms.ValidationError('Email must be unique.')

        return new_user


#     def clean(self):
#         p1 = self.cleaned_data.get('password')
#         p2 = self.cleaned_data.get('password2')
#
#         # check to see if the passwords don't match
#         if p1 != p2:
#             raise forms.ValidationError('Passwords must match')
#
#         # return if passwords match
#         return self.cleaned_data
