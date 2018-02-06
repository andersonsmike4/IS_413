from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib import Formless
from django import forms

@view_function
def process_request(request):
    # call constructor and assign to form
    login_form = LoginForm(request)

    if login_form.is_valid():
        return HttpResponseRedirect('/account/index/')
    context = {
        'login_form': login_form,
    }
    return request.dmp_render('login.html', context)

class LoginForm(Formless):
    def init(self):
        # create fields
        self.fields['email'] = forms.EmailField(label='Enter Email', required=True)
        self.fields['password'] = forms.CharField(label='Enter Password', widget=forms.PasswordInput(), required=True)
