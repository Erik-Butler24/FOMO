from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login



@view_function
def process_request(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            LoginForm.commit(form, request)
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    context = {
        'form': form,

    }
    return request.dmp_render('login.html', context)


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget = forms.PasswordInput)

    def clean(self):
        user = authenticate(email = self.cleaned_data.get('email'),password = self.cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError('Username or password is incorrect')

    def commit(self, request):
        user = authenticate(email = self.cleaned_data.get('email'),password = self.cleaned_data.get('password'))
        login(request, user)
