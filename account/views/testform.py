from django import forms
from django.conf import settings
from django_mako_plus import view_function
from django.http import HttpResponseRedirect
from formlib import Formless

@view_function
def process_request(request):

    # prints out the uncleaned data
    # if request.method == 'POST':
    #     print(request.POST['favorite_ice_cream'], type(request.POST['favorite_ice_cream']))
    #     print(request.POST['renewal_date'], type(request.POST['renewal_date']))
    #     print(request.POST['age'], type(request.POST['age']))
    # process the forms

    form = TestForm(request)
    if form.is_valid():
        # once you get here, everything is cleaned. Do not perform data changes here!!!
        # You can no longer inform the user that there is a problem
        print(form.cleaned_data)
        # do the work of the form
        # make the payment
        # create the user
        return HttpResponseRedirect('/')

    context = {
        'form': form,
    }
    return request.dmp_render('testform.html', context)


class TestForm(Formless):
    def init(self):
        self.fields['favorite_ice_cream'] = forms.CharField(label='Favorite Ice Cream')
        self.fields['renewal_date'] = forms.DateField(label='Renewal', help_text="Enter a date between now and 4 weeks (default 3).")
        self.fields['age'] = forms.IntegerField(label='Age')
        self.fields['password1'] = forms.CharField(label='Enter your password')
        self.fields['password2'] = forms.CharField(label='Verify your password')
        options = [
            'Choice 1',
            'Choice 2',
            'Choice 3',
        ]
        # this is not working
        # drop_down = forms.ChoiceField(label='Choices', widget=forms.Select(choices=options))

    # is_valid() calls the clean methods
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError('You must be 18 year or older to signup.')
        return age

    def clean(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError('Passwords must match')
        return self.cleaned_data
