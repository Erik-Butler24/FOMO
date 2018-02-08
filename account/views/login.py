from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django_mako_plus import view_function, jscontext


@view_function
def process_request(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            #login user
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    context = {
        'form': form,

    }
    return request.dmp_render('login.html', context)


class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password')

    def clean_password(self):
        print(self.cleaned_data)
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        return 0
