from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from account import models as amod
import re
from django.contrib.auth import authenticate, login



@view_function
def process_request(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = createUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            createUserForm.commit(form, request)
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = createUserForm()

    context = {
        'form': form,

    }
    return request.dmp_render('create.html', context)


class createUserForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password')
    password2 = forms.CharField(label='Re-enter Password')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            print(password)
            print(password2)
            raise forms.ValidationError('Passwords do not match')


    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters')
        if re.search('[0-9]', password) is None:
            raise forms.ValidationError('Password must contain a number')
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        print(email)
        if amod.User.objects.filter(email = email):
            raise forms.ValidationError('There is already an account with that Email')
        return email

    def commit(self,request):
            newUser = amod.User()
            newUser.email = self.cleaned_data.get('email')
            newUser.set_password(self.cleaned_data.get('password'))
            newUser.first_name = self.cleaned_data.get('first_name')
            newUser.last_name = self.cleaned_data.get('last_name')
            newUser.save()
            user = authenticate(email = self.cleaned_data.get('email'),password = self.cleaned_data.get('password'))
            login(request, user)
