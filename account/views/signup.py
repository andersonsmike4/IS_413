from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms
from account import models as amod
from django.contrib.auth import authenticate, login
import re

@view_function
def process_request(request):
    # call constructor and assign to form
    signup_form = SignupForm(request)

    if signup_form.is_valid():
        signup_form.commit()
        return HttpResponseRedirect('/account/index/')
    context = {
        'signup_form': signup_form,
    }
    return request.dmp.render('signup.html', context)

class SignupForm(Formless):
    def init(self):
        # create fields
        self.fields['first_name'] = forms.CharField(label='Enter First Name:', required=True)
        self.fields['last_name'] = forms.CharField(label='Enter Last Name:', required=True)
        self.fields['email'] = forms.EmailField(label='Enter Email:', required=True)
        self.fields['password'] = forms.CharField(label='Enter Password:', widget=forms.PasswordInput(), required=True)
        self.fields['password2'] = forms.CharField(label='Verify Password:', widget=forms.PasswordInput(), required=True)

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
        u1 = amod.User.objects.filter(email=new_user).exists()
        if u1 == True:
            raise forms.ValidationError('Email must be unique.')

        return new_user


    def clean(self):
        # grab the passwords
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')

        # check to see if the passwords don't match
        if p1 != p2:
            raise forms.ValidationError('Passwords must match')

        # return if passwords match
        return self.cleaned_data

    def commit(self):
        '''Save the user to the database'''

        # get user info
        new_user = amod.User()
        new_user.first_name = self.cleaned_data.get('first_name')
        new_user.last_name = self.cleaned_data.get('last_name')
        new_user.email = self.cleaned_data.get('email')
        new_user.set_password(self.cleaned_data.get('password'))

        # save the user info to the data base
        new_user.save()

        # authenticate and log in user
        self.user = authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password'))

        if self.user is None:
            raise forms.ValidationError('Invalid email or password.')

        # login user
        login(self.request, self.user)
